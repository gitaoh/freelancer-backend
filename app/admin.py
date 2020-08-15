from django.contrib import admin
from .models import (
    PaperType,
    Discipline,
    Rating,
)

# Register your models here.
admin.site.register(PaperType)
admin.site.register(Discipline)
admin.site.register(Rating)
