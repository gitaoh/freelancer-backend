from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator


class MinimalModel(models.Model):
    uuid = models.UUIDField(_('uuid'), max_length=32, null=False, unique=True,
                            validators=[MaxLengthValidator, MinLengthValidator], help_text="uuid is required")
    createdAt = models.DateTimeField(_('createdAt'), auto_now_add=True)
    deletedAt = models.DateTimeField(_('deletedAt'), null=True)
    updatedAt = models.DateTimeField(_('updatedAt'), auto_now=True)

    class Meta:
        abstract = True
