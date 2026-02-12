#  Secure LLM Gateway (Enterprise AI Security Layer)

An enterprise-ready security middleware that protects Large Language Model (LLM) applications from prompt injection, data exfiltration, abuse, and insecure logging.

Built with FastAPI and designed to simulate production-grade AI security controls.

---

##  Why This Project Exists

As organizations rapidly adopt LLM-powered features, most applications lack:

- Prompt injection protection
- Data Loss Prevention (DLP)
- Rate limiting (deny-of-wallet protection)
- Structured audit logging
- Policy enforcement layers

This project demonstrates how to wrap LLM calls inside a secure control plane before exposing them to users.

---

##  Architecture

Client  
↓  
Secure LLM Gateway  
↓  
LLM Provider (Mock or OpenAI)

The Gateway enforces:

-  Authentication (`x-api-key`)
-  Rate limiting (per client + per IP)
-  Prompt risk scoring (rule-based engine)
-  Strict policy enforcement
-  Input + output DLP redaction
-  Structured audit logging (JSONL)

---

##  Security Controls Implemented

### 1️ Prompt Injection Detection
Detects patterns such as:
- "Ignore previous instructions"
- "Reveal system prompt"
- "Show API key"

Blocks malicious prompts in strict mode.

---

### 2️ Data Loss Prevention (DLP)

Detects and redacts:
- API keys
- Emails
- Private key blocks

Prevents sensitive data leakage into:
- Model responses
- Audit logs

---

### 3️ Policy Enforcement

Modes:
- `strict` → Blocks injection attempts
- `monitor` → Logs but allows

---

### 4️ Audit Logging

- Stored in `audit.log.jsonl`
- No raw secrets stored
- Includes:
  - Risk score
  - Risk reasons
  - Metadata
  - Redaction indicators

Designed for SIEM ingestion.

---

### 5️ Mock Mode (Offline Demo)

The gateway supports a mock LLM provider so you can:
- Demonstrate security controls
- Run self-tests
- Avoid API costs

Switch to real OpenAI provider via `.env`.

---

##  Self-Test Endpoint

```bash
GET /v1/selftest
