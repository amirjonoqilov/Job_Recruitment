from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            return
        
        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'admin123')
        
        User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
