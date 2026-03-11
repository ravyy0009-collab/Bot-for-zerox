from dotenv import load_dotenv
import os

load_dotenv()  # only needed if using .env file locally

SUPPORT_BOT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")
AI_BOT_TOKEN = os.getenv("AI_BOT_TOKEN")

SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID"))  # ✅ Correct
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")