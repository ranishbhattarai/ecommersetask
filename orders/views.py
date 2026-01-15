from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderSerializer
from users.permissions import IsCustomer 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
# Create your views here.
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    filter_backends = [DjangoFilterBackend]
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

@action(detail=False, methods=['post'], url_path='place-order')
def place_order(self, request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    # Logic to create an order
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    product=product.objects.get(id=product_id)

    if product.stock < quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.create(
        customer=request.user,
        total_amount=product.price * quantity,)
    
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price
    )

    product.stock -= quantity
    product.save()

    #email(console log)
    send_mail(
        'Order Confirmation',
        f'Thank you for your order #{order.id}. Your order has been placed successfully.',
        None,
        [request.user.email],
    )
    return Response({'message': 'Order placed successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)
