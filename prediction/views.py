from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Count
from django.core.paginator import Paginator

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
    was_admin = request.user.is_staff

    logout(request)

    if was_admin:
        return redirect("admin_login")

    return redirect("login")


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

            return redirect("user_dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "prediction/login.html"
    )

@login_required
@never_cache
def user_dashboard(request):

    latest_prediction = (
        PredictionRecord.objects
        .filter(username=request.user.username)
        .order_by("-created_at")
        .first()
    )

    total_predictions = (
        PredictionRecord.objects
        .filter(username=request.user.username)
        .count()
    )

    consumption_level = None

    if latest_prediction:

        consumption = float(
            latest_prediction.predicted_consumption_kwh
        )

        if consumption < 300:
            consumption_level = "Low"

        elif consumption <= 600:
            consumption_level = "Moderate"

        else:
            consumption_level = "High"

    top_energy_factors = []
    recommendations = []

    if latest_prediction:

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

        top_energy_factors = get_top_energy_factors(
            input_data
        )

        recommendations = generate_recommendations(
            input_data,
            latest_prediction.predicted_consumption_kwh,
            latest_prediction.predicted_bill
        )


    return render(
        request,
        "prediction/user_dashboard.html",
        {
            "latest_prediction": latest_prediction,
            "total_predictions": total_predictions,
            "consumption_level": consumption_level,
            "top_energy_factors": top_energy_factors,
            "recommendations": recommendations,
        }
    )

