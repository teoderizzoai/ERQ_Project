# config/settings.py
import os
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from Streamlit secrets with better error handling
try:
    # First try to get from secrets
    if hasattr(st, 'secrets') and st.secrets is not None:
        API_KEY = st.secrets.get("GROQ_API_KEY")
        if API_KEY:
            logger.debug("Successfully loaded API key from secrets")
        else:
            # Try environment variable as fallback
            API_KEY = os.environ.get("GROQ_API_KEY")
            if API_KEY:
                logger.debug("Successfully loaded API key from environment variable")
            else:
                raise ValueError("API key not found in secrets or environment variables")
    else:
        # If st.secrets is not available, try environment variable
        API_KEY = os.environ.get("GROQ_API_KEY")
        if API_KEY:
            logger.debug("Successfully loaded API key from environment variable")
        else:
            raise ValueError("st.secrets not available and API key not found in environment variables")
except Exception as e:
    logger.error(f"Error accessing API key: {e}")
    raise ValueError("Failed to access API key. Please check your Streamlit Cloud secrets configuration.")

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
