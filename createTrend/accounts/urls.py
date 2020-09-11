from django.urls import path, include
from django.conf.urls import url
from .views import RegistrationAPI, LoginAPI, UserAPI, UserInfoAPI

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
    path("auth/profile/",UserInfoAPI.as_view()),
    url(r'^auth/profile/(?P<pk>\d+)/$',UserInfoAPI.as_view()),
]