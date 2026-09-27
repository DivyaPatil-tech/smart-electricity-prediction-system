def generate_recommendations(input_data, prediction, estimated_bill):
    """
    Generate personalized electricity-saving recommendations
    based on household input data and prediction results.
    """

    # ---------------------------------------------------------
    # Helper function
    # Converts Django form values (strings) into numbers safely
    # ---------------------------------------------------------
    def to_float(value, default=0):
        try:
            if value is None or value == "":
                return float(default)
            return float(value)
        except (ValueError, TypeError):
            return float(default)

    # ---------------------------------------------------------
    # Convert prediction and bill to numeric values
    # ---------------------------------------------------------
    prediction = to_float(prediction)
    estimated_bill = to_float(estimated_bill)

    # ---------------------------------------------------------
    # Convert input values from strings to numbers
    # ---------------------------------------------------------
    number_of_people = to_float(
        input_data.get("Number_of_People", 0)
    )

    number_of_rooms = to_float(
        input_data.get("Number_of_Rooms", 0)
    )

    ac_count = to_float(
        input_data.get("AC_Count", 0)
    )

    fan_count = to_float(
        input_data.get("Fan_Count", 0)
    )

    refrigerator = to_float(
        input_data.get("Refrigerator", 0)
    )

    washing_machine = to_float(
        input_data.get("Washing_Machine", 0)
    )

    television_count = to_float(
        input_data.get("Television_Count", 0)
    )

    geyser = to_float(
        input_data.get("Geyser", 0)
    )

    water_pump = to_float(
        input_data.get("Water_Pump", 0)
    )

    computer_count = to_float(
        input_data.get("Computer_Count", 0)
    )

    temperature = to_float(
        input_data.get("Temperature", 0)
    )

    occupancy_hours = to_float(
        input_data.get("Occupancy_Hours", 0)
    )

    weekend_usage = to_float(
        input_data.get("Weekend_Usage", 0)
    )

    daily_ac_hours = to_float(
        input_data.get("Daily_AC_Hours", 0)
    )

    daily_fan_hours = to_float(
        input_data.get("Daily_Fan_Hours", 0)
    )

    daily_tv_hours = to_float(
        input_data.get("Daily_TV_Hours", 0)
    )

    daily_geyser_hours = to_float(
        input_data.get("Daily_Geyser_Hours", 0)
    )

    daily_washing_machine_hours = to_float(
        input_data.get("Daily_Washing_Machine_Hours", 0)
    )

    average_daily_usage_hours = to_float(
        input_data.get("Average_Daily_Usage_Hours", 0)
    )

    previous_month_consumption = to_float(
        input_data.get("Previous_Month_Consumption_kWh", 0)
    )

    cooling_degree = to_float(
        input_data.get("Cooling_Degree", 0)
    )

    # ---------------------------------------------------------
    # Recommendation list
    # ---------------------------------------------------------
    recommendations = []

    # =========================================================
    # 1. Air Conditioner
    # =========================================================

    if ac_count > 0 and daily_ac_hours >= 6:
        recommendations.append(
            "Your AC usage is relatively high. "
            "Try setting the AC temperature around 24-26°C "
            "and switch it off when the room is unoccupied."
        )

    elif ac_count > 0 and daily_ac_hours >= 4:
        recommendations.append(
            "Consider reducing daily AC usage by using fans "
            "whenever weather conditions allow."
        )

    # =========================================================
    # 2. Fan Usage
    # =========================================================

    if fan_count > 0 and daily_fan_hours >= 10:
        recommendations.append(
            "Fan usage is high. Switch off fans when rooms are "
            "unoccupied and use lower speed settings when possible."
        )

    # =========================================================
    # 3. Television Usage
    # =========================================================

    if television_count > 0 and daily_tv_hours >= 5:
        recommendations.append(
            "TV usage is relatively high. Avoid leaving the TV "
            "running when nobody is watching and switch it off "
            "instead of keeping it on standby."
        )

    # =========================================================
    # 4. Geyser Usage
    # =========================================================

    if geyser > 0 and daily_geyser_hours >= 2:
        recommendations.append(
            "Geyser usage is high. Reduce heating time and avoid "
            "keeping the geyser switched on unnecessarily."
        )

    # =========================================================
    # 5. Washing Machine
    # =========================================================

    if washing_machine > 0 and daily_washing_machine_hours >= 1:
        recommendations.append(
            "Try running the washing machine with full loads "
            "instead of multiple small loads to reduce electricity usage."
        )

    # =========================================================
    # 6. Average Daily Usage
    # =========================================================

    if average_daily_usage_hours >= 12:
        recommendations.append(
            "Your average daily appliance usage is high. "
            "Identify appliances that remain switched on for long "
            "periods and turn them off when they are not required."
        )

    elif average_daily_usage_hours >= 8:
        recommendations.append(
            "Your average daily usage is moderate to high. "
            "Reducing unnecessary appliance operating time can "
            "help lower your monthly electricity consumption."
        )

    # =========================================================
    # 7. Occupancy
    # =========================================================

    if occupancy_hours >= 12:
        recommendations.append(
            "Your household has a high daily occupancy period. "
            "Try switching off lights, fans and appliances in rooms "
            "that are temporarily unoccupied."
        )

    # =========================================================
    # 8. Weekend Usage
    # =========================================================

    if weekend_usage >= 8:
        recommendations.append(
            "Weekend usage is relatively high. "
            "Avoid leaving appliances running for long periods "
            "when they are not required."
        )

    # =========================================================
    # 9. Overall Predicted Consumption
    # =========================================================

    if prediction >= 800:
        recommendations.append(
            "Your predicted monthly electricity consumption is high. "
            "Focus on reducing AC, geyser and other high-power "
            "appliance usage."
        )

    elif prediction >= 500:
        recommendations.append(
            "Your predicted electricity consumption is moderate to high. "
            "Small reductions in daily appliance usage can help lower "
            "your monthly consumption."
        )

    else:
        recommendations.append(
            "Your predicted monthly electricity consumption is "
            "relatively low. Continue following energy-saving practices."
        )

    # =========================================================
    # 10. Estimated Electricity Bill
    # =========================================================

    if estimated_bill >= 5000:
        recommendations.append(
            "Your estimated monthly electricity bill is high. "
            "Reducing the usage of high-consumption appliances can "
            "help control your electricity expenses."
        )

    elif estimated_bill >= 2500:
        recommendations.append(
            "Your estimated electricity bill is moderate to high. "
            "Monitor high-energy appliances and avoid unnecessary usage."
        )

    else:
        recommendations.append(
            "Your estimated electricity bill is relatively low. "
            "Continue monitoring your monthly electricity consumption."
        )

    # =========================================================
    # 11. Temperature / Cooling
    # =========================================================

    if temperature >= 32 or cooling_degree >= 10:
        recommendations.append(
            "The current temperature indicates higher cooling demand. "
            "Use AC efficiently, keep doors and windows closed while "
            "cooling, and clean AC filters regularly."
        )

    # =========================================================
    # 12. Previous Month Comparison
    # =========================================================

    if previous_month_consumption > 0:

        if prediction > previous_month_consumption * 1.20:
            recommendations.append(
                "Your predicted consumption is significantly higher "
                "than the previous month's consumption. Review AC, "
                "geyser and other high-energy appliance usage."
            )

        elif prediction < previous_month_consumption * 0.80:
            recommendations.append(
                "Your predicted consumption is lower than the previous "
                "month. Continue following your current energy-saving habits."
            )

    # =========================================================
    # Final fallback
    # =========================================================

    if not recommendations:
        recommendations.append(
            "Continue monitoring your electricity consumption and "
            "switch off appliances when they are not required."
        )

    # ---------------------------------------------------------
    # Return recommendations to the Django view
    # ---------------------------------------------------------
    return recommendations

