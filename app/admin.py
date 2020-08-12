from django.contrib import admin
from .models import (
    PaperType,
    Order,
    Discipline,
    Notification,
    OrderFiles
)

# Register your models here.
admin.site.register(OrderFiles)
admin.site.register(Notification)
admin.site.register(Order)
admin.site.register(PaperType)
admin.site.register(Discipline)
