from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Pushover API credentials
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")