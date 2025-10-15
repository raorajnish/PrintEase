from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **options):
        User = get_user_model()

        # Get credentials from environment variables or use defaults
        username = os.environ.get('SUPERUSER_USERNAME', 'admin1')
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@super20.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')

        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            return

        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            # Ensure flags for custom user models
            if not user.is_staff:
                user.is_staff = True
            if not user.is_superuser:
                user.is_superuser = True
            # Optional flags if present on custom model
            if hasattr(user, 'is_admin') and not getattr(user, 'is_admin', False):
                user.is_admin = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
