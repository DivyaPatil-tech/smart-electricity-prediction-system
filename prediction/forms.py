from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class HouseholdPredictionForm(forms.Form):

    MONTH_CHOICES = [
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    ]

    WEEKEND_CHOICES = [
        (0, "No"),
        (1, "Yes"),
    ]

    Month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="Month",
        help_text="Select the month for which you want to predict electricity consumption."
    )

    Number_of_People = forms.IntegerField(
        min_value=1,
        label="Number of People",
        help_text="Enter the total number of people living in the household."
    )

    Number_of_Rooms = forms.IntegerField(
        min_value=1,
        label="Number of Rooms",
        help_text="Enter the total number of rooms in the household."
    )

    AC_Count = forms.IntegerField(
        min_value=0,
        label="AC Count",
        help_text="Enter the number of air conditioners."
    )

    Fan_Count = forms.IntegerField(
        min_value=0,
        label="Fan Count",
        help_text="Enter the number of fans."
    )

    Refrigerator = forms.IntegerField(
        min_value=0,
        label="Refrigerator",
        help_text="Enter the number of refrigerators."
    )

    Washing_Machine = forms.IntegerField(
        min_value=0,
        label="Washing Machine",
        help_text="Enter the number of washing machines."
    )

    Television_Count = forms.IntegerField(
        min_value=0,
        label="Television Count",
        help_text="Enter the number of televisions."
    )

    Geyser = forms.IntegerField(
        min_value=0,
        label="Geyser",
        help_text="Enter the number of geysers."
    )

    Water_Pump = forms.IntegerField(
        min_value=0,
        label="Water Pump",
        help_text="Enter the number of water pumps."
    )

    Computer_Count = forms.IntegerField(
        min_value=0,
        label="Computer Count",
        help_text="Enter the number of computers."
    )

    Temperature = forms.FloatField(
        label="Temperature (°C)",
        help_text="Enter the average household temperature in degree Celcius."
    )

    Occupancy_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Occupancy Hours per Day",
        help_text="Enter the average number of hours people are present at home per day(0-24)."
    )

    Weekend_Usage = forms.ChoiceField(
        choices=WEEKEND_CHOICES,
        label="Weekend Usage",
        help_text="Select Yes if weekend usage is higher than usual."
    )

    Daily_AC_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Daily AC Usage Hours",
        help_text="Enter average AC usage per day(0-24 hours)."
    )

    Daily_Fan_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Daily Fan Usage Hours",
        help_text="Enter average fan usage per day(0-24 hours)."
    )

    Daily_TV_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Daily TV Usage Hours",
        help_text="Enter average TV usage per day(0-24 hours)."
    )

    Daily_Geyser_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Daily Geyser Usage Hours",
        help_text="Enter average geyser usage per day(0-24 hours)."
    )

    Daily_Washing_Machine_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Daily Washing Machine Usage Hours",
        help_text="Enter average washing machine usage per day(0-24 hours)."
    )

    Average_Daily_Usage_Hours = forms.FloatField(
        min_value=0,
        max_value=24,
        label="Average Daily Usage Hours",
        help_text="Enter the average total household usage hours per day(0-24 hours)."
    )

    Previous_Month_Consumption_kWh = forms.FloatField(
        min_value=0,
        label="Previous Month Consumption (kWh)",
        help_text="Enter the previous month's electricity consumption in kWh."
    )

class UserRegistrationForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=150,
        label="Full Name"
    )

    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        label="Age"
    )

    city = forms.CharField(
        max_length=100,
        label="City"
    )

    state = forms.CharField(
        max_length=100,
        label="State"
    )

    contact_number = forms.CharField(
        max_length=15,
        min_length=10,
        label="Contact Number"
    )

    email = forms.EmailField(
        label="Email Address"
    )

    photo = forms.ImageField(
        required=False,
        label="Profile Photo"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email

    def clean_contact_number(self):
        contact = self.cleaned_data["contact_number"]

        if not contact.isdigit():
            raise forms.ValidationError(
                "Contact number must contain only digits."
            )

        if len(contact) != 10:
            raise forms.ValidationError(
                "Please enter a valid 10-digit contact number."
            )

        return contact
