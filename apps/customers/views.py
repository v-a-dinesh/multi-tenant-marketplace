# apps/customers/views.py
from django.http import JsonResponse
from django.db import connection
from .models import Tenant, Domain

def schema_info(request):
    """Debug view to see current schema information"""
    return JsonResponse({
        'current_schema': connection.schema_name,
        'tenant': getattr(request, 'tenant', None).name if hasattr(request, 'tenant') else 'No tenant',
        'domain': request.get_host(),
        'all_tenants': list(Tenant.objects.values('name', 'schema_name')),
    })

# apps/customers/views.py (add to existing)

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from django_tenants.utils import get_public_schema_name

def request_flow_view(request):
    """Demonstrates the complete request flow in multi-tenancy"""
    
    # Get tenant from request
    tenant = getattr(request, 'tenant', None)
    
    # Build the flow explanation
    flow = [
        {
            'step': 1,
            'action': 'Request Received',
            'details': f"Domain: {request.get_host()}, Path: {request.path}"
        },
        {
            'step': 2,
            'action': 'TenantMainMiddleware Processing',
            'details': 'Middleware extracts domain from request'
        },
        {
            'step': 3,
            'action': 'Domain Lookup',
            'details': f"Query: SELECT tenant_id FROM domains WHERE domain='{request.get_host()}'"
        },
        {
            'step': 4,
            'action': 'Tenant Found' if tenant else 'No Tenant - Using Public',
            'details': f"Tenant: {tenant.name if tenant else 'Public'}, Schema: {tenant.schema_name if tenant else get_public_schema_name()}"
        },
        {
            'step': 5,
            'action': 'Schema Switch',
            'details': f"PostgreSQL: SET search_path TO {connection.schema_name}, public;"
        },
        {
            'step': 6,
            'action': 'URL Resolution',
            'details': f"Using URLconf: {settings.ROOT_URLCONF if tenant and tenant.schema_name != 'public' else settings.PUBLIC_SCHEMA_URLCONF}"
        },
        {
            'step': 7,
            'action': 'View Processing',
            'details': 'All database queries now use the tenant schema'
        }
    ]
    
    return JsonResponse({
        'current_state': {
            'domain': request.get_host(),
            'tenant': tenant.name if tenant else 'No tenant',
            'schema': connection.schema_name,
            'is_public': connection.schema_name == get_public_schema_name()
        },
        'request_flow': flow,
        'postgresql_info': {
            'current_search_path': connection.schema_name,
            'explanation': 'All tables are prefixed with this schema name'
        }
    }, json_dumps_params={'indent': 2})
# apps/customers/views.py (add to existing)

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.customers.models import Tenant
from apps.customers.db_utils import explain_db_routing

User = get_user_model()

def database_routing_view(request):
    """Shows how database queries are routed"""
    
    routing_info = explain_db_routing()
    
    # Demonstrate actual queries
    tenant_data = {
        'products_count': Product.objects.count(),  # From tenant schema
        'users_count': User.objects.count(),        # From tenant schema
        'all_tenants_count': Tenant.objects.count(), # Always from public schema
    }
    
    # Show raw SQL that would be executed
    from django.db import connection
    
    # Get the actual SQL for a query
    products_query = Product.objects.all().query
    
    return JsonResponse({
        'routing_explanation': routing_info,
        'current_tenant_data': tenant_data,
        'sample_sql': str(products_query),
        'connection_info': {
            'schema': connection.schema_name,
            'tenant': getattr(request, 'tenant', None).name if hasattr(request, 'tenant') else 'No tenant',
        }
    }, json_dumps_params={'indent': 2})


# apps/customers/views.py (add to existing)

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt  # Just for demo - don't do this in production!
def test_auth_view(request):
    """Demonstrates that each tenant has separate users"""
    
    tenant = getattr(request, 'tenant', None)
    
    if request.method == 'POST':
        # Create a test user for this tenant
        username = f"testuser_{connection.schema_name}"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            message = f"Created user: {username} in schema: {connection.schema_name}"
        else:
            message = f"User already exists: {username} in schema: {connection.schema_name}"
        
        return JsonResponse({
            'message': message,
            'tenant': tenant.name if tenant else 'No tenant',
            'schema': connection.schema_name,
            'user_id': user.id,
            'total_users_in_tenant': User.objects.count()
        })
    
    # GET request - show current auth status
    return JsonResponse({
        'tenant': tenant.name if tenant else 'No tenant',
        'schema': connection.schema_name,
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'users_in_this_tenant': list(User.objects.values_list('username', flat=True)),
        'session_info': {
            'session_key': request.session.session_key,
            'explanation': 'Sessions are shared but user data is per-tenant'
        }
    })

# apps/customers/views.py (add to existing)

from django.conf import settings
from django_tenants.utils import get_tenant_model, get_tenant_domain_model

def configuration_summary_view(request):
    """Shows complete multi-tenant configuration"""
    
    return JsonResponse({
        'django_tenants_config': {
            'TENANT_MODEL': settings.TENANT_MODEL,
            'TENANT_DOMAIN_MODEL': settings.TENANT_DOMAIN_MODEL,
            'PUBLIC_SCHEMA_NAME': getattr(settings, 'PUBLIC_SCHEMA_NAME', 'public'),
            'DATABASE_ENGINE': settings.DATABASES['default']['ENGINE'],
        },
        'apps_configuration': {
            'SHARED_APPS': settings.SHARED_APPS,
            'TENANT_APPS': settings.TENANT_APPS,
        },
        'middleware_order': [
            m for m in settings.MIDDLEWARE 
            if 'tenant' in m.lower() or 'TenantMainMiddleware' in m
        ],
        'url_configuration': {
            'ROOT_URLCONF': settings.ROOT_URLCONF,
            'PUBLIC_SCHEMA_URLCONF': getattr(settings, 'PUBLIC_SCHEMA_URLCONF', None),
        },
        'current_request_info': {
            'domain': request.get_host(),
            'tenant': getattr(request, 'tenant', None).name if hasattr(request, 'tenant') else 'No tenant',
            'schema': connection.schema_name,
        }
    }, json_dumps_params={'indent': 2})