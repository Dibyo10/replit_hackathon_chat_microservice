import google.generativeai as genai
from app.core.config import settings

def init_chat_model():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)

def init_generate_model():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(settings.GEMINI_GENERATE_MODEL)

def send_chat(model, history, message):
    chat = model.start_chat(history=history)
    try:
        resp = chat.send_message(message)
        return resp.text if hasattr(resp, "text") and resp.text else str(resp)
    except Exception as e:
        if "quota" in str(e).lower():
            return "⚠️ Rate limit hit (free tier). Wait 1 min or switch to billing."
        raise
