from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserConfirm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'phone_number', 'is_active', 'is_staff']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ['email', 'phone_number']


@admin.register(UserConfirm)
class UserConfirmAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_confirmed']
