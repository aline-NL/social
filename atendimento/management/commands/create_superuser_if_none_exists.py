from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exists.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Superuser username')
        parser.add_argument('--email', type=str, help='Superuser email')
        parser.add_argument('--password', type=str, help='Superuser password')

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')

        if not all([username, email, password]):
            self.stdout.write(
                self.style.WARNING('Username, email, and password are required to create a superuser.')
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists.')
            )
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
