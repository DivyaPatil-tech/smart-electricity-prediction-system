from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Count

from .forms import HouseholdPredictionForm, UserRegistrationForm
from .prediction_service import predict_household_bill
from .models import PredictionRecord, UserProfile
from .recommendations import generate_recommendations, get_top_energy_factors

from django.http import HttpResponse
from .pdf_report import generate_prediction_report

from django.http import JsonResponse
from .chatbot import get_energy_chatbot_response

def assign_season(month):

    if month in ["January", "February"]:
        return "Winter"

    elif month in ["March", "April", "May"]:
        return "Summer"

    elif month in ["June", "July", "August", "September"]:
        return "Monsoon"

    else:
        return "Post-Monsoon"

def register_view(request):

    if request.method == "POST":

        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():

            # Create Django User
            user = form.save(commit=False)

            user.email = form.cleaned_data["email"]

            user.save()

            # Create UserProfile
            UserProfile.objects.create(

                user=user,

                full_name=form.cleaned_data["full_name"],

                age=form.cleaned_data["age"],

                city=form.cleaned_data["city"],

                state=form.cleaned_data["state"],

                contact_number=form.cleaned_data["contact_number"],

                photo=form.cleaned_data.get("photo")
            )

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect("/login/")

    else:

        form = UserRegistrationForm()

    return render(
        request,
        "prediction/register.html",
        {
            "form": form
        }
    )

def logout_view(request):

    logout(request)

    return redirect("/login/")

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/prediction/")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "prediction/login.html"
    )

@ login_required 
@never_cache
def prediction_home(request):

    prediction = None
    estimated_bill = None
    recommendations=[]
    consumption_level= None
    top_energy_factors=[]

    if request.method == "POST":

        form = HouseholdPredictionForm(request.POST)

        if form.is_valid():

            # -----------------------------------------
            # 1. Get validated form data
            # -----------------------------------------
            input_data = form.cleaned_data.copy()


            # -----------------------------------------
            # 2. Calculate Month Number
            # -----------------------------------------
            month_numbers = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }

            month_number = month_numbers[
                input_data["Month"]
            ]

            input_data["Month_Number"] = month_number


            # -----------------------------------------
            # 3. Calculate Season
            # -----------------------------------------
            season = assign_season(
                input_data["Month"]
            )

            input_data["Season"] = season


            # -----------------------------------------
            # 4. Calculate Cooling Degree
            # -----------------------------------------
            cooling_degree = max(
                input_data["Temperature"] - 27,
                0
            )

            input_data["Cooling_Degree"] = cooling_degree


            # -----------------------------------------
            # 5. ML Prediction
            # -----------------------------------------
            prediction, estimated_bill = predict_household_bill(
                input_data
            )

            # Convert prediction results to numbers
            prediction = float(prediction)
            estimated_bill = float(estimated_bill)

            # -----------------------------------------
            # 5B. Consumption Level Indicator
            # -----------------------------------------

            if prediction < 300:
                consumption_level = "Low"
            elif prediction <= 600:
                consumption_level = "Moderate"
            else:
                consumption_level = "High"
    

            # -----------------------------------------
            # 5A. Personalized Recommendations
            # -----------------------------------------
            recommendations = generate_recommendations(
                input_data,
                prediction,
                estimated_bill
            )

            top_energy_factors=get_top_energy_factors(input_data)            

            # -----------------------------------------
            # 6. SAVE RECORD TO DATABASE
            # -----------------------------------------
            PredictionRecord.objects.create(

                username=request.user.username,

                month=input_data["Month"],
                month_number=month_number,

                number_of_people=input_data["Number_of_People"],
                number_of_rooms=input_data["Number_of_Rooms"],

                ac_count=input_data["AC_Count"],
                fan_count=input_data["Fan_Count"],
                refrigerator=input_data["Refrigerator"],
                washing_machine=input_data["Washing_Machine"],
                television_count=input_data["Television_Count"],
                geyser=input_data["Geyser"],
                water_pump=input_data["Water_Pump"],
                computer_count=input_data["Computer_Count"],

                temperature=input_data["Temperature"],
                occupancy_hours=input_data["Occupancy_Hours"],
                weekend_usage=input_data["Weekend_Usage"],

                daily_ac_hours=input_data["Daily_AC_Hours"],
                daily_fan_hours=input_data["Daily_Fan_Hours"],
                daily_tv_hours=input_data["Daily_TV_Hours"],
                daily_geyser_hours=input_data["Daily_Geyser_Hours"],
                daily_washing_machine_hours=input_data[
                    "Daily_Washing_Machine_Hours"
                ],

                average_daily_usage_hours=input_data[
                    "Average_Daily_Usage_Hours"
                ],

                previous_month_consumption_kwh=input_data[
                    "Previous_Month_Consumption_kWh"
                ],

                season=season,
                cooling_degree=cooling_degree,

                predicted_consumption_kwh=prediction,
                predicted_bill=estimated_bill
            )


    else:

        form = HouseholdPredictionForm()


    context = {
        "form": form,
        "prediction": prediction,
        "estimated_bill": estimated_bill,
        "recommendations":recommendations,
        "consumption_level":consumption_level,
        "top_energy_factors":top_energy_factors,
    }


    return render(
        request,
        "prediction/prediction_home.html",
        context
    )

