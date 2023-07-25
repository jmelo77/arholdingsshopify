import json
import requests
import pandas as pd
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .config import Config
from .models import Product, ProductLog

shop_conf = Config.get_shop_config()
shopify_url = shop_conf['shop_url']
headers = {
    'Content-Type': 'application/json',
    "X-Shopify-Access-Token": shop_conf['shop_acces_token']
}

ngrok_config = Config.get_ngrok_config()
ngrok_url = ngrok_config['ngrok_url']

@csrf_exempt
@require_POST
def migrate_data(request):
    data = pd.read_csv('./data/sample_data.csv')

    # Replace NaN values in numeric columns with 0
    numeric_columns = data.select_dtypes(include=['number']).columns
    data[numeric_columns] = data[numeric_columns].fillna(0)

    # Replace NaN values in string columns with an empty string
    string_columns = data.select_dtypes(include=['object']).columns
    data[string_columns] = data[string_columns].fillna('')
    data.columns = data.columns.str.lower()
    data.columns = data.columns.str.replace(' ', '_')
    data.columns = data.columns.str.replace('?', '')
    data.columns = data.columns.str.replace(':', '')
    data.columns = data.columns.str.replace('(', '')
    data.columns = data.columns.str.replace(')', '')
    data.columns = data.columns.str.replace(' ', '_')
    data.columns = data.columns.str.replace('__', '_')
    data.columns = data.columns.str.replace('-', '_')

    try:
        for index, row in data.iterrows():
            # Create the model instance dynamically
            model_instance = Product(**dict(row))
            model_instance.save()
        return JsonResponse({'message': 'Record saved successfully'})
    except IntegrityError as e:
        return JsonResponse({'error_message': str(e)}, status=500)

