from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateRequest, GeneratedFiles, ApprovalRequest
from app.services.session_manager import get_session
from app.services.gemini_service import init_gemini
from app.utils.parser import parse_generated_files

router = APIRouter()

@router.post("/generate", response_model=GeneratedFiles)
async def generate(req: GenerateRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    model = init_gemini(req.api_key)

    transcript = "\n".join([f"{m['role']}: {m['parts'][0]}" for m in session["history"]])

    prompt = f"""
The user has finished defining an API. Based on this conversation:

{transcript}

Generate openapi.yaml, rules.md, schema.json.
"""

    resp = model.generate_content(prompt)
    files = parse_generated_files(resp.text)

    if not files:
        raise HTTPException(status_code=500, detail="File parsing failed")

    session["generated_files"] = files
    session["awaiting_approval"] = True

    return GeneratedFiles(**files)
