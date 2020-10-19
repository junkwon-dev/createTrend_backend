from django.urls import path,include
from Video_Predict import views


urlpatterns = [
    path('/',views.videoPredict)
]