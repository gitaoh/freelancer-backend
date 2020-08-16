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
