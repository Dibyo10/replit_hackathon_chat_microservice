from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.session_manager import get_session, init_session, add_message
from app.services.gemini_service import send_chat
from app.core.prompts import SYSTEM_PROMPT
from app.services.gemini_service import init_chat_model
from app.services.gemini_service import send_chat_stream
from starlette.responses import StreamingResponse


router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = init_chat_model()

    
    session = get_session(req.session_id)
    if not session:
        init_session(req.session_id)
        session = get_session(req.session_id)
        add_message(req.session_id, "user", SYSTEM_PROMPT)

    
    add_message(req.session_id, "user", req.message)

    
    if "GENERATE" in req.message.upper():
        return ChatResponse(
            response="Ready to generate. Call /api/generate",
            should_generate=True
        )

    try:
        
        chat_history = session["history"][:-1] if len(session["history"]) > 1 else []

        
        response_text = send_chat(model, chat_history, req.message)

        
        add_message(req.session_id, "model", response_text)

        return ChatResponse(response=response_text)

    except Exception as e:
        print("ERROR in /api/chat:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chat/stream")
async def stream_chat(req: ChatRequest):

    try:
        model=init_chat_model()

        session = get_session(req.session_id)
        if not session:
            init_session(req.session_id)
            session = get_session(req.session_id)
            add_message(req.session_id, "user", SYSTEM_PROMPT)

        add_message(req.session_id, "user", req.message)

        def token_generator():
            for token in send_chat_stream(model, session["history"][:-1], req.message):
                yield token
            yield "\n[STREAM_END]\n"

        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))