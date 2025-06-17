# apps/customers/utils.py
from django_tenants.utils import schema_context, get_tenant_model
from django.db import connection

def get_current_schema():
    """Get the currently active schema"""
    return connection.schema_name

def list_all_schemas():
    """List all tenant schemas"""
    Tenant = get_tenant_model()
    return list(Tenant.objects.values_list('schema_name', flat=True))

def execute_in_tenant(tenant_schema, func, *args, **kwargs):
    """Execute a function in a specific tenant's schema context"""
    with schema_context(tenant_schema):
        return func(*args, **kwargs)

def get_tenant_by_request(request):
    """Get tenant from request object"""
    return getattr(request, 'tenant', None)

class TenantContextManager:
    """
    Context manager for switching between tenant schemas
    Usage:
        with TenantContextManager('techstore'):
            # All operations here use techstore schema
            products = Product.objects.all()
    """
    def __init__(self, schema_name):
        self.schema_name = schema_name
        self.previous_schema = None
    
    def __enter__(self):
        self.previous_schema = connection.schema_name
        connection.set_schema(self.schema_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        connection.set_schema(self.previous_schema)