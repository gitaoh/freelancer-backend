from django.contrib import admin
from .models import (
    OrderFiles,
    Order,
    Notification
)

# Register your models here.
admin.site.register(OrderFiles)
admin.site.register(Notification)
admin.site.register(Order)
