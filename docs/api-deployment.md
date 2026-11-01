# API deployment safeguards

The read-only market-data routes do not require a Gemini API key. Only the AI roadmap generation route (`POST /api/v1/roadmaps/generate`) requires the server-side `GEMINI_API_KEY` environment variable and returns HTTP 503 when it is absent.

The `GEMINI_MODEL` setting defaults to `gemini-3.8-flash`, which must be accessible through your project/plan. The API never sends this secret to browser code.

Generated Markdown is returned directly in the POST response. The service **attempts** to cache it in `ROADMAP_OUTPUT_DIR` (default: `web/api/output`), but storage may be read-only or ephemeral on serverless platforms. The GET endpoint for saved roadmaps only retrieves files available to the same runtime; **do not use it as persistent storage**. A durable store needs an explicitly provisioned database or object storage and appropriate authentication.

Role names are converted to a single safe filename component, preventing traversal into unrelated files. CORS allows public read-only origins without browser credentials. The generation route currently has **no application-level authorization or request quota**: use deployment/network protection and provider spending quotas before exposing AI generation publicly. Add API authentication and rate limiting before commercial use.

Offline smoke tests under `tests/` confirm public API import without a Gemini key, missing-key behavior, filename confinement and best-effort persistence. They do not test the live provider or web scraping.
