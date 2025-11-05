from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str
    api_key: str

class ChatResponse(BaseModel):
    response: str
    should_generate: bool = False

class GenerateRequest(BaseModel):
    session_id: str
    api_key: str

class GeneratedFiles(BaseModel):
    openapi_yaml: str
    rules_md: str
    schema_json: str

class ApprovalRequest(BaseModel):
    session_id: str
    approved: bool
    feedback: Optional[str] = None
