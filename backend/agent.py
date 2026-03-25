import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from advisor import generate_advisory
from models import ChatMessage, DiagnoseResponse
from rag import retrieve_relevant_diseases
from vision import analyze_crop_image

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL", "https://api.oxlo.ai/v1"),
)

CHAT_MODEL = os.getenv("CHAT_MODEL", "oxlo-chat")


def run_agent(image_bytes: bytes | None, description: str, language: str) -> DiagnoseResponse:
    vision_result: dict = {}
    if image_bytes:
        vision_result = analyze_crop_image(image_bytes)

    query = (
        f"{vision_result.get('crop_type', '')} "
        f"{vision_result.get('raw_observations', '')} "
        f"{description}"
    ).strip()

    retrieved_diseases = retrieve_relevant_diseases(query or description)

    return generate_advisory(
        vision_result=vision_result,
        retrieved_diseases=retrieved_diseases,
        farmer_description=description,
        language=language,
    )


def run_followup(
    message: str,
    history: list[ChatMessage],
    language: str,
    diagnosis_context: dict | None = None,
) -> str:
    system_prompt = (
        "You are AgriAdvisor, a compassionate agricultural AI assistant. "
        "Continue helping the farmer based on their previous diagnosis. "
        "Keep answers practical, brief, and easy to understand."
    )

    context = {
        "diagnosis_context": diagnosis_context or {},
        "conversation_history": [h.model_dump() for h in history],
        "new_message": message,
    }

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(context)},
            ],
        )

        reply = (response.choices[0].message.content or "").strip()

        if language == "sw":
            translation_prompt = (
                "Translate the following text into simple Swahili for smallholder farmers. "
                "Return only the translated text."
            )
            trans = client.chat.completions.create(
                model=CHAT_MODEL,
                temperature=0,
                messages=[
                    {"role": "system", "content": translation_prompt},
                    {"role": "user", "content": reply},
                ],
            )
            reply = (trans.choices[0].message.content or reply).strip()

        return reply

    except Exception as exc:  # noqa: BLE001
        logger.exception("Follow-up call failed: %s", exc)
        if language == "sw":
            return "Samahani, hitilafu imetokea. Tafadhali jaribu tena."
        return "Sorry, something went wrong while processing your follow-up. Please try again."
