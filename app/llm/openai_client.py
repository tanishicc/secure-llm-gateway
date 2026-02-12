from app.config import settings

# Optional import: only used if mock_mode is false
try:
    from openai import AsyncOpenAI
except Exception:
    AsyncOpenAI = None

from app.llm.mock_client import mock_generate

_client = None

def _get_client():
    global _client
    if _client is None:
        if AsyncOpenAI is None:
            raise RuntimeError("OpenAI SDK not available.")
        _client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
    return _client

async def call_llm(prompt: str) -> str:
    """
    If MOCK_MODE=true -> offline deterministic mock output (no APIs).
    Else -> calls OpenAI (requires billing).
    """
    if settings.mock_mode:
        return mock_generate(prompt)

    # Real mode (kept for later)
    client = _get_client()
    resp = await client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
