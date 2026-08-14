import json
from getenv import OPENAI_API_KEY


def calculate_recipe_nutrition(ingredients_text):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
    Quyidagi ingredientlar ro'yxatiga asoslanib umumiy kaloriya, oqsil (protein), uglevod (carbs) va yog' (fat) miqdorini hisoblab ber:
    "{ingredients_text}"

    JAVOBNI FAQAT SHU JSON FORMATIDA QAYTAR (boshqa matn yoza ma):
    {{
        "calories": 420,
        "protein": "24g",
        "carbs": "32g",
        "fat": "18g"
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        timeout=30,
    )
    data = json.loads(response.choices[0].message.content)
    return {
        "calories": data.get("calories", 0),
        "protein": data.get("protein", "0g"),
        "carbs": data.get("carbs", "0g"),
        "fat": data.get("fat", "0g"),
    }
