import json
import time
import hashlib
from pathlib import Path

AUDIT_FILE = Path("audit.log.jsonl")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def audit_log(event: dict) -> None:
    """
    Writes structured JSONL events.
    IMPORTANT: Do not log raw prompts/responses by default.
    Use hashes + metadata for auditability without leakage.
    """
    event.setdefault("ts", int(time.time()))
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
