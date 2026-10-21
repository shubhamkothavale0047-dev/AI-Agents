# ALEX DESIGN STUDIO OS — Web Starter

## Run locally

Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux/Termux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. API documentation: http://127.0.0.1:8000/docs. Health check: http://127.0.0.1:8000/health.

## Deploy the backend + UI to Render

1. Extract this ZIP and push the project folder to a GitHub repository.
2. In Render, choose **New + → Blueprint** and select that repository.
3. Render detects `render.yaml`; confirm deployment.
4. Open the generated `https://...onrender.com` URL.

Render's free service can sleep when idle. Files saved to `/tmp` or local service disk may be ephemeral; export reports after each run. For persistent production history, connect a managed PostgreSQL database and wire it to the job store before relying on persistence.

## Netlify

Netlify can host the `static/` UI, but it cannot run this Python FastAPI server as a normal static site. The easiest complete deployment is Render using `render.yaml`, which hosts both UI and API together. To use Netlify for the frontend, first deploy the backend on Render and then configure the frontend to call that backend URL (CORS and an API base URL setting are not yet configured in this starter).

## Current execution truth

- 64 registered role implementations are orchestrated in dependency order using local template logic.
- The campaign endpoint returns Markdown and JSON deliverables and an execution report.
- This build makes **zero independent live LLM calls**. It does not claim 64 independent AI models, live market research, generated image/video files, PostgreSQL persistence, Redis/Celery workers, authentication, or production-grade multi-user isolation.
- Do not publish generated offer prices or factual claims without client verification.
