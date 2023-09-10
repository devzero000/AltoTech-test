from django.contrib.auth import get_user_model
from django.db import models

from main.apps.orders.choices import OrderTypes, OrderStatus, OrderProblem
from main.apps.rooms.models import Room


class Order(models.Model):
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders_create'
    )
    assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders_assign'
    )
    memo_number = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
    )
    room = models.ForeignKey(
        Room(),
        on_delete=models.CASCADE,
        related_name='orders_room'
    )
    started_at = models.DateField()
    finished_at = models.DateField()
    order_type = models.CharField(
        max_length=20,
        choices=OrderTypes.choices,
    )
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    remark = models.TextField(
        blank=True,
        null=True
    )
    problem = models.CharField(
        null=True,
        max_length=20,
        choices=OrderProblem.choices,
        default=None
    )
    amenity_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    amenity_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=0
    )

    def __str__(self):
        return f'{self.room} - {self.order_status}'
