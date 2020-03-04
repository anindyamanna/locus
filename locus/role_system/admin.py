from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Role, Resource, CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("roles", )}),
    )


admin.site.register(Role)
admin.site.register(Resource)
admin.site.register(CustomUser, CustomUserAdmin)
