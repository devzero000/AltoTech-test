from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderTypes(models.TextChoices):
    """
    Order Types
    """
    CLEANING = 'cleaning', _('Cleaning'),
    MAID_REQUEST = 'maid_request', _('Maid Request'),
    TECHNICIAN_REQUEST = 'technician_request', _('Technician Request')
    AMENITY_REQUEST = 'amenity_request', _('Amenity Request')


class OrderStatus(models.TextChoices):
    """
    Order Status
    """
    CREATED = 'created', _('Created'),
    ASSIGNED = 'assigned', _('Assigned'),
    IN_PROGRESS = 'in_progress', _('In Progress')
    DONE = 'done', _('Done')
    CANCEL = 'cancel', _('Cancel')
    CANCEL_BY_GUEST = 'cancel_by_guest', _('Cancel By Guest')


class OrderProblem(models.TextChoices):
    """
    Order Problem
    """
    ELECTRICITY = 'electricity', _('Electricity')
    AIR_CONDITIONING = 'air_conditioning', _('Air Conditioning')
    PLUMBING = 'plumbing', _('Plumbing')
    INTERNET = 'internet', _('Internet')