def home(request):
    return render(
        request,
        "prediction/home.html"
    )

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(request, user)

            return redirect("/admin-dashboard/")

        messages.error(
            request,
            "Invalid admin username or password."
        )

    return render(
        request,
        "prediction/admin_login.html"
    )

def admin_dashboard(request):

    # -----------------------------------------
    # 1. Check admin authentication
    # -----------------------------------------

    if not request.user.is_authenticated:
        return redirect("/admin-login/")

    if not request.user.is_staff:
        return redirect("/login/")


    # -----------------------------------------
    # 2. Total registered users
    # -----------------------------------------

    total_users = User.objects.count()


    # -----------------------------------------
    # 3. Total prediction records
    # -----------------------------------------

    total_predictions = PredictionRecord.objects.count()


    # -----------------------------------------
    # 4. Average predicted consumption
    # -----------------------------------------

    average_consumption = (
        PredictionRecord.objects.aggregate(
            Avg("predicted_consumption_kwh")
        )["predicted_consumption_kwh__avg"]
    )


    # -----------------------------------------
    # 5. Average predicted bill
    # -----------------------------------------

    average_bill = (
        PredictionRecord.objects.aggregate(
            Avg("predicted_bill")
        )["predicted_bill__avg"]
    )


    # -----------------------------------------
    # 6. Highest consumption
    # -----------------------------------------

    highest_consumption = (
        PredictionRecord.objects.aggregate(
            Max("predicted_consumption_kwh")
        )["predicted_consumption_kwh__max"]
    )


    # -----------------------------------------
    # 7. Registered users
    # -----------------------------------------

    registered_users = (
        User.objects
        .select_related("profile")
        .order_by("-date_joined")
    )


    # -----------------------------------------
    # 8. Prediction records
    # -----------------------------------------

    prediction_records = (
        PredictionRecord.objects
        .order_by("-created_at")
    )


    # -----------------------------------------
    # 9. Prediction activity by month
    # -----------------------------------------

    prediction_activity = (
        PredictionRecord.objects
        .values(
            "month_number",
            "month"
        )
        .annotate(
            total=Count("id")
        )
        .order_by("month_number")
    )


    monthly_analytics = (
    PredictionRecord.objects
    .values("month_number", "month")
    .annotate(
        average_consumption=Avg("predicted_consumption_kwh"),
        average_bill=Avg("predicted_bill"),
    )
    .order_by("month_number")
    )

    # -----------------------------------------
    # Consumption analytics by month
    # -----------------------------------------

    consumption_activity = (
        PredictionRecord.objects
        .values("month_number", "month")
        .annotate(
            average_consumption=Avg(
                "predicted_consumption_kwh"
            )
        )
        .order_by("month_number")
    )


    # -----------------------------------------
    # Bill analytics by month
    # -----------------------------------------

    bill_activity = (
        PredictionRecord.objects
        .values("month_number", "month")
        .annotate(
            average_bill=Avg("predicted_bill")
        )
        .order_by("month_number")
    )


        # -----------------------------------------
        # 10. Dashboard context
        # -----------------------------------------

    context = {

        "total_users": total_users,

        "total_predictions": total_predictions,

        "average_consumption": average_consumption,

        "average_bill": average_bill,

        "highest_consumption": highest_consumption,

        "registered_users": registered_users,

        "prediction_records": prediction_records,

        "prediction_activity": list(prediction_activity),

        "consumption_activity": list(consumption_activity),

        "bill_activity": list(bill_activity),

        "monthly_analytics":list(monthly_analytics),

    }


    # -----------------------------------------
    # 11. Open admin dashboard
    # -----------------------------------------

    return render(
        request,
        "prediction/admin_dashboard.html",
        context
    )

