# apps/products/management/commands/create_test_data.py
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from apps.customers.models import Tenant
from apps.products.models import Product
from apps.orders.models import Order

class Command(BaseCommand):
    help = 'Creates test data in each tenant'
    
    def handle(self, *args, **options):
        # Get all tenants except public
        tenants = Tenant.objects.exclude(schema_name='public')
        
        for tenant in tenants:
            self.stdout.write(f"\nCreating data for {tenant.name} (schema: {tenant.schema_name})")
            
            with schema_context(tenant.schema_name):
                # Create products specific to this tenant
                if tenant.schema_name == 'techstore':
                    Product.objects.create(name="Laptop", price=999.99)
                    Product.objects.create(name="Mouse", price=29.99)
                    Order.objects.create(order_number="TECH001", total_amount=1029.98)
                    
                elif tenant.schema_name == 'fashion':
                    Product.objects.create(name="T-Shirt", price=19.99)
                    Product.objects.create(name="Jeans", price=49.99)
                    Order.objects.create(order_number="FASH001", total_amount=69.98)
                
                # Show what was created
                products = Product.objects.all()
                orders = Order.objects.all()
                
                self.stdout.write(f"  Products: {[p.name for p in products]}")
                self.stdout.write(f"  Orders: {[o.order_number for o in orders]}")