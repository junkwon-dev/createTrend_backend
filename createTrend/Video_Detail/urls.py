from django.urls import path,include
from Video_Detail import views


urlpatterns = [
    path('<int:pk>/',views.videoDetail)
    # path('topkeywords/', views.top),
    # path('topImaging/', views.topImaging),
]