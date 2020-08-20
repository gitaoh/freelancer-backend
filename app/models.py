from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from app.abstract import MinimalModel
from django.utils.timezone import now


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Discipline(MinimalModel):
    """
    Register a new discipline
    """
    admin = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', null=False,
                              on_delete=models.PROTECT, limit_choices_to={'user_type': 'MASTER', 'is_active': True})
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name

    def trash(self):
        self.is_active = False
        self.deletedAt = now()
        self.save()
        return

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _("Disciplines")
        db_table = "Discipline"


class PaperType(MinimalModel):
    """
    Register a paper type
    """
    admin = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', null=False,
                              on_delete=models.PROTECT, limit_choices_to={'user_type': 'MASTER', 'is_active': True})
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def trash(self):
        self.is_active = False
        self.deletedAt = now()
        self.save()
        return

    class Meta:
        verbose_name = _('PaperType')
        verbose_name_plural = _("PaperTypes")
        db_table = "PaperType"

