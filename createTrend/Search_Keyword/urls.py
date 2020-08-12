from django.urls import path
from Search_Keyword import views

urlpatterns = [
    path('channellist/', views.channellist),
    # path('topKeywords/', views.topKeywords),
    # path('topImaging/', views.topImaging),
]