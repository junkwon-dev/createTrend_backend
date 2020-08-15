from django.urls import path
from Analyze_Channel import views

urlpatterns = [
    path('', views.analyze_channel),
    # path('topKeywords/', views.topKeywords),
    # path('topImaging/', views.topImaging),
]