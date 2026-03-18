from django.urls import path
from ..views.notification_views import receive_notifications

app_name = "notifications"

urlpatterns = [
    path("receive_notifications/", receive_notifications, name="receive_notifications"),
]
