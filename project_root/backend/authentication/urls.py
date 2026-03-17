from django.urls import path, include
from . import views

urlpatterns = [
    path('api/auth/register', views.register, name='register'),
    path('api/auth/login', views.login, name='login'),
    path('api/auth/password-reset/request', views.password_reset_request, name='password-reset-request'),
    path('api/auth/password-reset/confirm/<str:token>', views.password_reset_confirm, name='password-reset-confirm'),
    path('api/user/me', views.user_me, name='user-me'),
]
