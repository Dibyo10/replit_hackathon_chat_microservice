# Replace w/ Redis later, this is just scaffolding
sessions = {}

def get_session(session_id: str):
    return sessions.get(session_id)

def init_session(session_id: str):
    sessions[session_id] = {
        "history": [],
        "generated_files": None,
        "awaiting_approval": False
    }


def add_message(session_id: str, role: str, content: str):
    sessions[session_id]["history"].append({
        "role": role,
        "parts": [{"text":content}]
    })
