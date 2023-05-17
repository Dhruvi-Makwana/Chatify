from django.contrib import admin
from .models import User, Group, Chat

admin.site.register(Group)
admin.site.register(Chat)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "profile_photo")
