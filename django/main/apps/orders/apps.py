from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'main.apps.orders'
    verbose_name = _('Order')

    def ready(self):
        import main.apps.orders.signals  # noqa: F401
        