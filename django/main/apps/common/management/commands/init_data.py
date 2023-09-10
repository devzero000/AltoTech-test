from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from main.apps.rooms.models import Room
from main.apps.users.choices import EmployeeGroup
from main.apps.users.models import User


def create_group(name: str):
    group, _ = Group.objects.get_or_create(name=name)


class Command(BaseCommand):
    """Command to initialize data on first run"""
    help = 'Create initial project data'

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        self.clear_sql_log()
        self._create_initial_group()
        self._create_initial_user()
        self._create_initial_room()

    @staticmethod
    def clear_sql_log():
        with open(settings.LOG_PATH, 'w') as log_file:
            log_file.write('')
    @staticmethod
    def _create_initial_user():
        if not User.objects.exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                first_name='admin',
                last_name='admin',
                password='admin'
            )

        list_user = [
            {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'first_name': 'supervisor',
                'last_name': 'supervisor',
                'password': make_password('supervisor'),
                'group': 'supervisor',
            },
            {
                'username': 'maid_supervisor',
                'email': 'maid_supervisor@example.com',
                'first_name': 'maid_supervisor',
                'last_name': 'maid_supervisor',
                'password': make_password('maid_supervisor'),
                'group': 'maid_supervisor',
            },
            {
                'username': 'guest',
                'email': 'guest@example.com',
                'first_name': 'guest',
                'last_name': 'guest',
                'password': make_password('guest'),
                'group': 'guest'
            },
        ]
        for user in list_user:
            role = user.pop('group')
            instance, _ = get_user_model().objects.update_or_create(
                username=user['username'],
                defaults=user
            )
            instance.groups.add(*Group.objects.filter(name=role).values_list('id', flat=True))
            instance.save()
            # Note can use method bulk_create when many user for better performance.
            # I not use method bulk_create because it's test

    @staticmethod
    def _create_initial_group():
        # Create groups
        create_group(name=EmployeeGroup.SUPERVISOR.value)
        create_group(name=EmployeeGroup.MAID_SUPERVISOR.value)
        create_group(name=EmployeeGroup.GUEST.value)

    @staticmethod
    def _create_initial_room():
        # Create rooms
        for i in range(1, 21):
            name = str(i).zfill(3)
            Room.objects.update_or_create(
                name=f'A{name}'
            )
