from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from todolistapi.settings.base import ADMIN


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = ADMIN.get('username', 'admin')
            email = ADMIN.get('email', 'admin@yourmail.com')
            password = ADMIN.get('password', 'admin')
            print(f'Creating account for {username} ({email})')
            admin = User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
