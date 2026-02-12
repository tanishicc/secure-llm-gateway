from app.risk.patterns import INJECTION_PATTERNS, EXFIL_PATTERNS, ROLE_MANIPULATION_PATTERNS
from app.risk.rules import contains_any, looks_obfuscated

def score_prompt(prompt: str) -> dict:
    """
    Explainable v1 scoring:
    returns {score: 0..100, reasons: [..]}
    """
    p = prompt.lower()
    score = 0
    reasons: list[str] = []

    if contains_any(p, INJECTION_PATTERNS):
        score += 30
        reasons.append("PROMPT_INJECTION_PATTERN")

    if contains_any(p, ROLE_MANIPULATION_PATTERNS):
        score += 20
        reasons.append("ROLE_MANIPULATION_PATTERN")

    if contains_any(p, EXFIL_PATTERNS):
        score += 30
        reasons.append("EXFIL_INTENT_PATTERN")

    if looks_obfuscated(prompt):
        score += 15
        reasons.append("OBFUSCATION_HEURISTIC")

    return {"score": min(score, 100), "reasons": reasons}
