from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent, run_followup
from models import FollowUpRequest
from rag import initialize_vector_store

app = FastAPI(title="AgriAdvisor AI", description="AI-powered crop advisory for farmers")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup_event():
#     initialize_vector_store()


@app.post("/diagnose")
async def diagnose(
    file: UploadFile=File(None),
    description: str=Form(...),
    language: str=Form("en")
):
    # Initialize vector store if not done
    try:
        initialize_vector_store()
    except:
        pass  # Skip if no API key
    
    image_bytes = None
    if file:
        image_bytes = await file.read()
    
    response = run_agent(image_bytes, description, language)
    return response


@app.post("/followup")
async def followup(request: FollowUpRequest):
    reply = run_followup(request.message, request.conversation_history, request.language)
    return {"reply": reply}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AgriAdvisor AI"}
