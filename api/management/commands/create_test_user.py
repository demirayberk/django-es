from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.settings import MOCK_USERNAME, MOCK_PASSWORD

class Command(BaseCommand):
    help = "Creates a test user if it doesn't exist"

    def handle(self, *args, **kwargs): # pyright: ignore
        username = MOCK_USERNAME
        password = MOCK_PASSWORD

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))

