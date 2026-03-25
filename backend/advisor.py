import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from models import DiagnoseResponse
from translator import translate_response

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL")
)

CHAT_MODEL = os.getenv("CHAT_MODEL")


def generate_advisory(vision_result: dict, retrieved_diseases: list[dict], farmer_description: str, language: str) -> DiagnoseResponse:
    system_prompt = """You are AgriAdvisor, an expert AI agricultural advisor helping smallholder 
farmers in Africa and South Asia. You provide accurate, actionable, and 
compassionate advice. Your responses must be practical — only recommend 
treatments using materials available in rural markets.

You have been given:
1. A vision model's analysis of a crop photo
2. Retrieved disease entries from a verified agricultural knowledge base
3. The farmer's own description of the problem

Based on all three, generate a complete diagnosis and advisory report.

Return ONLY a valid JSON object matching this structure:
{
  "crop_detected": "string",
  "disease_identified": "string",
  "confidence": "High" | "Medium" | "Low",
  "severity": "Mild" | "Moderate" | "Severe",
  "severity_score": 1-10,
  "diagnosis_summary": "2-3 sentences, plain language",
  "treatment_plan": {
    "organic": "string",
    "chemical": "string",
    "cultural": "string"
  },
  "prevention_advice": "string",
  "yield_loss_warning": "string",
  "follow_up_questions": ["string", "string", "string"],
  "sources_consulted": ["string", "string"]
}

Be empathetic. This farmer's livelihood depends on your advice."""

    user_message = f"""
Vision Analysis: {json.dumps(vision_result)}

Retrieved Diseases: {json.dumps(retrieved_diseases)}

Farmer Description: {farmer_description}
"""

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        # Strip markdown
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        result = json.loads(result_text)
        diagnose_response = DiagnoseResponse(**result, language="en")
        
        if language == "sw":
            diagnose_response = translate_response(diagnose_response, "sw")
        
        return diagnose_response
    
    except Exception as e:
        print(f"Advisory generation failed: {e}")
        # Return a fallback response
        return DiagnoseResponse(
            crop_detected="Unknown",
            disease_identified="Unable to diagnose",
            confidence="Low",
            severity="Unknown",
            severity_score=5,
            diagnosis_summary="We encountered an error analyzing your crop. Please try again or provide more details.",
            treatment_plan={"organic": "", "chemical": "", "cultural": ""},
            prevention_advice="",
            yield_loss_warning="",
            follow_up_questions=[],
            sources_consulted=[],
            language=language
        )
