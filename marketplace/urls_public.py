# marketplace/urls.py
from django.contrib import admin
from django.urls import path
from apps.customers.views import schema_info
from apps.products.views import tenant_data_view
from apps.products.views import media_info_view
from apps.customers.views import request_flow_view
from apps.customers.views import test_auth_view
from django.http import JsonResponse

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
    path('schema-info/', schema_info, name='schema_info'),
    path('data/', tenant_data_view, name='tenant_data'),
    path('media-info/', media_info_view, name='media_info'),
    path('', public_home, name='public_home'),
    path('request-flow/', request_flow_view, name='request_flow'),
    path('test-auth/', test_auth_view, name='test_auth'),
]


