# config/settings.py
import os

API_KEY = "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"

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "DB.json")
HIGH_SCORE_FILE = os.path.join(PROJECT_ROOT, "high_score.txt")
