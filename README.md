# 🎮 [Elden Ring Quiz with RAG](https://erqproject-8ykkmud3dzdnzkwjqyggf3.streamlit.app/)


![Main Menu Screenshot](https://i.imgur.com/ub0HDLG.png)

This project is my personal attempt to **understand how Retrieval-Augmented Generation (RAG)** works by building a practical application:  
a **personalized quiz generator** for *Elden Ring*, combining structured item data with contextual in-game lore.

Every quiz is:
- 🧠 **Personalized** based on a specific item (weapons, NPCs, places, etc.)
- 📖 Based only on **in-game text and descriptions**
- 🎓 Educational — each answer comes with a short **explanation**, so you learn something new every time!

---

## 🎯 What I Built

An interactive quiz app that demonstrates RAG in action:

- ✅ **Data Processing**
  - Parsed and chunked *Elden Ring* lore text
  - Implemented custom text chunking with overlap
  - Built a JSON-based item database with names, types, and descriptions

- ✅ **Retrieval-Augmented Generation**
  - Custom text retriever with relevance scoring
  - Retrieved relevant lore chunks based on the selected item
  - Combined lore context + metadata to form a prompt

- ✅ **Quiz Generation**
  - Called a Groq-hosted LLM to generate the quiz
  - Included retry logic and rate limiting
  - Structured the response with question + answer + explanation

- ✅ **Interactive UI**
  - Streamlit-based web interface
  - Themed visual feedback and score tracking
  - Item-type filtering for focused quizzes

---

## 🖼️ Example Question

![Question Screenshot](https://i.imgur.com/36Nj2Fn.png)

---

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
    quiz_item = select_random_item(items)
    additional_context = get_context_for_query(quiz_item['name'])
    response = call_groq_api(prompt_with_context)
    return parse_quiz(response)
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **LLM Integration**: Groq API  
- **Storage**: JSON files + raw text  
- **Text Retrieval**: Custom scoring-based chunk retriever  
- **State & Logic**: Python

---

## 🚀 Getting Started

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/elden-ring-quiz.git
cd elden-ring-quiz
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add your Groq API key**
```python
# Inside config/settings.py
API_KEY = "your-groq-api-key"
```

4. **Launch the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
elden_ring_quiz/
├── app.py                 # Main Streamlit app
├── config/
│   └── settings.py        # API key & config
├── data/
│   ├── DB.json            # Item metadata
│   └── lore.txt           # Game lore context
├── quiz/
│   └── generator.py       # RAG logic
├── utils/
│   └── text_processor.py  # Chunking & scoring
└── images/                # Screenshots & UI assets
```

---

## 🎓 What I Learned

- How to implement RAG **without external vector libraries**
- How to design a **custom chunking + scoring system**
- Crafting structured prompts for **LLM-based quiz generation**
- Managing **rate limits, retries**, and API stability
- Building themed, interactive apps with **Streamlit**

---

## 🔮 Future Plans

- [ ] Switch to **vector embeddings** via `sentence-transformers`
- [ ] Integrate **FAISS** for semantic retrieval
- [ ] Support **local LLMs** (Ollama, LM Studio)
- [ ] Implement smarter **semantic chunk splitting**
- [ ] Add **query caching** to improve speed

---

## 📝 License

MIT License – feel free to use, modify, and share.
