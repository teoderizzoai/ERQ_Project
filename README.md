# 🎮 Elden Ring Quiz with RAG

This project is my personal attempt to **understand how Retrieval-Augmented Generation (RAG)** works by implementing a practical application: an Elden Ring quiz generator that combines game data with deep lore understanding.

## 🎯 What I Built

An interactive quiz application that demonstrates RAG in action:

- ✅ **Data Processing Pipeline**
  - Parsed and chunked Elden Ring lore text
  - Implemented custom text chunking with overlap
  - Built a JSON-based item database with descriptions and metadata

- ✅ **RAG Implementation**
  - Created a custom text processor for context retrieval
  - Implemented relevance scoring for chunk selection
  - Combined item metadata with retrieved lore context

- ✅ **Quiz Generation**
  - Used Groq LLM for question generation
  - Implemented retry logic and rate limiting
  - Built context-aware question formatting

- ✅ **Interactive UI**
  - Streamlit-based web interface
  - Dynamic scoring system
  - Category-based filtering
  - Themed visual feedback

## 🧠 How It Works

### 1. Text Processing (`text_processor.py`)
```python
def get_context_for_query(query: str, num_chunks: int = 2) -> str:
    chunker = TextChunker()
    chunker.load_text(lore_file)
    relevant_chunks = chunker.get_relevant_chunks(query, num_chunks)
    return "\n\n---\n\n".join(chunk for _, chunk in relevant_chunks)
```

### 2. Quiz Generation (`quiz/generator.py`)
```python
def generate_quiz(items):
    # Select random item
    quiz_item = select_random_item(items)
    
    # Get relevant lore context
    additional_context = get_context_for_query(quiz_item['name'])
    
    # Generate question using combined context
    response = call_groq_api(prompt_with_context)
    
    return parse_quiz(response)
```

## 🛠 Technical Stack

- **Frontend**: Streamlit
- **LLM Integration**: Groq API
- **Data Storage**: JSON + Text Files
- **Text Processing**: Custom chunking implementation
- **Scoring**: File-based persistence

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/elden-ring-quiz.git
cd elden-ring-quiz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Groq API key:
```bash
# In config/settings.py
API_KEY = "your-groq-api-key"
```

4. Run the application:
```bash
streamlit run app.py
```

## 📁 Project Structure

```
elden_ring_quiz/
├── app.py                 # Main Streamlit application
├── config/
│   └── settings.py       # Configuration and API keys
├── data/
│   ├── DB.json          # Item database
│   └── lore.txt         # Lore context for RAG
├── quiz/
│   └── generator.py     # Quiz generation with RAG
├── utils/
│   └── text_processor.py # Custom text chunking
└── images/              # UI assets
```

## 🎓 What I Learned

- How to implement RAG without high-level libraries
- Effective text chunking strategies
- LLM prompt engineering for quiz generation
- Rate limiting and error handling for API calls
- Streamlit UI best practices

## 🔜 Future Improvements

- [ ] Implement proper vector embeddings using sentence-transformers
- [ ] Add FAISS for faster context retrieval
- [ ] Integrate local LLM options
- [ ] Add more sophisticated chunking algorithms
- [ ] Implement caching for frequent queries

## 📝 License

MIT License - feel free to use this code for your own RAG experiments! 