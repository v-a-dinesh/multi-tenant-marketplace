# apps/orders/models.py
from django.db import models

class Order(models.Model):
    """Simple order model - will be created in each tenant's schema"""
    order_number = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return f"Order {self.order_number}"