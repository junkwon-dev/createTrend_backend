from django.urls import path,include
from Search_StarYoutuber import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('channellist/',views.channellist),
    # path('topkeywords/', views.top),
    # path('topImaging/', views.topImaging),
]