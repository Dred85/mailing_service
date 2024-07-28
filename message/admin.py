from django.contrib import admin

from message.models import Message


@admin.register(Message)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    list_filter = ('subject', 'text',)
