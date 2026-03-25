# AgriAdvisor AI 🌾

## Problem Statement
Smallholder farmers in Africa and South Asia face significant challenges from crop diseases and pests, leading to substantial yield losses and food insecurity. Traditional diagnostic methods are often inaccessible, expensive, or inaccurate, leaving farmers without timely, actionable advice. With climate change exacerbating pest pressures and limited access to agricultural extension services, there's an urgent need for accessible, AI-powered crop advisory tools that can provide accurate diagnoses and practical treatment recommendations.

## Solution
AgriAdvisor AI is a multi-modal AI advisory agent that helps smallholder farmers diagnose crop problems using photos and text descriptions. The system combines computer vision for image analysis, retrieval-augmented generation (RAG) for knowledge-based disease identification, and conversational AI for personalized follow-up advice. All recommendations are tailored to rural market availability and local farming contexts, with support for English and Swahili languages.

## Architecture Diagram
```
[Farmer Input]
     |
     v
[Image + Text] --> [Vision Model] --> [RAG Knowledge Base] --> [Advisory Model] --> [Diagnosis Response]
                        |                    |                        |
                     Oxlo.ai             ChromaDB              Oxlo.ai Chat
```

## Tech Stack

### Backend
- **Python 3.11+** - Core language
- **FastAPI** - REST API framework
- **OpenAI SDK** - Integration with Oxlo.ai API
- **LangChain** - RAG pipeline orchestration
- **ChromaDB** - Local vector store for disease knowledge base
- **Pillow** - Image processing
- **python-dotenv** - Environment variable management
- **uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Dropzone** - File upload component
- **React Markdown** - Markdown rendering

## Oxlo.ai API Usage
- **Vision Model**: `oxlo-vision` - Used for analyzing crop photos to identify visible symptoms, crop type, and affected areas
- **Chat Model**: `oxlo-chat` - Used for generating diagnoses, treatment plans, and follow-up conversations
- **Embedding Model**: `oxlo-embed` - Used for creating vector embeddings of disease knowledge base for RAG retrieval
- **API Calls per Session**: Minimum 3 (vision + embed + chat), up to 10+ for multi-turn conversations
- **Base URL**: `https://api.oxlo.ai/v1` (OpenAI-compatible endpoint)

## Features
- 📸 **Photo-based diagnosis** - Upload crop images for visual analysis
- 💬 **Text description support** - Describe problems when photos aren't available
- 🧠 **RAG-powered knowledge base** - 15+ curated crop diseases with accurate information
- 📊 **Severity scoring** - 1-10 scale with visual indicators
- 💊 **Treatment recommendations** - Organic, chemical, and cultural options
- 🌍 **Multi-language support** - English and Swahili toggle
- 💬 **Follow-up chat** - Conversational AI for additional questions
- 📱 **Mobile-responsive** - Works on smartphones and tablets
- ⚡ **Fast inference** - Local vector search with cloud AI models

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Oxlo.ai account and API key (sign up at [portal.oxlo.ai](https://portal.oxlo.ai))

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
1. Open [http://localhost:5173](http://localhost:5173) in your browser
2. Upload a photo of your crop (optional) or describe the problem in text
3. Select your preferred language (EN/SW)
4. Click "Diagnose" to get AI-powered analysis
5. Review the diagnosis, severity score, and treatment recommendations
6. Ask follow-up questions in the chat window for more detailed advice

## Registered Oxlo.ai Email
your-registered-email@example.com

## License
MIT