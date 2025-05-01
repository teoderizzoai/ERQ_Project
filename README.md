# Elden Ring Quiz

A Streamlit-based quiz application that tests your knowledge of Elden Ring lore, items, and characters.

## Features

- Multiple choice questions about Elden Ring items and lore
- Dynamic question generation using AI
- Score tracking with high score system
- Beautiful UI with game-themed visuals
- Item type categorization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Groq API key in `config/settings.py`

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `quiz/generator.py`: Quiz generation logic
- `data/`: Contains game data and lore
- `images/`: UI assets
- `utils/`: Helper utilities
- `config/`: Configuration files

## Requirements

- Python 3.8+
- Streamlit
- Groq API key

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FromSoftware for creating Elden Ring
- The Elden Ring community for armor set data
- Groq for the AI-powered quiz generation
- Streamlit for the amazing web framework 