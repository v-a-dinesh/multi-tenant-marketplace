# apps/products/models.py
from django.db import models

class Product(models.Model):
    """Simple product model - will be created in each tenant's schema"""
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name