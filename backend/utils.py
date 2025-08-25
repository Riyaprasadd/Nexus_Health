import os


try:
    from googletrans import Translator
    _translator = Translator()
except Exception:
    _translator = None


SAFETY_NOTE = (
"This chatbot provides general wellness information and is not a substitute for professional medical advice. "
"If you have severe, persistent, or worrying symptoms, please seek a qualified clinician."
)


CITATIONS: dict[str, list[dict]] = {
"hydration": [
{"label": "WHO – Healthy Hydration", "url": "https://www.who.int/"},
{"label": "CDC – Water & Nutrition", "url": "https://www.cdc.gov/healthyweight/healthy_eating/water-and-health.html"},
],
"sleep": [
{"label": "NIH – Healthy Sleep", "url": "https://www.nhlbi.nih.gov/health/sleep"},
],
"nutrition": [
{"label": "Harvard – Healthy Plate", "url": "https://www.hsph.harvard.edu/nutritionsource/healthy-eating-plate/"},
],
"stress": [
{"label": "WHO – Stress Management", "url": "https://www.who.int/"},
],
}


TIPS = {
"hydration": [
"Carry a reusable bottle and set hourly reminders to sip.",
"Flavor water with lemon or mint instead of sugary drinks.",
],
"sleep": [
"Aim for 7–9 hours. Keep a regular sleep/wake schedule—even on weekends.",
"Avoid screens 60 minutes before bed; dim lights to cue melatonin.",
],
"nutrition": [
"Build plates with 1/2 veggies, 1/4 protein, 1/4 whole grains.",
"Add a fruit or nuts for a fiber-rich snack to steady energy.",
],
"stress": [
"Try a 4-7-8 breathing cycle for 1 minute during stressful moments.",
"Schedule a 10-minute walk to reset your nervous system.",
],
}




def translate(text: str, dest_lang: str = "en") -> str:
    if not dest_lang or dest_lang.lower() == "en" or _translator is None:
        return text
    try:
        return _translator.translate(text, dest=dest_lang).text
    except Exception:
        return text




def get_tip(category: str) -> str:
    items = TIPS.get(category, [])
    if not items:
        return "Stay curious, stay kind to your body!"
# Simple rotation
    return items[0]




def get_citations(category: str) -> list[dict]:
    return CITATIONS.get(category, [])