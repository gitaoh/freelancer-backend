from django.db import models
from django.utils.translation import gettext_lazy as _


class FormatChoices(models.TextChoices):
    """
    Accepted Paper Format
    """
    MLA = 'MLA', _('MLA')
    CHICAGO = 'CHICAGO/TURABIAN', _('CHICAGO/TURABIAN')
    APA7 = 'APA7', _('APA7')
    APA6 = 'APA6', _('APA6')
    __empty__ = _('Unknown')


class SpacingChoices(models.TextChoices):
    """
    Accepted spacing
    """
    SINGLE = 'SINGLE', _('SINGLE')
    DOUBLE = 'DOUBLE', _('DOUBLE')
    __empty__ = _('Unknown')


class StatusChoices(models.TextChoices):
    """
    Type of Different states of an order
    """
    ACTIVE = 'ACTIVE', _('ACTIVE')  # Order recently created and paid for.
    DRAFT = 'DRAFT', _('DRAFT')  # Order created by user by not submitted
    REVISION = 'REVISION', _('REVISION')  # Orders on revision
    FINISHED = 'FINISHED', _('FINISHED')  # Orders successfully finished/worded on
    CANCELED = 'CANCELED', _('CANCELED')  # Orders canceled by user/Admin
    DISPUTE = 'DISPUTE', _('DISPUTE')  # Orders disputed by user/client
    __empty__ = _('Unknown')


class NotificationChoices(models.TextChoices):
    """
    Type of a notification
    """
    ToSUPPORT = 'ToSUPPORT', _('ToSUPPORT')  # writer writes to support
    ToWRITER = 'ToWRITER', _('ToWRITER')  # writer writes to writer
    SUPPORT = 'SUPPORT', _('SUPPORT')  # Admin writes as support
    WRITER = 'WRITER', _('WRITER')  # Admin writes as Writer
    __empty__ = _('Unknown')


class EducationLevelChoices(models.TextChoices):
    """
    Accept education level choices
    """
    HIGHSCHOOL = 'HIGHSCHOOL', _('HIGHSCHOOL')
    PHD = 'PHD', _('PHD')
    GRADUATE = 'GRADUATE', _('GRADUATE')
    UNDERGRADUATE_1_2 = 'UNDERGRADUATE_1_2', _('UNDERGRADUATE_1_2')
    UNDERGRADUATE_3_4 = 'UNDERGRADUATE_3_4', _('UNDERGRADUATE_3_4')
    __empty__ = _('Unknown')


class SchoolChoices(models.TextChoices):
    ALL = 'ALL', _('ALL')
    HIGHSCHOOL = 'HIGHSCHOOL', _('HIGHSCHOOL')
    PHD = 'PHD', _('PHD')
    GRADUATE = 'GRADUATE', _('GRADUATE')
    UNDERGRADUATE_1_2 = 'UNDERGRADUATE_1_2', _('UNDERGRADUATE_1_2')
    UNDERGRADUATE_3_4 = 'UNDERGRADUATE_3_4', _('UNDERGRADUATE_3_4')
    __empty__ = _('Unknown')


class PreferencesChoices(models.TextChoices):
    """
    Choice for writer preference
    """
    STANDARD = 'STANDARD', _('STANDARD')
    TOP5 = 'TOP5', _('TOP5')
    EXPERT = 'EXPERT', _('EXPERT')
    __empty__ = _('Unknown')


class FileLabelChoices(models.TextChoices):
    FINAL = 'FINAL', _('FINAL')
    DRAFT = 'DRAFT', _('DRAFT')
    FILE = 'FILE', _('FILE')
    __empty__ = _('Unknown')
