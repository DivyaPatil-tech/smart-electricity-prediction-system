import pickle
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Locate the Django project directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# 2. Locate the ML deployment package
# --------------------------------------------------

MODEL_PATH = (
    BASE_DIR
    / "ml_models"
    / "electricity_deployment_package_fixed.pkl"
)


# --------------------------------------------------
# 3. Load the deployment package
# --------------------------------------------------

with open(MODEL_PATH, "rb") as file:
    deployment_package = pickle.load(file)


# --------------------------------------------------
# 4. Extract ML components
# --------------------------------------------------

model = deployment_package["model"]

month_encoder = deployment_package["month_encoder"]

season_encoder = deployment_package["season_encoder"]

feature_names = deployment_package["feature_names"]


# --------------------------------------------------
# 5. Create Season
# --------------------------------------------------

def assign_season(month):

    if month in ["January", "February"]:
        return "Winter"

    elif month in ["March", "April", "May"]:
        return "Summer"

    elif month in ["June", "July", "August", "September"]:
        return "Monsoon"

    else:
        return "Post-Monsoon"


# --------------------------------------------------
# 6. Calculate Electricity Bill
# --------------------------------------------------

def calculate_electricity_bill(consumption):

    if consumption < 0:
        raise ValueError(
            "Electricity consumption cannot be negative."
        )

    bill = 0

    # Slab 1: First 100 units
    if consumption <= 100:

        bill = consumption * 4

    # Slab 2: 101 to 200 units
    elif consumption <= 200:

        bill = (
            (100 * 4)
            + ((consumption - 100) * 5)
        )

    # Slab 3: 201 to 400 units
    elif consumption <= 400:

        bill = (
            (100 * 4)
            + (100 * 5)
            + ((consumption - 200) * 6)
        )

    # Slab 4: Above 400 units
    else:

        bill = (
            (100 * 4)
            + (100 * 5)
            + (200 * 6)
            + ((consumption - 400) * 8)
        )

    # Fixed charge
    fixed_charge = 150

    total_bill = bill + fixed_charge

    return round(total_bill, 2)


# --------------------------------------------------
# 7. Main Prediction Function
# --------------------------------------------------

def predict_household_bill(input_data):

    # Convert dictionary into DataFrame
    input_df = pd.DataFrame([input_data])

    # Create Season
    input_df["Season"] = input_df["Month"].apply(
        assign_season
    )

    # Create Cooling Degree
    input_df["Cooling_Degree"] = (
        input_df["Temperature"] - 27
    ).clip(lower=0)


    # Create Month Number
    month_number_map = {
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

    input_df["Month_Number"] = input_df["Month"].map(month_number_map)

    # Encode Month
    input_df["Month"] = month_encoder.transform(
        input_df["Month"]
    )

    # Encode Season
    input_df["Season"] = season_encoder.transform(
        input_df["Season"]
    )

    # Arrange columns in exact training order
    input_df = input_df[feature_names]

    # Predict consumption
    predicted_kwh = model.predict(input_df)[0]

    # Calculate electricity bill
    estimated_bill = calculate_electricity_bill(
        predicted_kwh
    )

    return round(predicted_kwh, 2), estimated_bill