from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.permissions import IsAdmin

# Create your views here.

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category','stock']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'supplier':
            return Product.objects.filter(supplier=user)
        return Product.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

