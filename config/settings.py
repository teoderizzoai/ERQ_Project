# config/settings.py
import os
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Simple secrets access
try:
    # Access the API key from the secrets section
    API_KEY = st.secrets["secrets"]["GROQ_API_KEY"]
    logger.debug("Successfully loaded API key from secrets")
except Exception as e:
    logger.error(f"Error accessing secrets: {e}")
    logger.error(f"Error type: {type(e)}")
    logger.error(f"st.secrets available: {hasattr(st, 'secrets')}")
    if hasattr(st, 'secrets'):
        logger.error(f"st.secrets type: {type(st.secrets)}")
        try:
            logger.error(f"st.secrets keys: {list(st.secrets.keys())}")
            if "secrets" in st.secrets:
                logger.error(f"nested secrets keys: {list(st.secrets['secrets'].keys())}")
        except Exception as e2:
            logger.error(f"Could not get st.secrets keys: {e2}")
    raise ValueError("Failed to access API key. Please check your Streamlit Cloud secrets configuration.")

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
