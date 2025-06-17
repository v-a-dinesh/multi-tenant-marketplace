from django.contrib import admin
from django.urls import path
from apps.customers import views  # or wherever your view is
from apps.products.views import tenant_data_view
from django.http import JsonResponse
from apps.products.views import media_info_view
from apps.customers.views import request_flow_view
from apps.customers.views import database_routing_view
from apps.customers.views import configuration_summary_view
from apps.customers.views import test_auth_view

def public_home(request):
    return JsonResponse({
        'message': 'This is the public schema',
        'info': 'Access tenant sites using subdomain.localhost:8000',
        'available_tenants': [
            'http://techstore.localhost:8000',
            'http://fashion.localhost:8000'
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema-info/', views.schema_info, name='schema-info'),
    path('data/', tenant_data_view, name='tenant_data'), 
    path('', public_home, name='public_home'), 
    path('media-info/', media_info_view, name='media_info'),
    path('request-flow/', request_flow_view, name='request_flow'),
    path('db-routing/', database_routing_view, name='db_routing'),
    path('config/', configuration_summary_view, name='config_summary'),
    path('test-auth/', test_auth_view, name='test_auth'),
]
