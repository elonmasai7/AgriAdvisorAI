import os
from openai import OpenAI
from dotenv import load_dotenv
from models import DiagnoseResponse

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OXLO_API_KEY"),
    base_url=os.getenv("OXLO_BASE_URL")
)

CHAT_MODEL = os.getenv("CHAT_MODEL")


def translate_response(response: DiagnoseResponse, target_language: str) -> DiagnoseResponse:
    if target_language == "en":
        return response
    
    fields_to_translate = [
        "diagnosis_summary",
        "treatment_plan",
        "prevention_advice",
        "yield_loss_warning",
        "follow_up_questions"
    ]
    
    translated = response.model_copy()
    
    for field in fields_to_translate:
        value = getattr(response, field)
        if isinstance(value, str):
            prompt = f"Translate the following text to Swahili (Swahili language code: sw). Keep it simple and natural. Only return the translated text, nothing else:\n\n{value}"
            try:
                resp = client.chat.completions.create(
                    model=CHAT_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                translated_text = resp.choices[0].message.content.strip()
                setattr(translated, field, translated_text)
            except Exception as e:
                print(f"Translation failed for {field}: {e}")
        elif isinstance(value, dict):
            # treatment_plan
            new_dict = {}
            for k, v in value.items():
                prompt = f"Translate the following text to Swahili. Keep it simple. Only return the translated text:\n\n{v}"
                try:
                    resp = client.chat.completions.create(
                        model=CHAT_MODEL,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200
                    )
                    new_dict[k] = resp.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Translation failed for treatment_plan {k}: {e}")
                    new_dict[k] = v
            setattr(translated, field, new_dict)
        elif isinstance(value, list):
            # follow_up_questions
            new_list = []
            for item in value:
                prompt = f"Translate the following text to Swahili. Keep it simple. Only return the translated text:\n\n{item}"
                try:
                    resp = client.chat.completions.create(
                        model=CHAT_MODEL,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=100
                    )
                    new_list.append(resp.choices[0].message.content.strip())
                except Exception as e:
                    print(f"Translation failed for question: {e}")
                    new_list.append(item)
            setattr(translated, field, new_list)
    
    translated.language = target_language
    return translated
