from django.urls import path

from authentication.views.login_view import LoginView

urlpatterns = [
    path("login", LoginView.as_view(), name="auth_login"),
]
