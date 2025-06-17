# apps/customers/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    """
    Tenant model stores each client's information.
    Inherits from TenantMixin which provides:
    - schema_name: PostgreSQL schema name for this tenant
    - created_on: Timestamp when tenant was created
    """
    # Basic tenant information
    name = models.CharField(max_length=100, help_text="Company/Store name")
    email = models.EmailField(help_text="Primary contact email")
    
    # Business information
    description = models.TextField(blank=True, help_text="About the store")
    is_active = models.BooleanField(default=True, help_text="Is store active?")
    created_on = models.DateField(auto_now_add=True)
    
    # Subscription/Plan information
    on_trial = models.BooleanField(default=True)
    paid_until = models.DateField(null=True, blank=True)
    
    # Schema will be automatically created when saving
    auto_create_schema = True
    auto_drop_schema = True  # Be careful with this in production!
    
    class Meta:
        db_table = 'tenants'
    
    def __str__(self):
        return f"{self.name} (Schema: {self.schema_name})"


class Domain(DomainMixin):
    """
    Domain model maps domains/subdomains to tenants.
    Inherits from DomainMixin which provides:
    - domain: The complete domain/subdomain for this tenant
    - tenant: ForeignKey to Tenant model
    - is_primary: Boolean indicating primary domain
    """
    # Additional fields if needed
    ssl_enabled = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'domains'
    
    def __str__(self):
        return f"{self.domain} -> {self.tenant.name}"