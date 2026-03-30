from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'Admin@123456')
        
        # Delete existing if needed
        User.objects.filter(username=username).delete()
        
        # Create new
        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Superuser created: {username}')
        )
