import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from models import DiagnoseResponse
from translator import translate_response

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


def generate_advisory(
    vision_result: dict,
    retrieved_diseases: list[dict],
    farmer_description: str,
    language: str,
) -> DiagnoseResponse:
    system_prompt = (
        "You are AgriAdvisor, an expert AI agricultural advisor helping smallholder "
        "farmers in Africa and South Asia. You provide accurate, actionable, and "
        "compassionate advice. Your responses must be practical and only recommend "
        "treatments using materials available in rural markets. "
        "You have been given: (1) a vision model analysis of a crop photo, "
        "(2) retrieved disease entries from a verified agricultural knowledge base, "
        "and (3) the farmer description. "
        "Based on all three, generate a complete diagnosis and advisory report. "
        "Return ONLY valid JSON with this structure: "
        "{"
        "crop_detected: string, "
        "disease_identified: string, "
        "confidence: 'High' | 'Medium' | 'Low', "
        "severity: 'Mild' | 'Moderate' | 'Severe', "
        "severity_score: number (1-10), "
        "diagnosis_summary: string, "
        "treatment_plan: {organic: string, chemical: string, cultural: string}, "
        "prevention_advice: string, "
        "yield_loss_warning: string, "
        "follow_up_questions: string[], "
        "sources_consulted: string[]"
        "}. "
        "Be empathetic. This farmer's livelihood depends on your advice."
    )

    user_payload = {
        "vision_result": vision_result,
        "retrieved_diseases": retrieved_diseases,
        "farmer_description": farmer_description,
    }

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload)},
            ],
        )

        content = response.choices[0].message.content or "{}"
        parsed = json.loads(_strip_json_fences(content))
        parsed["language"] = "en"

        advisory = DiagnoseResponse(**parsed)
        if language == "sw":
            advisory = translate_response(advisory, "sw")
        return advisory

    except Exception as exc:  # noqa: BLE001
        logger.exception("Advisory generation failed: %s", exc)

        fallback = DiagnoseResponse(
            crop_detected=vision_result.get("crop_type", "Unknown") or "Unknown",
            disease_identified="Needs further inspection",
            confidence="Low",
            severity="Moderate",
            severity_score=5,
            diagnosis_summary=(
                "I could not complete a reliable diagnosis this time. "
                "Please provide a clearer photo and describe when symptoms started."
            ),
            treatment_plan={
                "organic": "Remove heavily affected leaves and monitor daily.",
                "chemical": "Consult a local extension officer before chemical application.",
                "cultural": "Improve spacing, drainage, and field hygiene immediately.",
            },
            prevention_advice="Use clean seed, rotate crops, and scout early every week.",
            yield_loss_warning="Potential losses may increase if symptoms spread unchecked.",
            follow_up_questions=[
                "When did you first notice these symptoms?",
                "How quickly are the symptoms spreading?",
                "Have you applied any treatment already?",
            ],
            sources_consulted=[
                item.get("id", "knowledge_base") for item in retrieved_diseases[:3]
            ]
            or ["knowledge_base"],
            language="en",
        )

        if language == "sw":
            return translate_response(fallback, "sw")
        return fallback
