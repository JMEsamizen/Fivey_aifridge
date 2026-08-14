import requests
import base64
import json
from datetime import datetime
from getenv import API_KEY as AI_KEY


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
            "model": "openai/gpt-4o-mini",
            "max_tokens": 700,

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

Example:

[
    {
        "name": "Milk",
        "quantity": 2,
        "expire_date": "2026-08-20"
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
            timeout=(5, 45),
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        products = json.loads(content)
        if not isinstance(products, list):
            return []
        return products
    except (requests.RequestException, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError):
        return []
