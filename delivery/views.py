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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'destroy']:
            # Only admin can create or delete assignments
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            # Both admin and delivery person can update (delivery person updates status)
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user=self.request.user
        # Support both 'delivery' and 'delivery_person' role names
        if user.role in ['delivery', 'delivery_person']:
            return DeliveryAssignment.objects.filter(delivery_person=user)
        if user.role=='admin':
            return DeliveryAssignment.objects.all()
        return DeliveryAssignment.objects.none()
    
    def perform_create(self, serializer):
        """Only admin can create assignments"""
        assignment=serializer.save()

        notify(
            assignment.delivery_person,
            f'New delivery assignment created for order #{assignment.order.id}.'
        )
    
    def perform_update(self, serializer):
        """Allow delivery person to update their own assignments (status changes)"""
        user = self.request.user
        assignment = self.get_object()
        
        # Delivery person can only update their own assignments
        if user.role in ['delivery', 'delivery_person'] and assignment.delivery_person != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update your own deliveries.")
        
        # Save the delivery assignment
        updated_assignment = serializer.save()
        
        # Update order status based on delivery status
        order = updated_assignment.order
        delivery_status = updated_assignment.status
        
        if delivery_status == 'picked' and order.status == 'PENDING':
            order.status = 'SHIPPED'
            order.save()
        elif delivery_status == 'on_way' and order.status != 'DELIVERED':
            order.status = 'SHIPPED'
            order.save()
        elif delivery_status == 'delivered':
            order.status = 'DELIVERED'
            order.save()
