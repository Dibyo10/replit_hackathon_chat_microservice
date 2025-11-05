import re

def parse_generated_files(text: str):
    files = {}
    pattern = r'---FILE:\s*(.+?)---\s*([\s\S]*?)\s*---END FILE---'
    matches = re.finditer(pattern, text)

    for m in matches:
        name = m.group(1).lower()
        content = m.group(2).strip()

        if "openapi" in name:
            files["openapi_yaml"] = content
        elif "rules" in name:
            files["rules_md"] = content
        elif "schema" in name:
            files["schema_json"] = content

    return files if len(files) == 3 else None
