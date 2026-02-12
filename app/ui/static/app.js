function el(id){ return document.getElementById(id); }

function showPage(name){
  document.querySelectorAll(".page").forEach(p => p.classList.add("hidden"));
  const page = document.getElementById(`page-${name}`);
  if (page) page.classList.remove("hidden");

  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(`.tab[data-page="${name}"]`).forEach(t => t.classList.add("active"));
}

function setStatus(text, kind="muted") {
  const p = el("statusPill");
  if (!p) return;
  p.textContent = text;
  p.style.borderColor = kind==="ok" ? "#49f0a6" : kind==="bad" ? "#ff6b6b" : "#2a3a72";
}

function prettySignals(obj) {
  const risk = obj.risk_score ?? "-";
  const reasons = (obj.risk_reasons || []).join(", ") || "None";
  const filtered = obj.filtered ? "Yes" : "No";
  const mode = obj.policy_mode ? `Policy: ${obj.policy_mode}` : "";

  return `
    <div style="margin-top:10px;">
      <div><span class="pill">Risk score: ${risk}</span></div>
      <div style="margin-top:8px;"><span class="pill">Reasons: ${reasons}</span></div>
      <div style="margin-top:8px;"><span class="pill">Output redacted: ${filtered}</span></div>
      ${mode ? `<div style="margin-top:8px;"><span class="pill">${mode}</span></div>` : ""}
      ${obj.request_id ? `<div style="margin-top:10px;" class="muted">Request ID: ${obj.request_id}</div>` : ""}
    </div>
  `;
}

async function call(path, opts={}) {
  const base = (el("baseUrl")?.value || "http://127.0.0.1:8000").trim().replace(/\/$/, "");
  const url = base + path;
  const apiKey = (el("apiKey")?.value || "").trim();

  const headers = opts.headers || {};
  if (apiKey) headers["x-api-key"] = apiKey;
  opts.headers = headers;

  const res = await fetch(url, opts);
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch { /* ignore */ }
  return { res, text, json };
}

function explainFor(result, httpStatus) {
  const detail = result?.detail || "";

  if (httpStatus === 400 && String(detail).includes("blocked")) {
    return "Blocked ✅ The gateway detected a prompt-injection pattern and refused to send it to the model (strict policy).";
  }
  if (httpStatus === 429) {
    return "Rate-limited ✅ The gateway is protecting against abuse / denial-of-wallet patterns.";
  }
  if (httpStatus >= 500) {
    return "Upstream error ⚠️ The provider failed. In mock mode this shouldn’t happen; check server logs.";
  }
  if (result?.filtered) {
    return "Allowed, but redacted ✅ The model output contained sensitive patterns and was sanitized before returning.";
  }
  return "Allowed ✅ Prompt passed security checks and returned a normal response.";
}

async function runPrompt() {
  setStatus("Running…");
  if (el("raw")) el("raw").textContent = "";
  if (el("output")) el("output").textContent = "";
  if (el("signals")) el("signals").innerHTML = "";
  if (el("explain")) el("explain").textContent = "";

  const prompt = (el("prompt")?.value || "").trim();
  if (!prompt) { setStatus("Enter a prompt", "bad"); return; }

  const { res, text, json } = await call("/v1/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });

  if (el("raw")) el("raw").textContent = text;

  const status = res.status;
  const payload = json || { detail: text };

  if (el("signals")) el("signals").innerHTML = prettySignals(payload);
  if (el("output")) el("output").textContent = payload.output || payload.detail || text;
  if (el("explain")) el("explain").textContent = explainFor(payload, status);

  if (status >= 200 && status < 300) setStatus("OK", "ok");
  else setStatus(`HTTP ${status}`, "bad");
}

async function runSelftest() {
  setStatus("Selftest…");
  const { res, text, json } = await call("/v1/selftest");
  if (el("raw")) el("raw").textContent = text;

  if (json) {
    if (el("output")) el("output").textContent = `Passed ${json.passed}/${json.total}`;
    if (el("signals")) el("signals").innerHTML = `
      <div style="margin-top:10px;">
        <div><span class="pill">Policy mode: ${json.policy_mode}</span></div>
        <div style="margin-top:8px;"><span class="pill">Mock mode: ${json.mock_mode}</span></div>
        <div style="margin-top:8px;"><span class="pill">Passed: ${json.passed}/${json.total}</span></div>
      </div>
    `;
    if (el("explain")) el("explain").textContent =
      "Selftest automatically validates the gateway controls across attack scenarios (block + redaction + allow).";
  } else {
    if (el("output")) el("output").textContent = text;
  }

  if (res.ok) setStatus("OK", "ok");
  else setStatus(`HTTP ${res.status}`, "bad");
}

async function showPolicy() {
  setStatus("Loading policy…");
  const { res, text, json } = await call("/v1/policy");
  if (el("raw")) el("raw").textContent = text;

  if (json) {
    if (el("output")) el("output").textContent = "Policy loaded (see Raw).";
    if (el("signals")) el("signals").innerHTML = `
      <div style="margin-top:10px;">
        <div><span class="pill">Mock: ${json.mode?.mock_mode}</span></div>
        <div style="margin-top:8px;"><span class="pill">Policy: ${json.mode?.policy_mode}</span></div>
        <div style="margin-top:8px;"><span class="pill">Block threshold: ${json.thresholds?.block_threshold}</span></div>
      </div>
    `;
    if (el("explain")) el("explain").textContent =
      "This manifest lists enabled security controls: auth, rate limiting, DLP, audit logging, and enforcement mode.";
  } else {
    if (el("output")) el("output").textContent = text;
  }

  if (res.ok) setStatus("OK", "ok");
  else setStatus(`HTTP ${res.status}`, "bad");
}

/* Nav + buttons */
document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => showPage(btn.getAttribute("data-page")));
});

document.addEventListener("click", (e) => {
  const ex = e.target.closest("button[data-example]");
  if (ex && el("prompt")) el("prompt").value = ex.getAttribute("data-example");
});

if (el("runBtn")) el("runBtn").addEventListener("click", runPrompt);
if (el("selftestBtn")) el("selftestBtn").addEventListener("click", runSelftest);
if (el("policyBtn")) el("policyBtn").addEventListener("click", showPolicy);

if (el("goDemoBtn")) el("goDemoBtn").addEventListener("click", () => showPage("demo"));
if (el("goTutorialBtn")) el("goTutorialBtn").addEventListener("click", () => showPage("tutorial"));
if (el("goDemoBtn2")) el("goDemoBtn2").addEventListener("click", () => showPage("demo"));

/* Default page */
showPage("home");
