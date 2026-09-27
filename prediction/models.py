from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=150
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.user.username

class PredictionRecord(models.Model):

    # User information
    username = models.CharField(max_length=150)

    # Input features
    month = models.CharField(max_length=20)
    month_number = models.IntegerField()

    number_of_people = models.IntegerField()
    number_of_rooms = models.IntegerField()

    ac_count = models.IntegerField()
    fan_count = models.IntegerField()
    refrigerator = models.IntegerField()
    washing_machine = models.IntegerField()
    television_count = models.IntegerField()
    geyser = models.IntegerField()
    water_pump = models.IntegerField()
    computer_count = models.IntegerField()

    temperature = models.FloatField()
    occupancy_hours = models.FloatField()
    weekend_usage = models.IntegerField()

    daily_ac_hours = models.FloatField()
    daily_fan_hours = models.FloatField()
    daily_tv_hours = models.FloatField()
    daily_geyser_hours = models.FloatField()
    daily_washing_machine_hours = models.FloatField()

    average_daily_usage_hours = models.FloatField()
    previous_month_consumption_kwh = models.FloatField()

    season = models.CharField(max_length=30)
    cooling_degree = models.FloatField()

    # Prediction results
    predicted_consumption_kwh = models.FloatField()
    predicted_bill = models.FloatField()

    # Date and time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.predicted_consumption_kwh} kWh"
