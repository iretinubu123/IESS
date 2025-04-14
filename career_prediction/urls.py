from django.urls import path
from .views import career_prediction_api

urlpatterns = [
    path("predict-career/", career_prediction_api, name="career_prediction"),
]
