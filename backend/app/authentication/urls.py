
from app.authentication.views.password_reset_views import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns += [
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
