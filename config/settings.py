# config/settings.py
import os
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from Streamlit secrets with better error handling
try:
    if "GROQ_API_KEY" in st.secrets:
        API_KEY = st.secrets["GROQ_API_KEY"]
        logger.debug("Successfully loaded API key from secrets")
    else:
        logger.error("GROQ_API_KEY not found in secrets")
        raise KeyError("GROQ_API_KEY not found in secrets")
except Exception as e:
    logger.error(f"Error accessing secrets: {e}")
    raise ValueError("Failed to access API key. Please check your Streamlit Cloud secrets configuration.")

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
