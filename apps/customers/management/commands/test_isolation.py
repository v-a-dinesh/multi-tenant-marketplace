# apps/customers/management/commands/test_isolation.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from apps.customers.models import Tenant

User = get_user_model()

class Command(BaseCommand):
    help = 'Test data isolation between tenants'
    
    def handle(self, *args, **options):
        # Create users in different schemas
        tenants = Tenant.objects.exclude(schema_name='public')
        
        for tenant in tenants:
            with schema_context(tenant.schema_name):
                # Create a user specific to this tenant
                user = User.objects.create_user(
                    username=f'admin_{tenant.schema_name}',
                    email=f'admin@{tenant.schema_name}.local',
                    password='testpass123'
                )
                self.stdout.write(
                    f"Created user in {tenant.schema_name}: {user.username}"
                )
                
                # Show user count in this schema
                user_count = User.objects.count()
                self.stdout.write(
                    f"Total users in {tenant.schema_name}: {user_count}"
                )
        
        # Verify isolation
        self.stdout.write("\nVerifying isolation:")
        for tenant in tenants:
            with schema_context(tenant.schema_name):
                users = User.objects.all()
                self.stdout.write(
                    f"\n{tenant.schema_name} users: {[u.username for u in users]}"
                )