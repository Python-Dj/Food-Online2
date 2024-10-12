from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile



class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "firstName", "lastName", "role", "is_active", "is_staff"]
    ordering = ["-date_joined"]
    filter_horizontal = ()
    list_filter = []
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
