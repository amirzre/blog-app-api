from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('is_superuser', 'is_staff', 'id')
    list_display = (
        'phone', 'first_name', 'last_name', 'is_staff', 'author',
        'is_special_user',
    )
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('first_name', 'last_name', 'phone')
    fieldsets = (
        (None, {'fields': ('phone',)}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {'fields': (
                'is_active', 'is_staff', 'is_superuser', 'author',
                'two_step_password')}
        ),
        (_('Important Dates'), {'fields': (
            'date_joined', 'last_login', 'special_user',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name')
        })
    )
