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


class StatusChoices(models.TextChoices):
    DRAFT = 'DRAFT', _('DRAFT')  # Order created by user by not submitted
    REVISION = 'REVISION', _('REVISION')  # Orders on revision
    ACTIVE = 'ACTIVE', _('ACTIVE')  # Order recently created and paid for.
    FINISHED = 'FINISHED', _('FINISHED')  # Orders successfully finished/worded on
    CANCELED = 'CANCELED', _('CANCELED')  # Orders canceled by user/Admin
    DISPUTE = 'DISPUTE', _('DISPUTE')  # Orders disputed by user/client


class NotificationChoices(models.TextChoices):
    UPDATE = 'UPDATE', _('UPDATE')
    NOTIFICATION = 'NOTIFICATION', _('NOTIFICATION')


class EducationLevelChoices(models.TextChoices):
    HIGHSCHOOL = 'HIGHSCHOOL', _('HIGHSCHOOL')
    PHD = 'PHD', _('PHD')
    GRADUATE = 'GRADUATE', _('GRADUATE')
    UNDERGRADUATE_1_2 = 'UNDERGRADUATE_1_2', _('UNDERGRADUATE_1_2')
    UNDERGRADUATE_3_4 = 'UNDERGRADUATE_3_4', _('UNDERGRADUATE_3_4')
