from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_home, name='prediction_home'),

    path("dashboard/", views.user_dashboard, name="user_dashboard"),

    path(
    "analytics/",
    views.user_analytics,
    name="user_analytics"
    ),

    path(
        'prediction-details/<int:prediction_id>/',
        views.prediction_details,
        name='prediction_details'
    ),

    path(
    "admin-download-prediction-report/<int:prediction_id>/",
    views.admin_download_prediction_report,
    name="admin_download_prediction_report"
    ),

    path(
    "user-details/<int:user_id>/",
    views.user_details,
    name="user_details"
    ),

    path(
    "admin-user-prediction-history/<int:user_id>/",
    views.admin_user_prediction_history,
    name="admin_user_prediction_history"
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