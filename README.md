# SHL Assessment Recommendation System

An AI-powered conversational recommendation system that helps recruiters identify the most suitable SHL assessments based on hiring requirements. The system uses Retrieval-Augmented Generation (RAG) with FAISS semantic search and Google's Gemini LLM to provide grounded recommendations from the SHL assessment catalog.

---

## Features

- Conversational assessment recommendation
- Multi-turn clarification for incomplete requirements
- Semantic search using Sentence Transformers + FAISS
- Assessment comparison
- Prompt injection and off-topic request protection
- FastAPI REST API
- Ready for deployment on Render

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| LLM | Google Gemini 2.5 Flash |
| Language | Python 3.13 |
| Deployment | Render |

---

## Project Structure

```
shl-assessment-recommender/
│
├── app/
│   ├── api.py
│   ├── chatbot.py
│   ├── config.py
│   ├── conversation.py
│   ├── embeddings.py
│   ├── guardrails.py
│   ├── llm.py
│   ├── load_catalog.py
│   ├── models.py
│   ├── prompts.py
│   ├── retriever.py
│
├── data/
│   ├── catalog.json
│   └── catalog_processed.json
│
├── scripts/
│   ├── preprocess.py
│   └── build_index.py
│
├── vectorstore/
│   ├── faiss.index
│   └── metadata.pkl
│
├── tests/
│
├── main.py
├── requirements.txt
├── render.yaml
└── README.md
```

---

# System Architecture

```
                     User
                       │
                       ▼
                  FastAPI API
                       │
                       ▼
                  Chatbot Agent
                       │
      ┌────────────────┼─────────────────┐
      │                │                 │
      ▼                ▼                 ▼
 Guardrails     Conversation      Retriever
                     │                 │
                     ▼                 ▼
             Conversation State     FAISS
                                       │
                                       ▼
                          Relevant SHL Assessments
                                       │
                                       ▼
                                  Gemini LLM
                                       │
                                       ▼
                                Final Response
```

---

## Retrieval-Augmented Generation (RAG)

The chatbot follows a RAG pipeline:

1. User query
2. Conversation understanding
3. Semantic retrieval using FAISS
4. Retrieve top relevant SHL assessments
5. Gemini generates a grounded response using retrieved context
6. Return recommendations

---

## Setup

### Clone the repository

```bash
git clone https://github.com/PrathamChintawar/shl-assessment-recommender.git

cd shl-assessment-recommender
```

---

### Create virtual environment

```bash
python -m venv shl
```

Activate

Windows

```bash
shl\Scripts\activate
```

Linux/Mac

```bash
source shl/bin/activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file using .env.example

---

## Data Preparation

### Step 1

Place the SHL catalog JSON inside

```
data/catalog.json
```

---

### Step 2

Preprocess catalog

```bash
python -m scripts.preprocess
```

Generates

```
data/catalog_processed.json
```

---

### Step 3

Build FAISS index

```bash
python -m scripts.build_index
```

Generates

```
vectorstore/faiss.index

vectorstore/metadata.pkl
```

---

## Run the API

```bash
uvicorn main:app --reload
```

API

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

### Chat

```
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a mid-level Java developer"
    }
  ]
}
```

Example Response

```json
{
  "reply": "Based on your requirements, here are the most suitable SHL assessments...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "Knowledge"
    }
  ],
  "end_of_conversation": true
}
```

---

## Conversation Features

The chatbot supports:

- Assessment recommendation
- Multi-turn clarification
- Assessment comparison
- Context-aware conversations
- Off-topic request rejection
- Prompt injection protection

---

## Future Improvements

- Hybrid Retrieval (Keyword + Semantic Search)
- Cross-Encoder Re-ranking
- LLM-based intent extraction
- Better comparison workflow
- Conversation memory
- User feedback integration

---

## Author

**Pratham Chintawar**

AI/ML Enthusiast | Machine Learning | NLP | Computer Vision

GitHub: https://github.com/PrathamChintawar

LinkedIn: https://linkedin.com/in/pratham-chintawar

---
