from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import LoginAPIView, RegistrationAPIView, CurrentUserRetrieveUpdateAPIView


app_name = "account"
urlpatterns = [
    path("registration", RegistrationAPIView.as_view(), name="registration"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", CurrentUserRetrieveUpdateAPIView.as_view(), name="current_user_retrieve_update"),
]
