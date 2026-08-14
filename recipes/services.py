import json
from getenv import OPENAI_API_KEY


def calculate_recipe_nutrition(ingredients_text):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
    Quyidagi ingredientlar ro'yxatiga asoslanib umumiy kaloriya, oqsil (protein), uglevod (carbs), yog' (fat) va tolalar (fiber) miqdorini hisoblab ber hamda bu ovqatni iste'mol qilish orqali nimalarga ega bo'lish mumkinligini (benefits) qisqacha tushuntir:
    "{ingredients_text}"

    JAVOBNI FAQAT SHU JSON FORMATIDA QAYTAR (boshqa matn yoza ma):
    {{
        "calories": 420,
        "protein": "24g",
        "carbs": "32g",
        "fat": "18g",
        "fiber": "6g",
        "benefits": ["Qisqa foyda 1", "Qisqa foyda 2", "Qisqa foyda 3"]
    }}
    benefits ro'yxati 3-5 ta qisqa izohdan iborat bo'lsin.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        timeout=30,
    )
    data = json.loads(response.choices[0].message.content)

    benefits = data.get("benefits", [])
    if isinstance(benefits, str):
        benefits = [benefits]
    if not isinstance(benefits, list):
        benefits = []

    return {
        "calories": data.get("calories", 0),
        "protein": data.get("protein", "0g"),
        "carbs": data.get("carbs", "0g"),
        "fat": data.get("fat", "0g"),
        "fiber": data.get("fiber", "0g"),
        "benefits": [str(item).strip() for item in benefits if str(item).strip()],
    }
