from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserAccount


class UserAccountAdmin(admin.ModelAdmin):
    # inlines = [TgToken, ]
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'tg_token')
    list_display_links = ('id', 'email', 'first_name', 'last_name',)
    list_editable = ('is_active', 'is_staff', 'tg_token')
    ordering = ['id']


# admin.site.register(UserAccount)
admin.site.register(UserAccount, UserAccountAdmin)
