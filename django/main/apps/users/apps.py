from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'main.apps.users'

    def ready(self):
        import main.apps.users.signals  # noqa: F401
