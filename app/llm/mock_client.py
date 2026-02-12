import time

def mock_generate(prompt: str) -> str:
    """
    Offline mock LLM that returns deterministic outputs to test:
    - response DLP filtering (returns secret-like patterns sometimes)
    - prompt injection attempts (returns 'system prompt' leakage sometimes)
    - normal outputs
    """
    p = prompt.lower()

    # Simulate "leakage" to test response filtering
    if "api key" in p or "secret" in p or "token" in p:
        return "Sure. Here is the key you asked for: sk-1234567890abcdefghijklmnopqrstuv"


    if "system prompt" in p or "reveal" in p or "ignore previous" in p:
        return (
            "SYSTEM PROMPT (simulated leakage): "
            "You are a secure assistant. Never reveal secrets."
        )

    if "email" in p:
        return "Contact support at test@example.com for help."

    # Default helpful response
    return (
        "• Prompt injection is when attackers try to override the model’s instructions.\n"
        "• They can try to extract secrets or force unsafe behavior.\n"
        "• Mitigations include input validation, policy enforcement, and output filtering."
    )
