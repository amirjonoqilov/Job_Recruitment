from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            return
        
        # Use environment variables or defaults
        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'Admin@123456')
        
        try:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Superuser created!\n'
                    f'  Username: {username}\n'
                    f'  Email: {email}\n'
                    f'  Password: (from SUPERUSER_PASSWORD env var)'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e))}')
