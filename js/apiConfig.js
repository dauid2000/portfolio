/* ==========================================================================
   API configuration — the ONLY file you edit per environment.
   --------------------------------------------------------------------------
   Local development:  API running via `uvicorn main:app --reload` on :8000
   Production:         e.g. "https://api.davidmusumali.com"
   Same-origin deploy: ""  (site and API served from the same domain)
   ========================================================================== */

/* Production: Render free-tier web service (FastAPI backend). */
window.PORTFOLIO_API_BASE = "https://personal-api-zo5g.onrender.com";
