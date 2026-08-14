import json
import re
from getenv import OPENAI_API_KEY

# The recipe AI key is an OpenRouter key, so the client must talk to the
# OpenRouter endpoint. OpenRouter keys (sk-or-...) do NOT work against
# api.openai.com, which previously made every nutrition request fail.
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _extract_json_object(content):
    """Robustly parse a JSON object from the model reply.

    OpenRouter providers only sometimes honour ``response_format``, so the
    model may wrap the answer in Markdown fences or add surrounding text.
    This strips fences and falls back to the first ``{...}`` block.
    """
    if not content:
        return {}
    text = str(content).strip()

    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except (json.JSONDecodeError, ValueError):
                return {}
    return {}


def calculate_recipe_nutrition(ingredients_text):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    import requests

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

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Try with response_format first, retry once without it, because not all
    # OpenRouter providers honor response_format.
    last_error = None
    data = {}
    for use_json_mode in (True, False):
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
        }
        if use_json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=(5, 60),
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            data = _extract_json_object(content)
            if data:
                break
            raise ValueError("model returned an empty JSON response")
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
            last_error = exc
    else:
        raise RuntimeError(f"Nutrition analysis failed: {last_error}")

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
