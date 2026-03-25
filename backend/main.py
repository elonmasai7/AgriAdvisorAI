import logging
import os
import time
from collections import defaultdict, deque
from typing import Deque

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from agent import run_agent, run_followup
from models import FollowUpRequest
from rag import initialize_vector_store

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AgriAdvisor AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 10
request_log: dict[str, Deque[float]] = defaultdict(deque)


def _enforce_rate_limit(ip_address: str) -> None:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    bucket = request_log[ip_address]

    while bucket and bucket[0] < window_start:
        bucket.popleft()

    if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in a minute.")

    bucket.append(now)


@app.on_event("startup")
async def startup_event() -> None:
    try:
        initialize_vector_store()
        logger.info("Vector store ready")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Startup vector store initialization failed: %s", exc)


@app.post("/diagnose")
async def diagnose(
    request: Request,
    file: UploadFile | None = File(default=None),
    description: str = Form(...),
    language: str = Form("en"),
):
    client_ip = request.client.host if request.client else "unknown"
    _enforce_rate_limit(client_ip)

    try:
        image_bytes = await file.read() if file else None
        response = run_agent(image_bytes=image_bytes, description=description, language=language)
        return response.model_dump()
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("/diagnose failed: %s", exc)
        raise HTTPException(status_code=500, detail="Diagnosis failed. Please try again.") from exc


@app.post("/followup")
async def followup(request_body: FollowUpRequest):
    try:
        reply = run_followup(
            message=request_body.message,
            history=request_body.conversation_history,
            language=request_body.language,
            diagnosis_context=request_body.diagnosis_context,
        )
        return {"reply": reply}
    except Exception as exc:  # noqa: BLE001
        logger.exception("/followup failed: %s", exc)
        raise HTTPException(status_code=500, detail="Follow-up failed. Please try again.") from exc


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AgriAdvisor AI", "port": os.getenv("PORT", "8000")}
