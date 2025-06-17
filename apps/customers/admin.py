# apps/customers/admin.py
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain

@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    """
    Admin interface for managing tenants.
    TenantAdminMixin ensures admin actions work correctly with schemas.
    """
    list_display = ('name', 'schema_name', 'is_active', 'created_on', 'paid_until')
    list_filter = ('is_active', 'on_trial', 'created_on')
    search_fields = ('name', 'email', 'schema_name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'schema_name')
        }),
        ('Business Details', {
            'fields': ('description', 'is_active')
        }),
        ('Subscription', {
            'fields': ('on_trial', 'paid_until')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing tenant
            return ['schema_name', 'created_on']
        return ['created_on']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """Admin interface for managing domains."""
    list_display = ('domain', 'tenant', 'is_primary', 'ssl_enabled')
    list_filter = ('is_primary', 'ssl_enabled')
    search_fields = ('domain', 'tenant__name')
    
    fieldsets = (
        (None, {
            'fields': ('domain', 'tenant', 'is_primary', 'ssl_enabled')
        }),
    )