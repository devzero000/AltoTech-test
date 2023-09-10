from django.db import models


class EmployeeGroup(models.TextChoices):
    """ Employee Groups (Role)"""
    # syntax: VALUE, LABEL
    SUPERVISOR = 'supervisor', 'Supervisor'
    MAID_SUPERVISOR = 'maid_supervisor', 'Maid Supervisor'
    GUEST = 'guest', 'Guest'
