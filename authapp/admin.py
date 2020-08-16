from django.contrib import admin
from .models import (
    Avatar,
    User,
    Defaults,
)

admin.site.register(Avatar)
admin.site.register(User)
admin.site.register(Defaults)
