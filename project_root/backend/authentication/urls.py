from django.urls import path
from .views import RegisterView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('password-reset/request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
