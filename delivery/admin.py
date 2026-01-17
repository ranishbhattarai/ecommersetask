from django.contrib import admin
from .models import DeliveryAssignment

@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'delivery_person', 'status', 'assigned_at']
    list_filter = ['status', 'assigned_at']
    search_fields = ['order__id', 'delivery_person__username']
    list_editable = ['status']
    readonly_fields = ['assigned_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'admin':
            return qs
        elif request.user.role in ['delivery', 'delivery_person']:
            return qs.filter(delivery_person=request.user)
        return qs.none()
