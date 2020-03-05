from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from role_system.models import ActionResourcePair
from .models import Role, Resource, CustomUser, Action


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("roles", )}),
    )


admin.site.register(Action)
admin.site.register(ActionResourcePair)
admin.site.register(Role)
admin.site.register(Resource)
admin.site.register(CustomUser, CustomUserAdmin)
