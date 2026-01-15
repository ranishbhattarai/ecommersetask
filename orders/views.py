from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer
from users.permissions import IsCustomer 
# Create your views here.
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    filterset_fields = ['status','customer']
    def get_queryset(self):
        user=self.request.user
        if user.role=='admin':
            return Order.objects.all()
        if user.role=='customer':
            return Order.objects.filter(customer=user)
        return Order.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
