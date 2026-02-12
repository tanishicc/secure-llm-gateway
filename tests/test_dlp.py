from app.dlp.detector import detect_sensitive
from app.dlp.redactor import redact_text

def test_detects_openai_key_like():
    hits = detect_sensitive("my key is sk-1234567890abcdefghijk")
    assert any(h["type"] == "OPENAI_KEY" for h in hits)

def test_redacts_email():
    text = "contact me at test@example.com"
    hits = detect_sensitive(text)
    red = redact_text(text, hits)
    assert "REDACTED:EMAIL" in red
