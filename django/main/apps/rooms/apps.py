from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RoomsConfig(AppConfig):
    name = 'main.apps.rooms'
    verbose_name = _('Room')

    def ready(self):
        import main.apps.rooms.signals  # noqa: F401
        