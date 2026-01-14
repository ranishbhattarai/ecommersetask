from django.db import models
from django.conf import settings

# Create your models here.
user=settings.AUTH_USER_MODEL

class Notification(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