@login_required
def prediction_details(request, prediction_id):

    if not request.user.is_staff:
        return redirect("/login/")

    prediction = PredictionRecord.objects.get(
        id=prediction_id
    )

    return render(
        request,
        "prediction/prediction_details.html",
        {
            "prediction": prediction
        }
    )

@login_required
def prediction_history(request):

    predictions = PredictionRecord.objects.filter(
        username=request.user.username
    ).order_by("-created_at")

    return render(
        request,
        "prediction/prediction_history.html",
        {
            "predictions": predictions
        }
    )

def download_prediction_report(request):

    if not request.user.is_authenticated:
        return redirect("login")

    # Get the latest prediction of the logged-in user
    latest_prediction = PredictionRecord.objects.filter(
        username=request.user.username
    ).order_by("-created_at").first()

    if not latest_prediction:
        return HttpResponse(
            "No prediction available to generate a report.",
            status=404
        )

    # -----------------------------------------
    # Consumption Level
    # -----------------------------------------

    prediction = latest_prediction.predicted_consumption_kwh

    if prediction < 300:
        consumption_level = "Low"
    elif prediction <= 600:
        consumption_level = "Moderate"
    else:
        consumption_level = "High"

    # -----------------------------------------
    # Recreate input data for factor analysis
    # -----------------------------------------

    input_data = {
        "AC_Count": latest_prediction.ac_count,
        "Daily_AC_Hours": latest_prediction.daily_ac_hours,

        "Geyser": latest_prediction.geyser,
        "Daily_Geyser_Hours": latest_prediction.daily_geyser_hours,

        "Fan_Count": latest_prediction.fan_count,
        "Daily_Fan_Hours": latest_prediction.daily_fan_hours,

        "Television_Count": latest_prediction.television_count,
        "Daily_TV_Hours": latest_prediction.daily_tv_hours,

        "Washing_Machine": latest_prediction.washing_machine,
        "Daily_Washing_Machine_Hours":
            latest_prediction.daily_washing_machine_hours,

        "Water_Pump": latest_prediction.water_pump,

        "Computer_Count":
            latest_prediction.computer_count,

        "Occupancy_Hours":
            latest_prediction.occupancy_hours,
    }

    # -----------------------------------------
    # Top Energy-Consuming Factors
    # -----------------------------------------

    top_energy_factors = get_top_energy_factors(
        input_data
    )

    # -----------------------------------------
    # Personalized Recommendations
    # -----------------------------------------

    recommendations = generate_recommendations(
        input_data,
        prediction,
        latest_prediction.predicted_bill
    )

    # -----------------------------------------
    # Create PDF response
    # -----------------------------------------

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; '
        'filename="electricity_prediction_report.pdf"'
    )

    # -----------------------------------------
    # Generate PDF
    # -----------------------------------------

    generate_prediction_report(
        response=response,
        username=request.user.username,
        month=latest_prediction.month,
        prediction=latest_prediction.predicted_consumption_kwh,
        estimated_bill=latest_prediction.predicted_bill,
        consumption_level=consumption_level,
        top_energy_factors=top_energy_factors,
        recommendations=recommendations,
    )

    return response

def energy_chatbot(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "response": "Please login to use the Smart Energy Assistant."
            },
            status=401
        )

    if request.method != "POST":
        return JsonResponse(
            {
                "response": "Please send a message to the chatbot."
            },
            status=400
        )

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse(
            {
                "response": "Please type a question."
            },
            status=400
        )

    # Get user's latest prediction
    latest_prediction = PredictionRecord.objects.filter(
        username=request.user.username
    ).order_by("-created_at").first()

    prediction = None
    estimated_bill = None

    if latest_prediction:
        prediction = latest_prediction.predicted_consumption_kwh
        estimated_bill = latest_prediction.predicted_bill

    # Get chatbot response
    response_text = get_energy_chatbot_response(
        message=message,
        prediction=prediction,
        estimated_bill=estimated_bill
    )

    return JsonResponse(
        {
            "response": response_text
        }
    )
