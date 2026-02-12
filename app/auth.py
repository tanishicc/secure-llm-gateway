from fastapi import Request, HTTPException
from app.config import settings

def require_api_key(req: Request) -> str:
    key = req.headers.get("x-api-key")
    if not key:
        raise HTTPException(status_code=401, detail="Missing API key (x-api-key header)")

    allowed = [k.strip() for k in settings.api_keys.split(",") if k.strip()]
    if key not in allowed:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key
