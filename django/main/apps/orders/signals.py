from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.utils import timezone

from main.apps.common.utils import clean_instance_data
from main.apps.orders.models import Order

LOG_PATH = settings.LOG_PATH


@receiver(post_save, sender=Order)
def order_post_save_handler(sender, instance, created, **kwargs):
    timestamp = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
    action = 'insert' if created else 'update'
    model_name = sender.__name__

    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f"{timestamp} | {action} | {model_name} | {clean_instance_data(instance)}\n")


@receiver(post_delete, sender=Order)
def order_post_delete_handler(sender, instance, **kwargs):
    timestamp = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
    model_name = sender.__name__

    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f"{timestamp} | delete | {model_name} | {clean_instance_data(instance)}\n")
