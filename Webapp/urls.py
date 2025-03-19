from django.urls import path
from ImageApp.views.client_views import (
    ClientRegisterUserAPIView,
    ClientLoginUserAPIView,
    ClientResetPasswordAPIView,
    ClientViewUserInfoAPIView,
    ClientChangePasswordAPIView,
)

urlpatterns = [
    path('client/api/register/', ClientRegisterUserAPIView.as_view(), name='client-register'),
    path('client/api/login/', ClientLoginUserAPIView.as_view(), name='client-login'),
    path('client/api/reset-password/', ClientResetPasswordAPIView.as_view(), name='reset-password'),
    path('client/api/view-user-info/', ClientViewUserInfoAPIView.as_view(), name='view-user-info'),
    path('client/api/change-password/', ClientChangePasswordAPIView.as_view(), name='change-password'),
]
