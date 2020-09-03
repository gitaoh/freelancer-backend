from django.contrib import admin
from .models import (
    Avatar,
    User,
    Defaults,
    Rating
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'createdAt')


admin.site.register(Avatar)
admin.site.register(Defaults)
admin.site.register(Rating)
