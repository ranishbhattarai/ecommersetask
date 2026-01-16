from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign groups to all users based on their roles'

    def handle(self, *args, **options):
        # Get or create groups
        supplier_group, _ = Group.objects.get_or_create(name='Supplier')
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        delivery_group, _ = Group.objects.get_or_create(name='DeliveryPersonnel')
        
        self.stdout.write(self.style.SUCCESS('Groups created/verified'))
        
        # Update all users
        for user in User.objects.all():
            user.groups.clear()
            
            if user.role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                self.stdout.write(f'{user.username} -> Admin (Staff + Superuser)')
            
            elif user.role == 'supplier':
                user.groups.add(supplier_group)
                user.is_staff = False
                self.stdout.write(f'{user.username} -> Supplier Group')
            
            elif user.role == 'customer':
                user.groups.add(customer_group)
                user.is_staff = False
                self.stdout.write(f'{user.username} -> Customer Group')
            
            elif user.role in ['delivery', 'delivery_person']:
                user.groups.add(delivery_group)
                user.is_staff = False
                self.stdout.write(f'{user.username} -> Delivery Personnel Group')
            
            user.save()
        
        self.stdout.write(self.style.SUCCESS('All users have been assigned to appropriate groups'))
