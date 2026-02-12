from app.dlp.detector import detect_sensitive
from app.dlp.redactor import redact_text

def filter_response(text: str) -> dict:
    """
    If response contains sensitive patterns, redact them.
    Enterprise upgrade: add allowlists, context-aware policies, and block modes.
    """
    hits = detect_sensitive(text)
    if not hits:
        return {"text": text, "filtered": False, "hits": []}
    return {"text": redact_text(text, hits), "filtered": True, "hits": [h["type"] for h in hits]}
