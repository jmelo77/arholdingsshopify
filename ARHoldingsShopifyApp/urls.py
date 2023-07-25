from django.urls import path
from . import views

urlpatterns = [
    path('migrate_data/', views.migrate_data, name='migrate_data'),
    path('publish_product/', views.publish_product_to_shopify, name='publish_product_to_shopify'),
    path('create_webhook/', views.create_webhook, name='create_webhook'),
    path('update_webhook/', views.update_webhook, name='update_webhook'),
    path('webhooks/', views.log_webhook, name='log_webhook'),
]