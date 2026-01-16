from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Update user role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to update')
        parser.add_argument('role', type=str, help='New role (admin, customer, supplier, delivery)')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        valid_roles = ['admin', 'customer', 'supplier', 'delivery', 'delivery_person']
        
        if role not in valid_roles:
            self.stdout.write(self.style.ERROR(f'Invalid role. Must be one of: {", ".join(valid_roles)}'))
            return
        
        try:
            user = User.objects.get(username=username)
            user.role = role
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {username} role to {role}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))
