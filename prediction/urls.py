from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_home, name='prediction_home'),

    path(
        'prediction-details/<int:prediction_id>/',
        views.prediction_details,
        name='prediction_details'
    ),

    path(
    "prediction-history/",
    views.prediction_history,
    name="prediction_history"
    ),

    path(
    "download-report/",
    views.download_prediction_report,
    name="download_prediction_report"
    ),

    path(
    "energy-chatbot/",
    views.energy_chatbot,
    name="energy_chatbot"
    ),
]