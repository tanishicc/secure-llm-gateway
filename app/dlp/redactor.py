import re
from app.dlp.detector import PATTERNS

def redact_text(text: str, hits: list[dict]) -> str:
    """
    Redact only the patterns we detected to reduce unnecessary masking.
    """
    redacted = text
    for p in PATTERNS:
        if any(h["type"] == p["type"] for h in hits):
            redacted = re.sub(p["re"], f"[REDACTED:{p['type']}]", redacted)
    return redacted
