from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

@receiver(post_save, sender=User)
def assign_permissions_by_role(sender, instance, created, **kwargs):
    """
    Automatically assign user to groups and permissions based on role
    """
    user = instance
    
    # Flag to prevent recursion
    if hasattr(user, '_updating_permissions'):
        return
    
    user._updating_permissions = True
    
    try:
        # Remove all existing groups
        user.groups.clear()
        
        # Track if we need to save
        needs_save = False
        
        # Assign groups based on role
        if user.role == 'admin':
            # Admin has all permissions, so we just make sure they're staff
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                needs_save = True
        
        elif user.role == 'supplier':
            # Supplier group
            supplier_group, _ = Group.objects.get_or_create(name='Supplier')
            user.groups.add(supplier_group)
            if user.is_staff:
                user.is_staff = False
                needs_save = True
        
        elif user.role == 'customer':
            # Customer group
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            user.groups.add(customer_group)
            if user.is_staff:
                user.is_staff = False
                needs_save = True
        
        elif user.role in ['delivery', 'delivery_person']:
            # Delivery Personnel group
            delivery_group, _ = Group.objects.get_or_create(name='DeliveryPersonnel')
            user.groups.add(delivery_group)
            if user.is_staff:
                user.is_staff = False
                needs_save = True
        
        # Only save if needed
        if needs_save:
            User.objects.filter(pk=user.pk).update(
                is_staff=user.is_staff,
                is_superuser=user.is_superuser
            )
    
    finally:
        delattr(user, '_updating_permissions')

