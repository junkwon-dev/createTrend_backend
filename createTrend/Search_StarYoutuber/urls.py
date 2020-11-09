from django.urls import path,include
from Search_StarYoutuber import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('channel_list/',views.channel_list),
    path('channel_list/<int:pk>/',views.channel_info),
    path('channel_period_data/<int:pk>/',views.channel_period_data)
]