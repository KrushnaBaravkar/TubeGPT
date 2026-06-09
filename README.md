# ▶ TubeGPT: RAG-based YouTube Transcript Q&A System

> Ask anything about any YouTube video. TubeGPT fetches the transcript, indexes it into a local vector store, and answers your questions using a fully local LLM — no OpenAI API needed.

## Features

* 🎥 **YouTube Transcript Indexing:** Automatically fetch and index transcripts from any YouTube video URL.
* 🤖 **Powered by Local LLaMA 3.2:** Efficient and private inference using `Ollama` — no API keys required.
* 🔍 **Semantic Search with FAISS:** Retrieves the most relevant transcript chunks using vector similarity search.
* 🧠 **Context Augmentation:** Refines raw retrieved context using LLM before generating the final answer.
* 💬 **Conversational Q&A UI:** Ask multiple questions about the same video without re-indexing.
* 📄 **Transcript Viewer:** Inspect the raw transcript directly inside the app.
* 🛠 **Interactive UI:** Built with Streamlit — no coding knowledge required to use.

---

## 🖥 Demo

> Index a video → Ask questions → Get accurate, context-grounded answers instantly.

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.10+
* Install **Ollama** to run LLaMA 3.2 locally → [https://ollama.com](https://ollama.com)
* Pull the required model:

```bash
ollama pull llama3.2
ollama serve
```

### 📦 Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/KrushnaBaravkar/TubeGPT.git
cd TubeGPT
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file (for future API keys if needed):

```bash
touch .env
```

5. Start the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
TubeGPT/
│
├── app.py                  ← Streamlit UI (entry point)
│
├── indexing.py             ← Stage 1: Fetch transcript → chunk → embed → FAISS
├── retrieval.py            ← Stage 2: Query vector store → return top-K chunks
├── augmentation.py         ← Stage 3: Refine context with LLM before answering
├── generation.py           ← Stage 4: Generate final answer from context
│
├── .env                    ← Environment variables
├── requirements.txt        ← Python dependencies
└── README.md               ← Project documentation
```

---

## 🔄 Application Workflow

### 1. Input & Indexing
   * User pastes a YouTube URL (full URL or bare video ID).
   * Click **"Index Video"** to fetch the transcript and build the vector store.

### 2. Transcript Processing
   * The transcript is split into 1000-character chunks with 200-character overlap.
   * Each chunk is embedded using HuggingFace `all-MiniLM-L6-v2` and stored in a local FAISS index.

### 3. Question & Retrieval
   * User types a question in the chat panel.
   * The pipeline runs similarity search and retrieves the top-K most relevant chunks.

### 4. Augmentation
   * Retrieved context is passed to LLaMA 3.2 to strip irrelevant content and return a clean, focused context.

### 5. Answer Generation
   * The refined context and question are sent to LLaMA 3.2 with a strict prompt.
   * The model answers only from the video content — no hallucination.

### 6. Chat History
   * All questions and answers are stored in session state.
   * Users can ask unlimited follow-up questions without re-indexing.

---

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | UI development |
| Ollama + LLaMA 3.2 | Local LLM inference |
| HuggingFace Sentence Transformers | Text embedding |
| FAISS | Vector store & similarity search |
| LangChain | LLM orchestration & text splitting |
| youtube-transcript-api | YouTube transcript fetching |
| python-dotenv | Environment variable management |

---

## ❗ Notes

* This tool is designed for **local use** to ensure privacy and low latency.
* You must have `Ollama` running with a locally available `llama3.2` model before starting the app.
* Videos **must have captions enabled** — auto-generated captions work fine, but videos with captions fully disabled will not work.
* The FAISS index is **in-memory only** and resets when a new video is indexed or the app is restarted.

---

## 📋 Requirements

```
youtube-transcript-api
langchain
langchain-core
langchain-community
langchain-ollama
langchain-text-splitters
sentence-transformers
faiss-cpu
streamlit
python-dotenv
```

> **Note on FAISS:** Use `faiss-cpu` for standard machines. If you have an NVIDIA GPU, you may use `faiss-gpu` instead for faster indexing.

---

## 📄 License

MIT
