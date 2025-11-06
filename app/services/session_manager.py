import json
from app.core.redis_client import r

SESSION_EXPIRY_SECONDS = 3600 * 6  # 6 hours per session

def _session_key(session_id: str):
    return f"session:{session_id}"

def get_session(session_id: str):
    data = r.get(_session_key(session_id))
    return json.loads(data) if data else None

def init_session(session_id: str):
    session_data = {
        "history": [],
        "generated_files": None,
        "awaiting_approval": False
    }
    r.setex(_session_key(session_id), SESSION_EXPIRY_SECONDS, json.dumps(session_data))

def add_message(session_id: str, role: str, content: str):
    session = get_session(session_id)
    if not session:
        init_session(session_id)
        session = get_session(session_id)
    session["history"].append({"role": role, "parts": [{"text": content}]})
    r.setex(_session_key(session_id), SESSION_EXPIRY_SECONDS, json.dumps(session))

def save_generated_files(session_id: str, files: dict):
    session = get_session(session_id)
    if not session:
        return
    session["generated_files"] = files
    session["awaiting_approval"] = True
    r.setex(_session_key(session_id), SESSION_EXPIRY_SECONDS, json.dumps(session))

def clear_session(session_id: str):
    r.delete(_session_key(session_id))
