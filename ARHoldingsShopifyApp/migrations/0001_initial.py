# Generated by Django 4.2.3 on 2023-07-21 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.BigIntegerField(unique=True)),
                ('type', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('published', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('visibility_in_catalog', models.BooleanField(default=True)),
                ('short_description', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('date_sale_price_starts', models.DateTimeField(blank=True, null=True)),
                ('date_sale_price_ends', models.DateTimeField(blank=True, null=True)),
                ('tax_status', models.CharField(max_length=50)),
                ('tax_class', models.CharField(max_length=50)),
                ('in_stock', models.BooleanField(default=True)),
                ('stock', models.IntegerField(default=0)),
                ('backorders_allowed', models.BooleanField(default=False)),
                ('sold_individually', models.BooleanField(default=False)),
                ('weight_lbs', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('length_in', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('width_in', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('height_in', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('allow_customer_reviews', models.BooleanField(default=True)),
                ('purchase_note', models.TextField(blank=True)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('regular_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('categories', models.CharField(blank=True, max_length=255)),
                ('tags', models.CharField(blank=True, max_length=255)),
                ('shipping_class', models.CharField(blank=True, max_length=100)),
                ('images', models.CharField(blank=True, max_length=255)),
                ('download_limit', models.IntegerField(default=0)),
                ('download_expiry_days', models.IntegerField(default=0)),
                ('grouped_products', models.CharField(blank=True, max_length=255)),
                ('upsells', models.CharField(blank=True, max_length=255)),
                ('cross_sells', models.CharField(blank=True, max_length=255)),
                ('external_url', models.URLField(blank=True)),
                ('button_text', models.CharField(blank=True, max_length=100)),
                ('position', models.IntegerField(default=0)),
                ('attribute_1_name', models.CharField(blank=True, max_length=100)),
                ('attribute_1_values', models.CharField(blank=True, max_length=255)),
                ('attribute_2_name', models.CharField(blank=True, max_length=100)),
                ('attribute_2_values', models.CharField(blank=True, max_length=255)),
                ('attribute_3_name', models.CharField(blank=True, max_length=100)),
                ('attribute_3_values', models.CharField(blank=True, max_length=255)),
                ('attribute_4_name', models.CharField(blank=True, max_length=100)),
                ('attribute_4_values', models.CharField(blank=True, max_length=255)),
                ('attribute_5_name', models.CharField(blank=True, max_length=100)),
                ('attribute_5_values', models.CharField(blank=True, max_length=255)),
                ('meta_wpcom_is_markdown', models.BooleanField(default=False)),
                ('download_1_name', models.CharField(blank=True, max_length=100)),
                ('download_1_url', models.URLField(blank=True)),
                ('download_2_name', models.CharField(blank=True, max_length=100)),
                ('download_2_url', models.URLField(blank=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ARHoldingsShopifyApp.product')),
            ],
        ),
    ]
