from vision import analyze_crop_image
from rag import retrieve_relevant_diseases
from advisor import generate_advisory
from models import DiagnoseResponse, ChatMessage
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL")
)

CHAT_MODEL = os.getenv("CHAT_MODEL")


def run_agent(image_bytes: bytes | None, description: str, language: str) -> DiagnoseResponse:
    vision_result = {}
    if image_bytes:
        vision_result = analyze_crop_image(image_bytes)
    
    query = f"{vision_result.get('crop_type', '')} {vision_result.get('raw_observations', '')} {description}".strip()
    retrieved_diseases = retrieve_relevant_diseases(query)
    
    response = generate_advisory(vision_result, retrieved_diseases, description, language)
    return response


def run_followup(message: str, history: list[ChatMessage], language: str) -> str:
    # Build context from history
    context = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
    
    system_prompt = """You are AgriAdvisor, a compassionate agricultural AI assistant. 
Continue helping the farmer based on their previous diagnosis. Keep answers 
practical, brief, and easy to understand."""
    
    user_message = f"Conversation history:\n{context}\n\nNew question: {message}"
    
    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )
        
        reply = response.choices[0].message.content.strip()
        
        if language == "sw":
            # Translate reply
            translate_prompt = f"Translate the following text to Swahili. Keep it simple and natural. Only return the translated text:\n\n{reply}"
            try:
                trans_resp = client.chat.completions.create(
                    model=CHAT_MODEL,
                    messages=[{"role": "user", "content": translate_prompt}],
                    max_tokens=300
                )
                reply = trans_resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"Translation failed: {e}")
        
        return reply
    
    except Exception as e:
        print(f"Followup failed: {e}")
        return "Sorry, I encountered an error. Please try again."
