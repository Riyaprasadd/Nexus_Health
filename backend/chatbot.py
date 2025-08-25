# backend/chatbot.py

def get_chatbot_response(user_input: str) -> str:
    text = user_input.lower().strip()

    # very small demo knowledge; expand as you like
    if "diabetes" in text:
        return (
            "Diabetes is a condition where blood glucose is too high. "
            "General tips: focus on whole foods, monitor carbs, stay active, "
            "and follow your clinician’s advice. If you have symptoms like "
            "excessive thirst or frequent urination, seek medical guidance."
        )
    if "hypertension" in text or "blood pressure" in text:
        return (
            "High blood pressure can often be improved with reduced sodium, "
            "regular aerobic activity, stress management, and medication if prescribed."
        )

    if text in {"hi", "hello", "hey"}:
        return "Hi! Ask me anything about health & wellness. 😊"

    # default
    return (
        "I’m here to help with general wellness information. "
        "Try asking about sleep, stress, diabetes, blood pressure, or nutrition."
    )
