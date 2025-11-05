from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.session_manager import get_session, init_session, add_message
from app.services.gemini_service import send_chat
from app.core.prompts import SYSTEM_PROMPT
from app.services.gemini_service import init_chat_model


router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = init_chat_model()

    # Fetch or init session
    session = get_session(req.session_id)
    if not session:
        init_session(req.session_id)
        session = get_session(req.session_id)
        add_message(req.session_id, "user", SYSTEM_PROMPT)

    # Add this user message to history
    add_message(req.session_id, "user", req.message)

    # GENERATE trigger shortcut
    if "GENERATE" in req.message.upper():
        return ChatResponse(
            response="Ready to generate. Call /api/generate",
            should_generate=True
        )

    try:
        # Prepare history for chat model (exclude latest user msg)
        chat_history = session["history"][:-1] if len(session["history"]) > 1 else []

        # Call Gemini
        response_text = send_chat(model, chat_history, req.message)

        # Store model reply
        add_message(req.session_id, "model", response_text)

        return ChatResponse(response=response_text)

    except Exception as e:
        print("🔥 ERROR in /api/chat:", e)
        raise HTTPException(status_code=500, detail=str(e))
