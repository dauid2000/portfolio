/* ==========================================================================
   API client — talks to the Personal API (FastAPI backend).
   --------------------------------------------------------------------------
   The base URL comes from js/apiConfig.js (window.PORTFOLIO_API_BASE):
     - local development:  "http://127.0.0.1:8000"
     - production:         "https://personal-api-xxxx.onrender.com"
     - same-origin deploy: ""  (empty string)
   Exposed as window.PortfolioAPI for js/script.js.
   ========================================================================== */

"use strict";

const API_BASE = window.PORTFOLIO_API_BASE || "";

/* ---------- Small fetch helpers ---------- */

async function getJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

async function postJSON(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res;
}

/* ---------- Public: projects ---------- */

async function getProjects() {
  return getJSON("/api/projects");
}

/* ---------- Public: contact form ---------- */

/* Sends the contact form. Resolves with:
     { ok: true }
     { ok: false, errors: { fieldName: "message" }, message: "..." }
   Throws Error(message) for network failures (script.js shows a toast). */
async function sendContact(payload) {
  let res;
  try {
    res = await postJSON("/api/contact", payload);
  } catch {
    throw new Error("Network error — please try again.");
  }

  if (res.status === 201) return { ok: true };

  let data = {};
  try {
    data = await res.json();
  } catch {
    /* non-JSON error body */
  }

  /* Validation errors: 422 with field-level details from FastAPI */
  if (res.status === 422 && Array.isArray(data.errors)) {
    const errors = {};
    for (const err of data.errors) {
      const field = Array.isArray(err.loc) ? err.loc[err.loc.length - 1] : null;
      if (typeof field === "string" && !errors[field]) {
        errors[field] = err.msg || "Please check this field.";
      }
    }
    return { ok: false, errors, message: "Please check the highlighted fields." };
  }

  return {
    ok: false,
    message:
      (typeof data.detail === "string" && data.detail) ||
      "The message could not be sent. Please try again.",
  };
}

/* ---------- Expose for js/script.js ---------- */

window.PortfolioAPI = { getProjects, sendContact };
