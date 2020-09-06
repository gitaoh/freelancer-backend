from django.contrib import admin
from .models import (
    Files,
    Order,
    Message,
    Writer
)

# Register your models here.
admin.site.register(Files)
admin.site.register(Message)
admin.site.register(Order)
admin.site.register(Writer)
