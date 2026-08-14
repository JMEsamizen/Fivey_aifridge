import requests
import base64
import json
import re
from datetime import datetime
from getenv import API_KEY as AI_KEY


class AIServiceError(Exception):
    """Raised when the AI provider itself fails (network, auth, bad response)."""


def _extract_json(content):
    """Robustly parse the JSON array from the model's reply.

    Models sometimes wrap the answer in Markdown code fences or add extra
    prose around the JSON, so a plain ``json.loads`` is not enough. This
    helper strips fences and falls back to the first ``[...]`` block.
    """
    if not content:
        return []

    text = str(content).strip()

    # Remove Markdown code fences (```json ... ```) if present.
    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return []
        try:
            data = json.loads(match.group(0))
        except (json.JSONDecodeError, ValueError):
            return []

    if isinstance(data, list):
        return data

    # Some models return a wrapper object instead of a bare array.
    if isinstance(data, dict):
        for key in ("products", "items", "data", "results"):
            if isinstance(data.get(key), list):
                return data[key]

    return []


def analyze_media(file):
    try:
        file_bytes = file.read()
        content_type = file.content_type
        if not content_type or not content_type.startswith("image"):
            return []

        encoded_file = base64.b64encode(file_bytes).decode("utf-8")
        response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        },

        json={
            # NOTE: openai/gpt-4o-mini is text-only and cannot "see" images,
            # which is why real fridge photos were never recognised. A
            # vision-capable model is required to analyse photos.
            "model": "google/gemini-2.5-flash",
            "max_tokens": 12000,

            "messages": [
                {
                    "role": "system",
                    "content": """
You identify food products in refrigerator images.

Return ONLY valid JSON.
Do not use Markdown.
Do not use ```json.
Do not add explanations.

The response MUST be a JSON array.

Each product MUST have:

- "name": product name
- "quantity": integer quantity
- "expire_date": expiration date in YYYY-MM-DD format
- "calories": estimated calories for one serving, as a number
- "protein": estimated protein in grams for one serving, as a number
- "carbs": estimated carbohydrates in grams for one serving, as a number
- "fat": estimated fat in grams for one serving, as a number
- "benefits": a short, plain-text description of nutritional benefits
- "warnings": a short dietary warning, or an empty string when there is none

Example:

[
    {
        "name": "Milk",
        "quantity": 2,
        "expire_date": "2026-08-20",
        "calories": 61,
        "protein": 3.2,
        "carbs": 4.8,
        "fat": 3.3,
        "benefits": "Source of calcium and protein.",
        "warnings": "Contains lactose."
    },
    {
        "name": "Eggs",
        "quantity": 12,
        "expire_date": "2026-09-01"
    },
    {
        "name": "Apple",
        "quantity": 5,
        "expire_date": null
    }
]

IMPORTANT:

If the expiration date is visible on the package, return it.

If the expiration date cannot be determined from the image,
return null.

NEVER invent an expiration date.

If quantity cannot be determined, use 1.

Nutrition values are estimates. Never claim a medical benefit. Warnings must be
short, factual and limited to common allergens or dietary considerations.

If you are unsure about a product, still include it.
"""
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identify all food products in this fridge and determine their expiration dates if visible."
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{encoded_file}"
                            }
                        }
                    ]
                }
            ]
            },
            timeout=(5, 60),
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return _extract_json(content)
    except requests.RequestException as exc:
        raise AIServiceError(f"AI service request failed: {exc}") from exc
    except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise AIServiceError(f"AI service returned an unexpected response: {exc}") from exc
