import base64
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL")
)

VISION_MODEL = os.getenv("VISION_MODEL")


def analyze_crop_image(image_bytes: bytes) -> dict:
    try:
        # Resize image if larger than 1200px
        image = Image.open(io.BytesIO(image_bytes))
        if max(image.size) > 1200:
            image.thumbnail((1200, 1200))
        # Convert to JPEG if PNG
        if image.format == 'PNG':
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            image_bytes = buffer.getvalue()
        
        # Convert to base64
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        
        system_prompt = """You are an expert agricultural pathologist with 20 years of experience 
identifying crop diseases, pests, and nutritional deficiencies in 
Sub-Saharan African and South Asian farming contexts.
Analyze this crop image and return a JSON object with:
{
  crop_type: string,
  visible_symptoms: string[],
  suspected_conditions: string[],
  affected_area_percentage: number,
  confidence_level: 'High' | 'Medium' | 'Low',
  urgent: boolean,
  raw_observations: string
}
Return ONLY valid JSON, no markdown, no explanation."""
        
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_string}"}}
                ]}
            ],
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        # Strip markdown if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        result = json.loads(result_text)
        return result
    
    except Exception as e:
        print(f"Vision analysis failed: {e}")
        return {
            "crop_type": "",
            "visible_symptoms": [],
            "suspected_conditions": [],
            "affected_area_percentage": 0,
            "confidence_level": "Low",
            "urgent": False,
            "raw_observations": "",
            "vision_failed": True
        }
