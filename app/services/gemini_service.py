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

def send_chat_stream(model, history, message):
    """
    Streaming version of send_chat().
    Yields tokens progressively as the Gemini model sends them.
    """
    chat = model.start_chat(history=history)

    try:
        stream = chat.send_message(message, stream=True)

        for chunk in stream:
            
            if hasattr(chunk, "candidates") and chunk.candidates:
                candidate = chunk.candidates[0]
                if candidate.content.parts:
                    part = candidate.content.parts[0]
                    if hasattr(part, "text"):
                        yield part.text
    except Exception as e:
        if "quota" in str(e).lower():
            yield "⚠️ Rate limit hit (free tier). Wait 1 min or switch to billing."
        else:
            yield f"[ERROR] {str(e)}"

def send_generation(model, history):

    try:
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") and response.text else str(response)
    except Exception as e:
        if "quota" in str(e).lower():
            return "⚠️ Rate limit hit (free tier). Wait 1 min or switch to billing."
        raise