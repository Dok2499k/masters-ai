# 📚 Dostoevsky Support Bot

Welcome to the **Dostoevsky Support Bot** — your virtual assistant for exploring the philosophical depths, plotlines, and characters in the works of **Fyodor Mikhailovich Dostoevsky**.

This Streamlit-powered chatbot is designed to answer questions **strictly based on Dostoevsky's original texts**. If the answer can't be found in the documents provided, the bot will transparently let you know.

---

## 🚀 Live Demo

👉 **[Try it on Hugging Face Spaces](https://huggingface.co/spaces/Dok2499k/GenAI)**

---

## 💡 Features

- Ask natural language questions about Dostoevsky's works
- Answers are grounded in specific documents and pages (with citations)
- If the bot is unsure, it invites you to create a support ticket
- Tickets are submitted to a real Trello board
- Conversation history is preserved across interactions

---

## 📁 Project Structure

```
📦 Dostoevsky-Support-Bot
├── app.py                  # Main Streamlit UI
├── requirements.txt        # Project dependencies
├── .env.example            # Example environment config
├── utils/                  # Core bot logic
│   ├── qa_system.py        # Vector search + GPT-4o interface
│   ├── ticket_system.py    # Trello integration
│   └── company_info.py     # Sidebar info
├── document_processing/    # PDF loader utils
├── data/                   # 📌 Upload your PDFs here (manually on HF)
└── vectorstore/            # FAISS vector database (created on first run)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://huggingface.co/spaces/Dok2499k/GenAI
cd GenAI
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
Create a `.env` file based on the provided `.env.example`:

```env
OPENAI_API_KEY=your-openai-key
TRELLO_API_KEY=your-trello-key
TRELLO_API_TOKEN=your-trello-token
TRELLO_LIST_ID=your-trello-list-id
```

### 5. Add documents
Create a `data/` folder and add your Dostoevsky `.pdf` files (must be in English for optimal results).

---

## 🧠 How It Works

- PDFs are loaded and split using LangChain
- FAISS indexes the document chunks for fast semantic search
- `gpt-4o` (via OpenAI API) is called with search-relevant context
- Only content **from documents** is used in generation
- A strict system prompt ensures the bot doesn't hallucinate

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — orchestration
- [OpenAI GPT-4o](https://openai.com/) — LLM backend
- [FAISS](https://github.com/facebookresearch/faiss) — vector store
- [Trello API](https://developer.atlassian.com/cloud/trello/) — ticketing
- [Hugging Face Spaces](https://huggingface.co/spaces) — deployment

---

## 📌 Notes for Hugging Face Users

- **PDF files are not tracked by Git due to size.**
- You must **upload your `.pdf` files manually** via the “Files and versions” tab in the Space (inside the `data/` folder).

---