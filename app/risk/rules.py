def contains_any(text_lower: str, patterns: list[str]) -> bool:
    return any(p in text_lower for p in patterns)

def looks_obfuscated(text: str) -> bool:
    """
    Lightweight obfuscation heuristic:
    - Very long strings
    - Large base64-ish blobs
    """
    if len(text) > 4000:
        return True
    import re
    return re.search(r"[A-Za-z0-9+/]{300,}={0,2}", text) is not None
