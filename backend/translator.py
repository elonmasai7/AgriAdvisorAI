import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from models import DiagnoseResponse

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL", "https://api.oxlo.ai/v1"),
)

CHAT_MODEL = os.getenv("CHAT_MODEL", "oxlo-chat")


def _strip_json_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json") :].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```") :].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    return cleaned


def _translate_structured_fields(payload: dict, target_language: str) -> dict:
    if target_language != "sw":
        return payload

    prompt = (
        "Translate ONLY the values of these keys into Swahili while keeping the same JSON structure and keys: "
        "diagnosis_summary, treatment_plan.organic, treatment_plan.chemical, treatment_plan.cultural, "
        "prevention_advice, yield_loss_warning, follow_up_questions. "
        "Do not translate crop_detected, disease_identified, confidence, severity, sources_consulted, language. "
        "Return JSON only."
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload)},
        ],
    )

    text = response.choices[0].message.content or "{}"
    return json.loads(_strip_json_fences(text))


def translate_response(response: DiagnoseResponse, target_language: str) -> DiagnoseResponse:
    if target_language == "en":
        return response

    try:
        as_dict = response.model_dump()
        translated = _translate_structured_fields(as_dict, target_language)
        translated["language"] = target_language
        return DiagnoseResponse(**translated)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Translation failed: %s", exc)
        fallback = response.model_copy()
        fallback.language = target_language
        return fallback
