import base64
import io
import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL", "https://api.oxlo.ai/v1"),
)

VISION_MODEL = os.getenv("VISION_MODEL", "oxlo-vision")


def _strip_json_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json") :].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```") :].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    return cleaned


def _prepare_image_bytes(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))

    if max(image.size) > 1200:
        image.thumbnail((1200, 1200))

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=88, optimize=True)
    return output.getvalue()


def analyze_crop_image(image_bytes: bytes) -> dict:
    fallback = {
        "crop_type": "",
        "visible_symptoms": [],
        "suspected_conditions": [],
        "affected_area_percentage": 0,
        "confidence_level": "Low",
        "urgent": False,
        "raw_observations": "",
        "vision_failed": True,
    }

    try:
        processed_bytes = _prepare_image_bytes(image_bytes)
        base64_image = base64.b64encode(processed_bytes).decode("utf-8")

        system_prompt = (
            "You are an expert agricultural pathologist with 20 years of experience "
            "identifying crop diseases, pests, and nutritional deficiencies in "
            "Sub-Saharan African and South Asian farming contexts. "
            "Analyze this crop image and return a JSON object with: "
            "{"
            "crop_type: string, "
            "visible_symptoms: string[], "
            "suspected_conditions: string[], "
            "affected_area_percentage: number, "
            "confidence_level: 'High' | 'Medium' | 'Low', "
            "urgent: boolean, "
            "raw_observations: string"
            "}. "
            "Return ONLY valid JSON, no markdown, no explanation."
        )

        response = client.chat.completions.create(
            model=VISION_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        }
                    ],
                },
            ],
        )

        content = response.choices[0].message.content or "{}"
        parsed = json.loads(_strip_json_fences(content))
        parsed["vision_failed"] = False
        return parsed

    except Exception as exc:  # noqa: BLE001
        logger.exception("Vision analysis failed at %s: %s", __name__, exc)
        return fallback
