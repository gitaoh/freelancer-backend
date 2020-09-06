from django.contrib import admin
from .models import (
    PaperType,
    Discipline,
)

# Register your models here.
admin.site.register(PaperType)
admin.site.register(Discipline)
