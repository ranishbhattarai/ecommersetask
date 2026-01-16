from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'supplier', 'created_at']
    list_filter = ['category', 'supplier', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Force database write
        obj.refresh_from_db()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
