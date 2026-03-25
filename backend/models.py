from typing import Any

from pydantic import BaseModel


class DiagnoseRequest(BaseModel):
    description: str
    language: str = "en"


class DiagnoseResponse(BaseModel):
    crop_detected: str
    disease_identified: str
    confidence: str
    severity: str
    severity_score: int
    diagnosis_summary: str
    treatment_plan: dict[str, str]
    prevention_advice: str
    yield_loss_warning: str
    follow_up_questions: list[str]
    sources_consulted: list[str]
    language: str


class ChatMessage(BaseModel):
    role: str
    content: str


class FollowUpRequest(BaseModel):
    message: str
    conversation_history: list[ChatMessage]
    language: str = "en"
    diagnosis_context: dict[str, Any] | None = None
