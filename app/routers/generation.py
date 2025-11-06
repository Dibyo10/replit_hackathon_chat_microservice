from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from app.models.schemas import GenerateRequest, GeneratedFiles
from app.services.session_manager import get_session
from app.services.gemini_service import init_generate_model
from app.utils.parser import parse_generated_files


router = APIRouter()

@router.post("/generate", response_model=GeneratedFiles)
async def generate(req: GenerateRequest):
    """
    Generate OpenAPI spec, rules.md, and schema.json
    based on the ongoing chat session conversation.
    Uses gemini-2.5-pro (heavy model).
    """
    try:
        session = get_session(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        model = init_generate_model()

       
        transcript = "\n".join([
            f"{m['role']}: {m['parts'][0]['text']}"
            for m in session["history"]
            if m.get("parts") and isinstance(m["parts"], list) and "text" in m["parts"][0]
        ])

        prompt = f"""
The user has finished defining an API. Based on this conversation:

{transcript}

Generate the following three files in exactly this format:

---FILE: openapi.yaml---
[OpenAPI 3.0 specification with endpoints, schemas, parameters, responses, and auth]
---END FILE---

---FILE: rules.md---
[Markdown rules and conventions: naming, error handling, rate limiting, auth, etc.]
---END FILE---

---FILE: schema.json---
[Strict JSON Schema definitions for all entities]
---END FILE---
"""

        resp = model.generate_content(prompt)

        if not hasattr(resp, "text") or not resp.text:
            raise HTTPException(status_code=500, detail="Model returned empty response")

        files = parse_generated_files(resp.text)

        if not files:
            
            print("⚠️ parse_generated_files failed, raw snippet:", resp.text[:500])
            return GeneratedFiles(
                openapi_yaml="",
                rules_md="Model not ready to generate. Finish conversation phase.",
                schema_json=resp.text[:1000]
            )

        
        session["generated_files"] = files
        session["awaiting_approval"] = True

        return GeneratedFiles(**files)

    except Exception as e:
        print("ERROR in /api/generate:", e)
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/files/{session_id}/openapi", response_class=PlainTextResponse)
async def get_openapi_file(session_id: str):
    session = get_session(session_id)
    if not session or not session.get("generated_files"):
        raise HTTPException(status_code=404, detail="OpenAPI file not found or not generated yet.")
    return PlainTextResponse(session["generated_files"].get("openapi_yaml", ""), media_type="text/yaml")


@router.get("/files/{session_id}/rules", response_class=PlainTextResponse)
async def get_rules_file(session_id: str):
    session = get_session(session_id)
    if not session or not session.get("generated_files"):
        raise HTTPException(status_code=404, detail="Rules file not found or not generated yet.")
    return PlainTextResponse(session["generated_files"].get("rules_md", ""), media_type="text/markdown")


@router.get("/files/{session_id}/schema", response_class=PlainTextResponse)
async def get_schema_file(session_id: str):
    session = get_session(session_id)
    if not session or not session.get("generated_files"):
        raise HTTPException(status_code=404, detail="Schema file not found or not generated yet.")
    return PlainTextResponse(session["generated_files"].get("schema_json", ""), media_type="application/json")
