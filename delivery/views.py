from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryAssignment
from .serializers import DeliveryAssignmentSerializer
from users.permissions import IsDeliveryPerson
# Create your views here.

class DeliveryAssignmentViewSet(ModelViewSet):
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticated, IsDeliveryPerson]

    def get_queryset(self):
        return DeliveryAssignment.objects.filter(delivery_person=self.request.user)
