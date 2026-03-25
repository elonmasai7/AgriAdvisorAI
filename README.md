# AgriAdvisor AI ??

## Problem Statement
Smallholder farmers across Africa and South Asia lose a large share of harvests because crop diseases and pests are detected late or diagnosed incorrectly. Extension support is often limited, and laboratory testing is expensive or inaccessible. Farmers need fast, practical, and trustworthy advice in simple language that works with locally available inputs.

## Solution
AgriAdvisor AI is a multimodal advisory web app that lets farmers upload a crop photo and/or describe symptoms in text. The system combines vision analysis, RAG retrieval from a curated disease knowledge base, and reasoning-based advisory generation to produce:
- Probable diagnosis
- Severity level and 1-10 severity score
- Organic, chemical, and cultural treatment options
- Prevention guidance and yield-risk warning
- Follow-up chat support
- English/Swahili response toggle

## Architecture Diagram
```text
Farmer Input (Image + Text)
          |
          v
   [Vision Model - Oxlo]
          |
          v
 [RAG Retriever - ChromaDB]
          |
          v
 [Advisory Model - Oxlo Chat]
          |
          v
 Structured Diagnosis Response
```

## Tech Stack
- Backend: Python 3.11+, FastAPI, OpenAI Python SDK (Oxlo base_url), LangChain, ChromaDB, Pillow, python-dotenv, uvicorn
- Frontend: React 18 (Vite), Tailwind CSS, Axios, React Dropzone, React Markdown
- Data: Local crop disease knowledge base JSON (15+ entries)

## Oxlo.ai API Usage
- Model 1: `${VISION_MODEL}` (configured in `.env`) — Used for crop photo analysis
- Model 2: `${CHAT_MODEL}` (configured in `.env`) — Used for diagnosis generation, translation, and follow-up chat
- Model 3: `${EMBED_MODEL}` (configured in `.env`) — Used for RAG embeddings and retrieval
- API calls per session: minimum 3 (vision + embed + chat), up to 10+ for multi-turn conversations

## Features
- Photo + text crop diagnosis
- RAG-powered knowledge base (15+ diseases)
- Severity scoring (1-10)
- Multi-turn follow-up chat
- English / Swahili language toggle
- Mobile-responsive UI

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Oxlo.ai account and API key (sign up at portal.oxlo.ai)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your OXLO_API_KEY to .env
python disease_db/seed_db.py
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage
1. Open http://localhost:5173
2. Upload a photo of your crop or describe the problem
3. Click Diagnose
4. Review diagnosis, treatment plan, and severity score
5. Ask follow-up questions in the chat window

## Registered Oxlo.ai Email
your-registered-email@example.com

## License
MIT
