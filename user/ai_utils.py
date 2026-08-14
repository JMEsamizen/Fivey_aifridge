import requests
import base64
import json
from getenv import API_KEY as AI_KEY


def analyze_media(file):
    file_bytes = file.read()
    content_type = file.content_type

    if not content_type.startswith("image"):
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

            "max_tokens": 500,

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

Each product must have:
- "name": product name
- "quantity": integer quantity

Example:
[
    {"name": "Milk", "quantity": 2},
    {"name": "Eggs", "quantity": 12},
    {"name": "Apple", "quantity": 5},
    {"name": "Cheese", "quantity": 1}
]

If you are unsure about a product, still include it.
If you cannot determine the quantity, use 1.
"""
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What food products are in this fridge?"
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
        }
    )

    data = response.json()

    if "choices" not in data:
        print("AI ERROR:", data)
        return []

    content = data["choices"][0]["message"]["content"]

    try:
        products = json.loads(content)

        if not isinstance(products, list):
            return []

        return products

    except json.JSONDecodeError:
        print("AI returned invalid JSON:")
        print(content)
        return []
