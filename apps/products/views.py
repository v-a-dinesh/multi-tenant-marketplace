# apps/products/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Product
from apps.orders.models import Order

def tenant_data_view(request):
    """Shows data from current tenant"""
    
    # Get current tenant info
    current_tenant = getattr(request, 'tenant', None)
    current_schema = connection.schema_name
    
    # Get data (automatically from current tenant's schema)
    products = Product.objects.all()
    orders = Order.objects.all()
    
    data = {
        'tenant_info': {
            'name': current_tenant.name if current_tenant else 'No tenant',
            'schema': current_schema,
            'domain': request.get_host(),
        },
        'products': [
            {'name': p.name, 'price': str(p.price)} 
            for p in products
        ],
        'orders': [
            {'order_number': o.order_number, 'total': str(o.total_amount)} 
            for o in orders
        ],
        'counts': {
            'products': products.count(),
            'orders': orders.count(),
        }
    }
    
    return JsonResponse(data, json_dumps_params={'indent': 2})
import os
from django.conf import settings
from django.http import JsonResponse
from django.db import connection

def media_info_view(request):
    """Shows how media files are organized per tenant"""
    tenant = getattr(request, 'tenant', None)
    
    if tenant and tenant.schema_name != 'public':
        media_root = os.path.join(
            settings.MEDIA_ROOT, 
            'tenant', 
            tenant.schema_name
        )
    else:
        media_root = settings.MEDIA_ROOT
    
    return JsonResponse({
        'tenant': tenant.name if tenant else 'Public',
        'schema': connection.schema_name,
        'media_root': media_root,
        'media_url': settings.MEDIA_URL,
        'explanation': 'Each tenant can have separate media folders'
    })