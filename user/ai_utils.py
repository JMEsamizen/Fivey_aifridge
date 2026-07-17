#AI message
import requests
import base64
from getenv import OPENROUTER_API_KEY as AI_KEY




def analyze_media(file):

    file_bytes = file.read()

    content_type = file.content_type


    if not content_type.startswith("image"):
        return "Пока поддерживаются только изображения."


    encoded_file = base64.b64encode(
        file_bytes
    ).decode("utf-8")


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
        You are an AI that identifies products in a refrigerator from images. 
        Your response should only include the list of products.

        Response only with the list of products and their quantities.
        Do not include any additional information.

        Response format:

        🥛 Milk - 2
        🥚 Eggs - 12
        🍎 Apple - 5
        🧀 Cheese - 1

        If you are not sure about a product, mark it as "not sure".
        """
    },

    {
        "role": "user",
        "content": [

            {
                "type": "text",
                "text": "What products are in this fridge?"
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


    if "choices" in data:
        return data["choices"][0]["message"]["content"]


    return "Error AI: " + str(data)