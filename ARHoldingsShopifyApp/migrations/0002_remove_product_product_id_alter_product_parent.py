# Generated by Django 4.2.3 on 2023-07-22 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARHoldingsShopifyApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_id',
        ),
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.CharField(max_length=100),
        ),
    ]
