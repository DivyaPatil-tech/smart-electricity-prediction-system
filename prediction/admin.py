from django.contrib import admin
from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):

    # Fields shown in the main Admin table
    list_display = (
        "username",
        "month",
        "number_of_people",
        "number_of_rooms",
        "ac_count",
        "temperature",
        "occupancy_hours",
        "previous_month_consumption_kwh",
        "season",
        "cooling_degree",
        "predicted_consumption_kwh",
        "predicted_bill",
        "created_at",
    )

    # Search box
    search_fields = (
        "username",
        "month",
        "season",
    )

    # Filters on right side
    list_filter = (
        "month",
        "season",
        "created_at",
    )

    # Newest records first
    ordering = (
        "-created_at",
    )

