from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('dashboard.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('governance.urls')),
]
