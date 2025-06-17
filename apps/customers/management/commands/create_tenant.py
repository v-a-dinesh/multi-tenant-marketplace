# apps/customers/management/commands/create_tenant.py
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.customers.models import Tenant, Domain

class Command(BaseCommand):
    help = 'Creates a new tenant with domain'
    
    def add_arguments(self, parser):
        parser.add_argument('--name', required=True, help='Tenant name')
        parser.add_argument('--email', required=True, help='Tenant email')
        parser.add_argument('--schema', required=True, help='Schema name (no spaces, lowercase)')
        parser.add_argument('--domain', required=True, help='Domain (e.g., tenant1.localhost)')
    
    def handle(self, *args, **options):
        name = options['name']
        email = options['email']
        schema_name = options['schema']
        domain_name = options['domain']
        
        try:
            with transaction.atomic():
                # Create tenant
                tenant = Tenant(
                    name=name,
                    email=email,
                    schema_name=schema_name,
                )
                tenant.save()
                self.stdout.write(f"Created tenant: {tenant}")
                
                # Create domain
                domain = Domain(
                    domain=domain_name,
                    tenant=tenant,
                    is_primary=True
                )
                domain.save()
                self.stdout.write(f"Created domain: {domain}")
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created tenant '{name}' with schema '{schema_name}'"
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error creating tenant: {str(e)}")
            )