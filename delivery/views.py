from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryAssignment
from .serializers import DeliveryAssignmentSerializer
from users.permissions import IsDeliveryPerson, IsAdmin
from notifications.utils import notify

# Create your views here.

class DeliveryAssignmentViewSet(ModelViewSet):
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticated, IsDeliveryPerson, IsAdmin]

    def get_queryset(self):
        user=self.request.user
        if user.role=='delivery':
            return DeliveryAssignment.objects.filter(delivery_person=user)
        if user.role=='admin':
            return DeliveryAssignment.objects.all()
        return DeliveryAssignment.objects.none()
    
    def perform_create(self, serializer):
        assingment=serializer.save()

        notify(
            assingment.delivery_person,
            f'New delivery assignment created for order #{assingment.order.id}.'
        )
