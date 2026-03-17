from django.urls import path
from . import views

urlpatterns = []
urlpatterns += [path('login/', LoginAPIView.as_view(), name='login')]
