"""Authentication URL configuration."""
from django.urls import path
from .views import RegisterView, LoginView, PasswordResetRequestView, PasswordResetConfirmView, UserProfileView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/password-reset/request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/me', UserProfileView.as_view(), name='user_profile'),
]
