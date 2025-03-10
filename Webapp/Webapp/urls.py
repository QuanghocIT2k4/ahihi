from django.urls import path
from ImageApp.views.client_views import (
    ClientRegisterUserAPIView,
    ClientLoginUserAPIView,
    ClientResetPasswordAPIView
)

urlpatterns = [
    path('client/api/register/', ClientRegisterUserAPIView.as_view(), name='client-register'),
    path('client/api/login/', ClientLoginUserAPIView.as_view(), name='client-login'),
    path('client/api/reset-password/', ClientResetPasswordAPIView.as_view(), name='reset-password'),
]
