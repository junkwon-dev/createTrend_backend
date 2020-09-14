from django.urls import path, include
from django.conf.urls import url
from .views import RegistrationAPI, LoginAPI, UserAPI, UserInfoUpdateAPI

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
    path('auth/userinfo/update/', UserInfoUpdateAPI.as_view()),
]