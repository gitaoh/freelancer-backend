from django.contrib import admin
from .models import (
    Files,
    Order,
    Notification,
    Writer
)

# Register your models here.
admin.site.register(Files)
admin.site.register(Notification)
admin.site.register(Order)
admin.site.register(Writer)
