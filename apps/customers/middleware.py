# apps/customers/middleware.py
from django.http import JsonResponse
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class TenantDebugMiddleware:
    """
    Debug middleware to understand how tenant detection works.
    Place this AFTER TenantMainMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Before view is processed
        tenant = getattr(request, 'tenant', None)
        
        # Log tenant information
        logger.info(f"=== Tenant Debug Info ===")
        logger.info(f"Domain: {request.get_host()}")
        logger.info(f"Tenant: {tenant.name if tenant else 'No tenant'}")
        logger.info(f"Schema: {connection.schema_name}")
        logger.info(f"Path: {request.path}")
        
        # Add debug headers to response
        response = self.get_response(request)
        
        # After view is processed
        response['X-Tenant-Schema'] = connection.schema_name
        response['X-Tenant-Name'] = tenant.name if tenant else 'No tenant'
        
        return response