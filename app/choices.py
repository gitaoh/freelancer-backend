from django.utils.translation import gettext_lazy as _
from django.db import models


class AdminCategory(models.TextChoices):
    USER = 'USER', _('USER')
    ADMIN = 'ADMIN', _('ADMIN')
    MASTER = 'MASTER', _('MASTER')


class FormatChoices(models.TextChoices):
    MLA = 'MLA', _('MLA')
    CHICAGO = 'CHICAGO/TURABIAN', _('CHICAGO/TURABIAN')
    APA7 = 'APA7', _('APA7')
    APA6 = 'APA6', _('APA6')


class SpacingChoices(models.TextChoices):
    SINGLE = 'SINGLE', _('SINGLE')
    DOUBLE = 'DOUBLE', _('DOUBLE')


class PreferencesChoices(models.TextChoices):
    BEST = 'BEST AVAILABLE', _('BEST AVAILABLE')
    ADVANCED = 'ADVANCED', _('ADVANCED')
    TOP10 = 'TOP10', _('TOP10')
    TOP25 = 'TOP25', _('TOP25')


class NotificationChoices(models.TextChoices):
    UPDATE = 'UPDATE', _('UPDATE')
    NOTIFICATION = 'NOTIFICATION', _('NOTIFICATION')
