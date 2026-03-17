from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    MeAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]
