import re

PATTERNS = [
    {"type": "AWS_ACCESS_KEY", "re": r"\bAKIA[0-9A-Z]{16}\b"},
    {"type": "AWS_SECRET_KEY_LIKE", "re": r"\b[0-9A-Za-z/+]{40}\b"},
    {"type": "PRIVATE_KEY_BLOCK", "re": r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"},
    {"type": "OPENAI_KEY", "re": r"\bsk-[A-Za-z0-9]{20,}\b"},
    {"type": "EMAIL", "re": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"},
]

def detect_sensitive(text: str) -> list[dict]:
    hits = []
    for p in PATTERNS:
        if re.search(p["re"], text):
            hits.append({"type": p["type"]})
    return hits
