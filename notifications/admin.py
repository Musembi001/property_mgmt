from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'message', 'created_at', 'is_read', 'sent')
    list_filter = ('channel', 'is_read', 'sent')
    search_fields = ('user__username', 'message')
