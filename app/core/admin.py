from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import User, Blog, Category


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'special', 'status', 'visits')
    search_fields = ('title', 'author__first_name', 'category__title')
    list_filter = ('status', 'special', 'publish')
    prepopulated_fields = {'slug': ('title',), }
    exclude = ('slug',)
    filter_horizontal = ('category', 'likes')
    radio_fields = {'status': admin.HORIZONTAL}
    list_per_page = 30


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent', 'status')
    search_fields = ('title', 'slug', 'status')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',), }
    list_per_page = 30