def get_top_energy_factors(input_data):
    """
    Identify the major household factors contributing
    to electricity consumption based on the user's inputs.
    """

    factors = []

    # AC usage
    ac_count = float(input_data.get("AC_Count", 0) or 0)
    ac_hours = float(input_data.get("Daily_AC_Hours", 0) or 0)

    ac_score = ac_count * ac_hours

    if ac_score > 0:
        factors.append({
            "name": "AC Usage",
            "score": ac_score,
            "description": f"{int(ac_count)} AC(s) × {ac_hours:.1f} hours/day"
        })

    # Geyser usage
    geyser = float(input_data.get("Geyser", 0) or 0)
    geyser_hours = float(
        input_data.get("Daily_Geyser_Hours", 0) or 0
    )

    geyser_score = geyser * geyser_hours

    if geyser_score > 0:
        factors.append({
            "name": "Geyser Usage",
            "score": geyser_score,
            "description": f"{int(geyser)} geyser(s) × {geyser_hours:.1f} hours/day"
        })

    # Fan usage
    fan_count = float(input_data.get("Fan_Count", 0) or 0)
    fan_hours = float(input_data.get("Daily_Fan_Hours", 0) or 0)

    fan_score = fan_count * fan_hours

    if fan_score > 0:
        factors.append({
            "name": "Fan Usage",
            "score": fan_score,
            "description": f"{int(fan_count)} fan(s) × {fan_hours:.1f} hours/day"
        })

    # TV usage
    tv_count = float(input_data.get("Television_Count", 0) or 0)
    tv_hours = float(input_data.get("Daily_TV_Hours", 0) or 0)

    tv_score = tv_count * tv_hours

    if tv_score > 0:
        factors.append({
            "name": "Television Usage",
            "score": tv_score,
            "description": f"{int(tv_count)} TV(s) × {tv_hours:.1f} hours/day"
        })

    # Washing machine
    washing_machine = float(
        input_data.get("Washing_Machine", 0) or 0
    )

    washing_hours = float(
        input_data.get("Daily_Washing_Machine_Hours", 0) or 0
    )

    washing_score = washing_machine * washing_hours

    if washing_score > 0:
        factors.append({
            "name": "Washing Machine Usage",
            "score": washing_score,
            "description": (
                f"{int(washing_machine)} machine(s) × "
                f"{washing_hours:.1f} hours/day"
            )
        })

    # Water pump
    water_pump = float(
        input_data.get("Water_Pump", 0) or 0
    )

    if water_pump > 0:
        factors.append({
            "name": "Water Pump",
            "score": water_pump,
            "description": "Water pump usage detected"
        })

    # Computer usage
    computer_count = float(
        input_data.get("Computer_Count", 0) or 0
    )

    if computer_count > 0:
        factors.append({
            "name": "Computer Usage",
            "score": computer_count,
            "description": f"{int(computer_count)} computer(s)"
        })

    # Occupancy
    occupancy_hours = float(
        input_data.get("Occupancy_Hours", 0) or 0
    )

    if occupancy_hours > 0:
        factors.append({
            "name": "Occupancy Hours",
            "score": occupancy_hours,
            "description": f"{occupancy_hours:.1f} hours/day"
        })

    # Sort from highest to lowest
        factors.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # Add user-friendly impact level
        for factor in factors:

            if factor["score"] >= 8:
                factor["impact"] = "High"
            elif factor["score"] >= 3:
                factor["impact"] = "Moderate"
            else:
                factor["impact"] = "Low"

        # Return top 3 factors
        return factors[:3]
