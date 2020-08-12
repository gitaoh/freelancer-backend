from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator


class MinimalModel(models.Model):
    uuid = models.UUIDField(_('uuid'), max_length=32, null=True, blank=True,
                            unique=True,
                            validators=[MaxLengthValidator, MinLengthValidator],
                            help_text="uuid is required")
    createdAt = models.DateTimeField(_('createdAt'), auto_now_add=True)
    deletedAt = models.DateTimeField(_('deletedAt'), null=True, blank=True)
    updateAt = models.DateTimeField(_('updateAt'), auto_now=True)

    class Meta:
        abstract = True
