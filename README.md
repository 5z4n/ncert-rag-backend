🧠 ApnaNCERT Backend

NCERT-based Retrieval Augmented Generation (RAG) API

This repository contains the backend service for ApnaNCERT, an academic doubt-solving application that answers questions strictly using NCERT textbooks.

The backend:

Indexes NCERT content using embeddings

Retrieves the most relevant textbook chunks

Generates answers using a local LLM (Ollama)

Exposes a REST API consumed by the Flutter app

🚀 Tech Stack

Python 3.10+

FastAPI – API framework

FAISS – Vector similarity search

SentenceTransformers – Embeddings

Ollama – Local LLM inference (offline)

Cloudflare Tunnel – Temporary public access for demos

📁 Project Structure
NCERT_RAG/
├── app/                    # FastAPI application
│   ├── api.py              # API entry point
│   ├── auth.py             # (Optional) Auth logic
│   ├── schemas.py          # Request/response models
│   └── core/
│       └── config.py       # App configuration
│
├── rag/                    # RAG pipeline
│   ├── main/
│   │   ├── embed.py        # Embedding logic
│   │   ├── index.py        # FAISS index builder
│   │   ├── retrieve.py    # Retrieval logic
│   │   └── local_llm.py   # Ollama LLM interface
│   │
│   └── utils/
│       ├── chunker.py
│       ├── ocr.py
│       ├── text_cleaner.py
│       └── text_audit.py
│
├── data/                   # NCERT textbook data
├── models/
│   ├── embedding_model/    # Saved embedding model
│   └── ollama/             # Ollama installer
│
└── README.md

⚙️ Setup Instructions (Local)
1️⃣ Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install dependencies

Install required Python libraries manually:

pip install fastapi uvicorn faiss-cpu sentence-transformers pydantic


(Exact versions are not pinned to keep setup flexible.)

3️⃣ Install & run Ollama

Download Ollama from:
👉 https://ollama.com

Pull a model (example):

ollama pull mistral


Start Ollama:

ollama serve


Ollama runs locally at:

http://localhost:11434

📚 NCERT Ingestion (One-Time)

Ensure cleaned NCERT textbook text files are present inside data/.

Then generate embeddings and the FAISS index:

python rag/main/index.py


This step:

Cleans NCERT text

Chunks content

Generates embeddings

Builds FAISS index

▶️ Run the Backend API

From the project root:

uvicorn app.api:app --host 0.0.0.0 --port 8000


Swagger UI:

http://localhost:8000/docs

🔌 API Endpoint
POST /ask

Request

{
  "question": "What is photosynthesis?",
  "class": "9",
  "subject": "science"
}


Response

{
  "answer": "Photosynthesis is the process by which green plants...",
  "source": {
    "class": "9",
    "subject": "science",
    "file": "chapter_1.txt"
  }
}


✔ Answers are grounded only in NCERT content
✔ Source metadata included for transparency

🌐 Public Access (Cloudflare Tunnel)

To expose the backend temporarily for demos or APK testing:

cloudflared tunnel --url http://localhost:8000


You’ll receive a URL like:

https://xxxxx.trycloudflare.com


Use this URL as the API base URL in the Flutter app.

⚠️ Notes:

Temporary tunnel

Laptop must remain ON

Intended for evaluation & demos

🔐 Authentication

Currently disabled for ease of testing

auth.py included for future JWT / OAuth extension

🧪 Tested With

Flutter Web (Chrome)

Flutter Android APK (real device)

Postman & Swagger UI

🏁 Status

✅ Backend stable
✅ Fully offline LLM
✅ NCERT-grounded answers
✅ APK-compatible
✅ Submission ready

📌 Notes for Evaluators

No paid APIs used

No cloud LLM calls

Entire inference runs locally

Cloudflare Tunnel used only for temporary public access

📜 License

For academic and educational use.
