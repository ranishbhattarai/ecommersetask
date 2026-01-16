from django.db import models
from django.conf import settings

# Create your models here.

User=settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

