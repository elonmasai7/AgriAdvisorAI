from pydantic import BaseModel
from typing import List, Dict


class DiagnoseRequest(BaseModel):
    description: str  # Farmer's text description of the problem
    language: str = "en"  # "en" or "sw" (Swahili)


class DiagnoseResponse(BaseModel):
    crop_detected: str
    disease_identified: str
    confidence: str  # "High", "Medium", "Low"
    severity: str  # "Mild", "Moderate", "Severe"
    severity_score: int  # 1–10
    diagnosis_summary: str
    treatment_plan: Dict[str, str]  # {organic, chemical, cultural}
    prevention_advice: str
    yield_loss_warning: str
    follow_up_questions: List[str]
    sources_consulted: List[str]
    language: str


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class FollowUpRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage]
    language: str = "en"
