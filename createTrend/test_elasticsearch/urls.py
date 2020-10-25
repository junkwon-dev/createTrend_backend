from django.urls import path
from test_elasticsearch import views

urlpatterns = [
    path('', views.keyword),
    # path('topKeywords/', views.topKeywords),
    # path('topImaging/', views.topImaging),
]