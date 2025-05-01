# config/settings.py
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Try to load from .env file first
load_dotenv()

# Then try to get from environment variables
API_KEY = os.environ.get("GROQ_API_KEY")
logger.debug(f"Environment variables: {dict(os.environ)}")
logger.debug(f"API_KEY value: {API_KEY}")

if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set. Please check your Streamlit Cloud environment variables.")

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