@login_required
@never_cache
def user_analytics(request):

    user_predictions = (
        PredictionRecord.objects
        .filter(username=request.user.username)
        .order_by("-created_at")
    )

    recent_predictions = user_predictions[:5]

    total_predictions = user_predictions.count()

    average_consumption = (
        user_predictions.aggregate(
            Avg("predicted_consumption_kwh")
        )["predicted_consumption_kwh__avg"]
    )

    average_bill = (
        user_predictions.aggregate(
            Avg("predicted_bill")
        )["predicted_bill__avg"]
    )

    highest_consumption = (
        user_predictions.aggregate(
            Max("predicted_consumption_kwh")
        )["predicted_consumption_kwh__max"]
    )

    # -----------------------------------------
    # Latest Energy Insight
    # -----------------------------------------

    latest_prediction = user_predictions.first()

    energy_insight = None

    energy_trend = None

    if latest_prediction and average_consumption:

        latest_consumption = float(
            latest_prediction.predicted_consumption_kwh
        )

        average_value = float(
            average_consumption
        )

        if latest_consumption > average_value:
            energy_trend = "above"

            energy_insight = (
                f"Your latest predicted consumption is "
                f"{latest_consumption:.2f} kWh, which is above "
                f"your average consumption of "
                f"{average_value:.2f} kWh."
            )

        elif latest_consumption < average_value:
            energy_trend = "below"

            energy_insight = (
                f"Your latest predicted consumption is "
                f"{latest_consumption:.2f} kWh, which is below "
                f"your average consumption of "
                f"{average_value:.2f} kWh."
            )

        else:
            energy_trend = "equal"

            energy_insight = (
                f"Your latest predicted consumption is "
                f"{latest_consumption:.2f} kWh, which is equal "
                f"to your average consumption."
            )

    # -----------------------------------------
    # Consumption Level Distribution
    # -----------------------------------------

    low_consumption = user_predictions.filter(
        predicted_consumption_kwh__lt=300
    ).count()

    moderate_consumption = user_predictions.filter(
        predicted_consumption_kwh__gte=300,
        predicted_consumption_kwh__lte=600
    ).count()

    high_consumption = user_predictions.filter(
        predicted_consumption_kwh__gt=600
    ).count()



    monthly_consumption = (
        user_predictions
        .values(
            "month_number",
            "month"
        )
        .annotate(
            average_consumption=Avg(
                "predicted_consumption_kwh"
            )
        )
        .order_by("month_number")
    )

    # -----------------------------------------
    # Peak and Lowest Usage Months
    # -----------------------------------------

    peak_usage_month = None
    lowest_usage_month = None

    if monthly_consumption:

        peak_usage_month = max(
            monthly_consumption,
            key=lambda item: item["average_consumption"]
        )

        lowest_usage_month = min(
            monthly_consumption,
            key=lambda item: item["average_consumption"]
        )

    monthly_bill = (
            user_predictions
            .values(
                "month_number",
                "month"
            )
            .annotate(
                average_bill=Avg(
                    "predicted_bill"
                )
            )
            .order_by("month_number")
        )

    return render(
        request,
        "prediction/user_analytics.html",
        {
            "total_predictions": total_predictions,
            "average_consumption": average_consumption,
            "average_bill": average_bill,
            "highest_consumption": highest_consumption,

            "energy_insight":energy_insight,
            "energy_trend" : energy_trend,

            "recent_predictions":recent_predictions,

            "low_consumption": low_consumption,
            "moderate_consumption": moderate_consumption,
            "high_consumption": high_consumption,

            "monthly_consumption": list(monthly_consumption),
            "monthly_bill":list(monthly_bill),

            "peak_usage_month": peak_usage_month,
            "lowest_usage_month": lowest_usage_month,
        }
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

    registered_search = request.GET.get("user_search", "").strip()

    registered_users = User.objects.select_related("profile")

    if registered_search:
        registered_users = registered_users.filter(
            username__icontains=registered_search
        )

    registered_users = registered_users.order_by("-date_joined")


    # -----------------------------------------
    # 8. Prediction records
    # -----------------------------------------

    search_query = request.GET.get("search", "").strip()

    prediction_records = PredictionRecord.objects.all()

    if search_query:
        prediction_records = prediction_records.filter(
            username__icontains=search_query
        )

    prediction_records = prediction_records.order_by("-created_at")

    # -----------------------------------------
    # Pagination
    # -----------------------------------------

    paginator = Paginator(
        prediction_records,
        10
    )

    page_number = request.GET.get("page")

    prediction_records = paginator.get_page(
        page_number
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

    # =========================================================
    # ADVANCED ADMIN ANALYTICS
    # =========================================================

    # Top users by average predicted consumption
    top_users_consumption = list(
        PredictionRecord.objects
        .values("username")
        .annotate(
            average_consumption=Avg(
                "predicted_consumption_kwh"
            )
        )
        .order_by("-average_consumption")[:5]
    )

    # Consumption level distribution
    low_consumption_count = PredictionRecord.objects.filter(
        predicted_consumption_kwh__lt=300
    ).count()

    moderate_consumption_count = PredictionRecord.objects.filter(
        predicted_consumption_kwh__gte=300,
        predicted_consumption_kwh__lte=600
    ).count()

    high_consumption_count = PredictionRecord.objects.filter(
        predicted_consumption_kwh__gt=600
    ).count()

    consumption_level_distribution = [
        {
            "level": "Low",
            "count": low_consumption_count,
        },
        {
            "level": "Moderate",
            "count": moderate_consumption_count,
        },
        {
            "level": "High",
            "count": high_consumption_count,
        },
    ]



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

        "top_users_consumption": top_users_consumption,

        "consumption_level_distribution": consumption_level_distribution,

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
def user_details(request, user_id):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    selected_user = User.objects.select_related("profile").get(
        id=user_id
    )

    if request.method == "POST":
        photo = request.FILES.get("photo")

        if photo:
            selected_user.profile.photo = photo
            selected_user.profile.save()

            messages.success(
                request,
                "Profile photo updated successfully."
            )

        return redirect(
            "user_details",
            user_id=selected_user.id
        )

    user_predictions = PredictionRecord.objects.filter(
        username=selected_user.username
    ).order_by("-created_at")

    # -----------------------------------------
    # Prediction Summary
    # -----------------------------------------

    prediction_summary = user_predictions.aggregate(
        total_predictions=Count("id"),
        average_consumption=Avg("predicted_consumption_kwh"),
        average_bill=Avg("predicted_bill"),
        highest_consumption=Max("predicted_consumption_kwh"),
    )

    latest_prediction = user_predictions.first()

    return render(
        request,
        "prediction/user_details.html",
        {
            "selected_user": selected_user,
            "user_predictions": user_predictions,
            "prediction_summary": prediction_summary,
            "latest_prediction": latest_prediction,
        }
    )


@login_required
def prediction_details(request, prediction_id):

    prediction = PredictionRecord.objects.get(
        id=prediction_id
    )

    # Admin can view any prediction.
    # Normal users can view only their own prediction.
    if not request.user.is_staff:
        if prediction.username != request.user.username:
            return redirect("user_dashboard")

    selected_user = None

    if request.user.is_staff:
        selected_user = User.objects.select_related("profile").get(
            username=prediction.username
        )

    return render(
        request,
        "prediction/prediction_details.html",
        {
            "prediction": prediction,
            "selected_user": selected_user,
        }
    )

@login_required
def admin_download_prediction_report(request, prediction_id):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    prediction = PredictionRecord.objects.get(
        id=prediction_id
    )

    consumption = float(
        prediction.predicted_consumption_kwh
    )

    if consumption < 300:
        consumption_level = "Low"
    elif consumption <= 600:
        consumption_level = "Moderate"
    else:
        consumption_level = "High"

    input_data = {
        "AC_Count": prediction.ac_count,
        "Daily_AC_Hours": prediction.daily_ac_hours,
        "Geyser": prediction.geyser,
        "Daily_Geyser_Hours": prediction.daily_geyser_hours,
        "Fan_Count": prediction.fan_count,
        "Daily_Fan_Hours": prediction.daily_fan_hours,
        "Television_Count": prediction.television_count,
        "Daily_TV_Hours": prediction.daily_tv_hours,
        "Washing_Machine": prediction.washing_machine,
        "Daily_Washing_Machine_Hours": prediction.daily_washing_machine_hours,
        "Water_Pump": prediction.water_pump,
        "Computer_Count": prediction.computer_count,
        "Occupancy_Hours": prediction.occupancy_hours,
    }

    top_energy_factors = get_top_energy_factors(
        input_data
    )

    recommendations = generate_recommendations(
        input_data,
        prediction.predicted_consumption_kwh,
        prediction.predicted_bill
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="prediction_{prediction.id}_report.pdf"'
    )

    generate_prediction_report(
        response=response,
        username=prediction.username,
        month=prediction.month,
        prediction=prediction.predicted_consumption_kwh,
        estimated_bill=prediction.predicted_bill,
        consumption_level=consumption_level,
        top_energy_factors=top_energy_factors,
        recommendations=recommendations,
        prediction_id=prediction.id,
    )

    return response

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

@login_required
def admin_user_prediction_history(request, user_id):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    selected_user = User.objects.select_related("profile").get(
        id=user_id
    )

    predictions = PredictionRecord.objects.filter(
        username=selected_user.username
    ).order_by("-created_at")

    paginator = Paginator(
        predictions,
        10
    )

    page_number = request.GET.get("page")

    predictions = paginator.get_page(
        page_number
    )

    return render(
        request,
        "prediction/admin_user_prediction_history.html",
        {
            "selected_user": selected_user,
            "predictions": predictions,
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
