# config/settings.py
import os
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from Streamlit secrets
API_KEY = st.secrets["GROQ_API_KEY"]

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
