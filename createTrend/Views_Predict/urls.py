from django.urls import path,include
from Views_Predict import views


urlpatterns = [
    path('',views.videoViewsPredict),
    path('advanced_recommendation',views.advanced_recommendation),
    path('simple_recommendation',views.simple_recommendation),
]