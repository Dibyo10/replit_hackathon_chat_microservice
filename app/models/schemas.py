from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str
    

class ChatResponse(BaseModel):
    response: str
    should_generate: bool = False

class GenerateRequest(BaseModel):
    session_id: str
    

class GeneratedFiles(BaseModel):
    openapi_yaml: str
    rules_md: str
    json_schema: str

class ApprovalRequest(BaseModel):
    session_id: str
    approved: bool
    feedback: Optional[str] = None
