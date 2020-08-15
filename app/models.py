from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from app.abstract import MinimalModel
from django.conf import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Discipline(MinimalModel):
    """
    Register a new discipline
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _("Disciplines")
        db_table = "Discipline"


class PaperType(MinimalModel):
    """
    Register a paper type
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('PaperType')
        verbose_name_plural = _("PaperTypes")
        db_table = "PaperType"


class Rating(MinimalModel):
    """
    Custom rating from the user when they delete their account
    """
    rate = models.PositiveIntegerField()
    client = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', on_delete=models.SET_DEFAULT,
                               default='deleted')

    def __str__(self):
        return f"{self.rate}{self.client}"

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        db_table = 'Rating'
