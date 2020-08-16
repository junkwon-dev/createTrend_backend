from django.urls import path,include
from Search_StarYoutuber import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('channel_list/',views.channellist),
    path('channel_list/<int:pk>/',views.channelinfo),
    path('channel_period_data/<int:pk>/',views.channelperioddata)
    # path('topkeywords/', views.top),
    # path('topImaging/', views.topImaging),
]