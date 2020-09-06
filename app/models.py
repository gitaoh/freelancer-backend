from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from app.abstract import MinimalModel
from order.choices import EducationLevelChoices, SchoolChoices
from django.utils.timezone import now
from .choices import AlertChoices, AlertTypeChoices, AdminCategory


class CommonDP(MinimalModel):
    admin = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', null=False,
                              on_delete=models.PROTECT,
                              limit_choices_to={'user_type': AdminCategory.MASTER, 'is_active': True})
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.CharField(max_length=10, null=False, default=0)
    # Conversion is handled by the frontend
    level = models.CharField(max_length=20, null=False, default=SchoolChoices.HIGHSCHOOL,
                             choices=SchoolChoices.choices)
    is_active = models.BooleanField(default=True, null=False)
    valid = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name

    def trash(self):
        self.is_active = False
        self.deletedAt = now()
        self.save()
        return

    def verify(self):
        self.valid = True
        self.save()

    def is_invalid(self):
        self.valid = False
        self.save()

    class Meta:
        abstract = True


class Discipline(CommonDP):
    """
    Register a new discipline
    """

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _("Disciplines")
        db_table = "Discipline"
        ordering = ('-createdAt',)


class PaperType(CommonDP):
    """
    Register a paper type
    """

    class Meta:
        verbose_name = _('PaperType')
        verbose_name_plural = _("PaperTypes")
        db_table = "PaperType"
        ordering = ('-createdAt',)


# Notify the user's for general updated
class Alert(MinimalModel):
    """
    Alert user/Clients for any changes on the platform eg increase in price, UI update
    TODO Alert Image will be on the frontend and will load depending on alert type
    """
    admin = models.ForeignKey(to_field='username', null=False, to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                              limit_choices_to={'user_type': 'MASTER', 'is_active': True, 'is_staff': True,
                                                'is_superuser': True}, help_text=_('Admin creating the alert.'),
                              related_name='admin')

    title = models.CharField(max_length=30, null=False, help_text=_('Title of the Alert.'), unique=True)
    description = models.TextField(help_text=_('Description for the Alert.'))
    status = models.CharField(max_length=10, null=False, choices=AlertChoices.choices, default=AlertChoices.REVIEW,
                              help_text=_('Status of the Alert.'))
    _type = models.CharField(max_length=12, choices=AlertTypeChoices.choices, default=AlertTypeChoices.INFORMATIVE,
                             null=False, help_text=_('Type of the alert being created.'))
    _from = models.DateTimeField(null=False, auto_now_add=True, help_text=_('Active from.'))
    to = models.DateTimeField(null=False, help_text=_('Active until.'), auto_now=True)
    is_active = models.BooleanField(default=True, help_text=_('Deleted or active.'))
    deleted_by = models.ForeignKey(to_field='username', null=True, to=settings.AUTH_USER_MODEL,
                                   related_name='deleted_by', help_text=_('Admin deleting the alert.'),
                                   on_delete=models.PROTECT, limit_choices_to={'user_type': 'MASTER', 'is_active': True,
                                                                               'is_staff': True, 'is_superuser': True})

    def __str__(self):
        return self.title

    def trash(self):
        self.is_active = False
        self.deletedAt = now()
        self.save()

    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        db_table = 'Alert'
        ordering = ('-createdAt',)
