from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cart.models import Cart

class Command(BaseCommand):
    help = 'Create default carts for all users'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            # Create default carts if they don't exist
            cart1, created1 = Cart.objects.get_or_create(name='Cart 1', user=user)
            cart2, created2 = Cart.objects.get_or_create(name='Cart 2', user=user)
            cart3, created3 = Cart.objects.get_or_create(name='Cart 3', user=user)
            
            if created1 or created2 or created3:
                created_count += 1
                self.stdout.write(f'Created default carts for user: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default carts for {created_count} users')
        )
