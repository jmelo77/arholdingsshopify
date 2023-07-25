from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    published = models.SmallIntegerField(default=0)
    is_featured = models.SmallIntegerField(default=0)
    visibility_in_catalog = models.CharField(max_length=50)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    date_sale_price_starts = models.CharField(max_length=50, blank=True)
    date_sale_price_ends = models.CharField(max_length=50, blank=True)
    tax_status = models.CharField(max_length=50)
    tax_class = models.CharField(max_length=50)
    in_stock = models.SmallIntegerField(default=0)
    stock = models.IntegerField(default=0)
    backorders_allowed = models.SmallIntegerField(default=0)
    sold_individually = models.SmallIntegerField(default=0)
    weight_lbs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length_in = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width_in = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height_in = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    allow_customer_reviews = models.SmallIntegerField(default=0)
    purchase_note = models.TextField(blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    shipping_class = models.CharField(max_length=100, blank=True)
    images = models.TextField(blank=True)
    download_limit = models.IntegerField(default=0)
    download_expiry_days = models.IntegerField(default=0)
    parent = models.CharField(max_length=100, blank=True)
    grouped_products = models.CharField(max_length=255, blank=True)
    upsells = models.CharField(max_length=255, blank=True)
    cross_sells = models.CharField(max_length=255, blank=True)
    external_url = models.URLField(blank=True)
    button_text = models.CharField(max_length=100, blank=True)
    position = models.IntegerField(default=0)
    attribute_1_name = models.CharField(max_length=100, blank=True)
    attribute_1_values = models.CharField(max_length=255, blank=True)
    attribute_2_name = models.CharField(max_length=100, blank=True)
    attribute_2_values = models.CharField(max_length=255, blank=True)
    attribute_3_name = models.CharField(max_length=100, blank=True)
    attribute_3_values = models.CharField(max_length=255, blank=True)
    attribute_4_name = models.CharField(max_length=100, blank=True)
    attribute_4_values = models.CharField(max_length=255, blank=True)
    attribute_5_name = models.CharField(max_length=100, blank=True)
    attribute_5_values = models.CharField(max_length=255, blank=True)
    meta_wpcom_is_markdown = models.SmallIntegerField(default=0)
    download_1_name = models.CharField(max_length=100, blank=True)
    download_1_url = models.URLField(blank=True)
    download_2_name = models.CharField(max_length=100, blank=True)
    download_2_url = models.URLField(blank=True)
    synchronized_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)


class ProductLog(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=100)
    topic = models.CharField(max_length=100, blank=True)
    json = models.JSONField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)
