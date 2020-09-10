from django.urls import path, include
from .views import RegistrationAPI, LoginAPI, UserAPI, UserInfoAPI

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
    path("auth/profile/",UserInfoAPI.as_view()),
]