import google.generativeai as genai
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT

def init_gemini(key: str):
    genai.configure(api_key=key)
    return genai.GenerativeModel(settings.GEMINI_MODEL)

def send_chat(model, history, message):
    chat = model.start_chat(history=history[:-1])
    response = chat.send_message(message)
    return response.text
