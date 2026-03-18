from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'message', 'timestamp')
    list_filter = ('timestamp', 'sender', 'recipient')
    search_fields = ('message', 'sender__username', 'recipient__username')
    readonly_fields = ('timestamp',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True
