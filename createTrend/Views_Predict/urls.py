from django.urls import path,include
from Views_Predict import views


urlpatterns = [
    path('',views.videoViewsPredict)
]