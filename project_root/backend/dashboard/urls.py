from django.urls import path
from .views import UserMeView, DashboardView

urlpatterns = [
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
