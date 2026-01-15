from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'supplier'
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'customer'
    
class IsDeliveryPerson(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'delivery_person'