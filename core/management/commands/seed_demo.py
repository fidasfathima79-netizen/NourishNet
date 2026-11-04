from django.core.management.base import BaseCommand

from core.models import User


DEMO_ACCOUNTS = [
    # username, password, role, is_superuser/is_staff
    ('admin', 'Admin@12345', 'ADMIN', True),
    ('demo_donor', 'Donor@12345', 'DONOR', False),
    ('demo_ngo', 'Ngo@12345', 'NGO', False),
]


class Command(BaseCommand):
    help = 'Create (or reset) the demo Admin, Donor and NGO accounts.'

    def handle(self, *args, **options):
        for username, password, role, is_admin in DEMO_ACCOUNTS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'},
            )
            user.role = role
            user.is_superuser = is_admin
            user.is_staff = is_admin
            user.is_active = True
            user.set_password(password)
            user.save()
            state = 'created' if created else 'reset'
            self.stdout.write(self.style.SUCCESS(
                f'{state}: {username} ({role})'
            ))
