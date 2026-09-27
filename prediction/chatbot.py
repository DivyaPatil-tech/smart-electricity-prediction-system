def get_energy_chatbot_response(message, prediction=None, estimated_bill=None):
    """
    Rule-based Smart Energy Chatbot.

    It can answer common electricity consumption,
    bill, prediction and energy-saving questions.
    """

    message = message.lower().strip()

    # -----------------------------------------
    # Greeting
    # -----------------------------------------

    if message in [
        "hello",
        "hi",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]:
        return (
            "Hello! 👋 I am your Smart Energy Assistant. "
            "I can help you understand your electricity "
            "consumption, estimated bill, and energy-saving tips."
        )

    # -----------------------------------------
    # Latest prediction
    # -----------------------------------------

    if (
        "predicted consumption" in message
        or "my prediction" in message
        or "latest prediction" in message
        or "what is my consumption" in message
        or "how much electricity will i use" in message
        or "what will my consumption be" in message
        or "how much will i consume" in message
    ):
        if prediction is not None:
            return (
                f"⚡ Your latest predicted monthly electricity "
                f"consumption is {float(prediction):.2f} kWh."
            )

        return (
            "You have not made a prediction yet. "
            "Please make a prediction first."
        )

    # -----------------------------------------
    # Electricity bill
    # -----------------------------------------

    if (
        "bill" in message
        or "electricity cost" in message
        or "electricity charge" in message
        or "estimated bill" in message
        or "monthly bill" in message
        or "electricity bill" in message
    ):
        if estimated_bill is not None:
            return (
                f"💰 Your latest estimated monthly electricity "
                f"bill is ₹{float(estimated_bill):.2f}."
            )

        return (
            "You have not made a prediction yet, so an estimated "
            "bill is not available."
        )

    # -----------------------------------------
    # Reduce consumption
    # -----------------------------------------

    if (
        "reduce consumption" in message
        or "reduce my consumption" in message
        or "reduce electricity" in message
        or "reduce my electricity" in message
        or "save electricity" in message
        or "save energy" in message
        or "energy saving" in message
        or "energy-saving" in message
        or "save my electricity" in message
        or "lower my consumption" in message
        or "decrease my consumption" in message
        or "how can i save" in message
        or "how can i reduce" in message
        or "ways to save electricity" in message
        or "ways to save energy" in message
    ):
        return (
            "💡 Here are some ways to reduce electricity consumption:\n\n"
            "• Reduce unnecessary AC usage.\n"
            "• Set the AC to a reasonable temperature.\n"
            "• Switch off lights and appliances when not required.\n"
            "• Reduce unnecessary geyser usage.\n"
            "• Avoid keeping appliances on standby.\n"
            "• Use energy-efficient appliances where possible."
        )

    # -----------------------------------------
    # AC
    # -----------------------------------------

    if (
        "ac" in message
        or "air conditioner" in message
        or "air conditioning" in message
    ):
        return (
            "❄️ AC usage can significantly affect household "
            "electricity consumption. Try reducing daily AC hours "
            "and avoid unnecessarily low temperature settings."
        )

    # -----------------------------------------
    # Geyser
    # -----------------------------------------

    if (
        "geyser" in message
        or "water heater" in message
    ):
        return (
            "🔥 Geysers can contribute noticeably to electricity "
            "consumption. Reduce unnecessary heating time and "
            "avoid keeping the geyser switched on continuously."
        )

    # -----------------------------------------
    # High consumption
    # -----------------------------------------

    if (
        "high consumption" in message
        or "high electricity consumption" in message
        or "consumption is high" in message
        or "usage is high" in message
        or "electricity usage is high" in message
        or "electricity consumption is high" in message
        or "why is my consumption high" in message
        or "why is my electricity consumption high" in message
        or "why is my electricity usage high" in message
        or "why is my usage high" in message
        or "why is consumption high" in message
        or "what is high consumption" in message
        or "what does high consumption mean" in message
        or "why is my electricity bill high" in message
        or "why is my bill high" in message
    ):
        return (
            "🔴 High electricity consumption can be caused by "
            "factors such as high AC usage, geyser usage, longer "
            "appliance operating hours, higher occupancy, and "
            "frequent use of electrical appliances."
        )

    # -----------------------------------------
    # Moderate consumption
    # -----------------------------------------

    if (
        "moderate consumption" in message
        or "medium consumption" in message
        or "moderate electricity consumption" in message
        or "moderate electricity usage" in message
        or "is my consumption moderate" in message
        or "is my usage moderate" in message
        or "what is moderate consumption" in message
        or "what does moderate consumption mean" in message
    ):
        return (
            "🟡 Moderate consumption means your predicted electricity "
            "usage falls within the moderate range defined by this "
            "project. Reducing unnecessary appliance usage can help "
            "lower consumption further."
        )

    # -----------------------------------------
    # Low consumption
    # -----------------------------------------

    if (
        "low consumption" in message
        or "low electricity" in message
        or "low electricity consumption" in message
        or "low electricity usage" in message
        or "is my consumption low" in message
        or "is my usage low" in message
        or "what is low consumption" in message
        or "what does low consumption mean" in message
    ):
        return (
            "🟢 Low consumption means your predicted electricity "
            "usage falls within the low range defined by this project. "
            "Continue following energy-efficient practices."
        )

    # -----------------------------------------
    # How system works
    # -----------------------------------------

    if (
        "how does this work" in message
        or "how does this prediction system work" in message
        or "how prediction works" in message
        or "how does prediction work" in message
        or "how does the prediction work" in message
        or "how is electricity predicted" in message
        or "how is my electricity consumption predicted" in message
        or "how does the model work" in message
        or "how does machine learning predict" in message
        or "how is prediction calculated" in message
        or "how does ml predict" in message
    ):
        return (
            "🤖 The system uses household and appliance-related "
            "inputs such as number of people, appliance usage, "
            "daily operating hours, temperature and previous "
            "consumption to predict monthly electricity "
            "consumption using a trained machine learning model. "
            "It then estimates the electricity bill and provides "
            "energy-saving insights."
        )

    # -----------------------------------------
    # About project
    # -----------------------------------------

    if (
        "about project" in message
        or "what is this project" in message
        or "what does this system do" in message
        or "tell me about this project" in message
        or "explain this project" in message
        or "what is this system" in message
        or "what does this project do" in message
        or "purpose of this project" in message
    ):
        return (
            "🏠 This is a Smart Household Electricity Consumption "
            "and Electricity Bill Prediction System. It uses "
            "machine learning to predict monthly household "
            "electricity consumption and estimate the electricity "
            "bill. It also provides a consumption-level indicator, "
            "identifies major energy-consuming factors, gives "
            "personalized energy-saving recommendations, maintains "
            "prediction history, and provides a downloadable "
            "prediction report."
        )

    # -----------------------------------------
    # Thank you
    # -----------------------------------------

    if (
        "thank you" in message
        or "thanks" in message
        or "thank you so much" in message
    ):
        return (
            "You're welcome! 😊 I'm happy to help you save energy."
        )

    # -----------------------------------------
    # Default response
    # -----------------------------------------

    return (
        "I'm your Smart Energy Assistant 🤖. "
        "You can ask me things like:\n\n"
        "• What is my predicted consumption?\n"
        "• What is my estimated bill?\n"
        "• How can I reduce electricity consumption?\n"
        "• Why is my consumption high?\n"
        "• What is moderate consumption?\n"
        "• What is low consumption?\n"
        "• How does this prediction system work?\n"
        "• How can I reduce AC or geyser usage?\n"
        "• Tell me about this project."
    )