@csrf_exempt
@require_POST
def publish_product_to_shopify(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        request_data = {}
    create_collections = request_data.get('create_collections', False)
    response_data = {}
    try:
        if create_collections:
            # Query distinct categories
            distinct_categories = Product.objects.filter(categories__isnull=False).values_list('categories', flat=True).distinct()

            # Convert the records to a pandas DataFrame
            df = pd.DataFrame.from_records(distinct_categories.values())
        
            # Split the strings and drop the duplicates to have only the required values
            categories = df['categories'].apply(lambda x: x.split('|')[0].split('>')[-1]).T.drop_duplicates().values

            # For every type of product we create a smart collection that will detect the tags of the products
            for clothe_type in categories:
                # The dictionary (JSON) that defines the smart collection structure is created
                if clothe_type != "":
                    collection = {"smart_collection":{"title":f'{clothe_type}',"rules":[{"column":"tag","relation":"equals","condition":f'{clothe_type}'}]}}
                    # URL smartcollection
                    post_url = f"{shopify_url}/admin/api/2023-07/smart_collections.json"

                    # Send the request
                    r = requests.post(post_url, data=json.dumps(collection), headers=headers)
                    response_data = r.json()
        
        # start_index = 0 
        # end_index = 10
        # parents = Product.objects.filter(parent='').order_by('id')[start_index:end_index + 1]

        # Now we extract all the product info on the parent or simple items
        parents = Product.objects.filter(parent='').order_by('id')

        # For every parent, search its variants, add the required information, and link the images
        # Iterate over parent objects
        for parent in parents:
            if parent.sku != '':
                print(parent.sku)
            
                # Query to extract all the variants
                products = Product.objects.filter(sku__startswith=parent.sku).order_by('-id')
                df = pd.DataFrame.from_records(products.values())

                # Initialize product JSON
                product = {"product":{}}
                
                # Edge case validation for products that have a different name estructure
                if ';' in df['name'][0]:
                    product['product']['title'] = df['name'][0].split(';')[1]
                else:
                    product['product']['title'] = df['name'][0].split('-')[0]

                # Fill the required information
                product['product']['body_html'] =  df['description'][0]
                product['product']['product_type'] = df['categories'][0].split('|')[0].split('>')[-1]
                product['product']['tags'] = f"{df['categories'][0].split('|')[0].split('>')[-1]}"
                product['product']['variants'] = []

                # If type is no simple it means it has multiple variants if not only add one, create the different variants
                if df['type'][0] != 'simple':
                    
                    for index, row in df.iterrows():
                        if row['sku'] == parent.sku:
                            continue

                        variant = {}
                        variant['option1'] = row['attribute_1_values']
                        variant['option2'] = row['attribute_2_values']
                        variant['price'] = row['regular_price']
                        variant['weight'] = row['weight_lbs']
                        variant['weight_unit'] = 'lb'
                        variant['sku'] = row["sku"]
                        variant['inventory_management'] = 'shopify'
                        product['product']['variants'].append(variant)
                    
                    # Create the options for the products that have it            
                    product['product']['options'] = [{"name": df['attribute_1_name'][1],"values":(list)(df['attribute_1_values'].dropna().drop_duplicates().values)},
                                                    {"name": df['attribute_2_name'][1],"values":(list)(df['attribute_2_values'].dropna().drop_duplicates().values)}]
                    
                else:
                    variant = {}
                    variant['title'] = df['name'][0]
                    variant['price']= df['regular_price'][0]
                    variant['weight'] = df['weight_lbs'][0]
                    variant['weight_unit'] = 'lb'
                    variant['sku'] = df['sku'][0]
                    variant['inventory_management'] = 'shopify'
                    product['product']['variants'].append(variant)
                
                # URL product
                product_url = f"{shopify_url}/admin/api/2023-04/products.json"

                # Create and Get the created product
                r = requests.post(product_url, data=json.dumps(product, default=str), headers=headers)
                response_data = r.json()

                # After saving update the sync column to current time for the product and his variants
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Product.objects.filter(sku=parent.sku).update(synchronized_at=current_datetime)

                # Get the location of the store to be able to update the inventory later
                location = requests.get(f"{shopify_url}/admin/api/2023-07/locations/87101243674.json", headers=headers).json()

                # If the product was created succesfully we update the images and inventory
                if r.status_code == 201:
                    r = r.json()
                    inventory_url = f"{shopify_url}/admin/api/2023-07/inventory_levels/set.json"

                    # For every variant of the product update and link the images, and update the stock
                    for variant in r['product']['variants']:
                        # we create the inventory level JSON
                        inventory_json = {"location_id":location['location']['id'],
                                            "inventory_item_id":variant['inventory_item_id'],
                                            "available":(str)(df[df['sku'] == variant['sku']]['stock'].values[0])}
                        
                        # Set the stock quantity of the variants
                        requests.post(inventory_url, data=json.dumps(inventory_json), headers=headers)

                        # We populate the image json
                        image = {"image":{'product_id': r['product']['id'],
                                        'variant_ids': [variant['id']],
                                        'src':df[df['sku'] == variant['sku']]['images'].values[0].split(',')[0]}}

                        # Assign the image to a product
                        image = requests.post(f"{shopify_url}/admin/api/2023-07/products/{r['product']['id']}/images.json", 
                                            data=json.dumps(image), 
                                            headers=headers)

                        # Assign the image to a product variant
                        variant_json = {"variant":{"id": variant['id'], "image_id": image.json()['image']['id']}}

                        # Sent the update
                        variant = requests.put(f"{shopify_url}/admin/api/2023-07/variants/{variant['id']}.json", 
                                                data=json.dumps(variant_json), 
                                                headers=headers)
            
        return JsonResponse(response_data)
    
    except requests.exceptions.RequestException as e:
        error_message = {'error': str(e)}
        return JsonResponse(error_message, status=500)

@csrf_exempt
@require_POST
def create_webhook(request):
    try:
        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            request_data = {}
        topic = request_data.get('topic', 'products/create')

        webhook_json = {"webhook":{}}
        webhook_json["webhook"]['address'] = f"{ngrok_url}/api/webhooks/"
        webhook_json["webhook"]['topic'] = topic
        webhook_json["webhook"]['format'] = 'json'

        # Send the request
        url = f"{shopify_url}/admin/api/2023-07/webhooks.json"
        r = requests.post(url, data=json.dumps(webhook_json, default=str), headers=headers)
        response_data = r.json()
        
        return JsonResponse(response_data)
    
    except requests.exceptions.RequestException as e:
        error_message = {'error': str(e)}
        return JsonResponse(error_message, status=500)

@csrf_exempt
def update_webhook(request):
    if request.method == 'PUT':
        try:
            try:
                request_data = json.loads(request.body)
            except json.JSONDecodeError:
                request_data = {}
            id = request_data.get('id', '')

            webhook_json = {"webhook":{}}
            webhook_json["webhook"]['id'] = id
            webhook_json["webhook"]['address'] = f"{ngrok_url}/api/webhooks/"
            webhook_json["webhook"]['format'] = 'json'

            # Send the request
            url = f"{shopify_url}/admin/api/2023-07/webhooks/{id}.json"
            r = requests.put(url, data=json.dumps(webhook_json, default=str), headers=headers)
            response_data = r.json()
        
            return JsonResponse(response_data)
    
        except requests.exceptions.RequestException as e:
            error_message = {'error': str(e)}
            return JsonResponse(error_message, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def log_webhook(request):
    if request.method == 'POST':
        res = request.body.decode()
        response_data = json.loads(res)

        product_id = response_data.get('id', '')
        topic = request.headers['X-Shopify-Topic']
        product_log = ProductLog(product_id=product_id, topic=topic, json=response_data)
        product_log.save()

        return JsonResponse({'message': 'Record saved successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
