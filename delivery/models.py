from django.db import models
from django.conf import settings
from orders.models import Order

User=settings.AUTH_USER_MODEL

class DeliveryAssignment(models.Model):
    delivery_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=20, choices=(
        ('assigned', 'Assigned'),
        ('picked', 'Picked'),
        ('on_way', 'On the Way'),
        ('delivered', 'Delivered'),
    ), default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id}"
