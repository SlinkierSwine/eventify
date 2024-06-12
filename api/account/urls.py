from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import LoginAPIView, RegistrationAPIView


app_name = "authentication"
urlpatterns = [
    path("registration", RegistrationAPIView.as_view(), name="registration"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
