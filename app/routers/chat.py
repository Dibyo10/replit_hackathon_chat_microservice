from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.session_manager import get_session, init_session, add_message
from app.services.gemini_service import init_gemini, send_chat
from app.core.prompts import SYSTEM_PROMPT

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = init_gemini(req.api_key)

    session = get_session(req.session_id)
    if not session:
        init_session(req.session_id)
        session = get_session(req.session_id)
        # add persona to session
        add_message(req.session_id, "system", SYSTEM_PROMPT)

    add_message(req.session_id, "user", req.message)

    if "GENERATE" in req.message.upper():
        return ChatResponse(
            response="Ready to generate. Call /api/generate",
            should_generate=True
        )

    try:
        response_text = send_chat(model, session["history"], req.message)
        add_message(req.session_id, "model", response_text)

        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
