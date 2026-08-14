import os
from dotenv import load_dotenv

load_dotenv()

# Fridge photo analysis key (OpenRouter). Your .env stores it as OPENAI_1_API_KEY.
API_KEY = os.getenv("OPENAI_1_API_KEY") or os.getenv("API_KEY")
# Recipes / calorie analysis key (OpenRouter). Your .env stores it as OPENAI_2_API_KEY.
OPENAI_API_KEY = os.getenv("OPENAI_2_API_KEY") or os.getenv("OPENAI_API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
