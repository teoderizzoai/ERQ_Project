# utils/scores.py
from config.settings import HIGH_SCORE_FILE

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def update_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))
