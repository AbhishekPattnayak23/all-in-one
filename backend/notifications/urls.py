from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReceiveNotificationsViewSet

router = DefaultRouter()
router.register('', ReceiveNotificationsViewSet, basename='receive_notifications')

urlpatterns = [
    path('', include(router.urls)),
]
