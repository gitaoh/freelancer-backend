from django.utils.translation import gettext_lazy as _
from django.db import models


class AdminCategory(models.TextChoices):
    """
    Allowed categories of users to the server
    """
    USER = 'USER', _('USER')
    ADMIN = 'ADMIN', _('ADMIN')
    MASTER = 'MASTER', _('MASTER')
    __empty__ = 'Unknown'


class AlertChoices(models.TextChoices):
    """ Allowed choices of an alert """
    ACTIVE = 'ACTIVE', _('ACTIVE')  # Live or users/clients are able to view/get informed
    REVIEW = 'REVIEW', _('REVIEW')  # Admins are constricting the alert
    INACTIVE = 'INACTIVE', _('INACTIVE')  # Alert has passed the message
    __empty__ = 'Unknown'


class AlertTypeChoices(models.TextChoices):
    """ Type of an alert """
    INFORMATIVE = 'INFORMATIVE', _('INFORMATIVE')
    UI = 'UI', _('UI')
    __empty__ = 'Unknown'
