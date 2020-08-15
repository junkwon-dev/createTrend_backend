from django.urls import path
from Search_Keyword import views

urlpatterns = [
    path('', views.analyze_channel),
    # path('topKeywords/', views.topKeywords),
    # path('topImaging/', views.topImaging),
]