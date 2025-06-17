# apps/customers/management/commands/create_sample_tenants.py
from django.core.management.base import BaseCommand
from apps.customers.models import Tenant, Domain

class Command(BaseCommand):
    """Create sample tenants for Docker environment"""

    def handle(self, *args, **options):
        # Check if tenants already exist
        if Tenant.objects.filter(schema_name='techstore').exists():
            self.stdout.write('Sample tenants already exist')
            return

        # Create TechStore
        tenant1 = Tenant.objects.create(
            name='TechStore',
            email='admin@techstore.local',
            schema_name='techstore'
        )
        Domain.objects.create(
            domain='techstore.localhost',
            tenant=tenant1,
            is_primary=True
        )

        # Create Fashion Boutique
        tenant2 = Tenant.objects.create(
            name='Fashion Boutique',
            email='admin@fashion.local',
            schema_name='fashion'
        )
        Domain.objects.create(
            domain='fashion.localhost',
            tenant=tenant2,
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS('Sample tenants created!'))