from django.db import models


class Room(models.Model):
    name = models.CharField(
        max_length=5,
        db_index=True,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'
