# Generated by Django 4.2.3 on 2023-07-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARHoldingsShopifyApp', '0009_productlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlog',
            name='topic',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]