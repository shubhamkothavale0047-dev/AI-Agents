# ALEX DESIGN STUDIO OS — Deployment Guide

## Run Locally

**Python 3.11+ required.**

```bash
# 1. Clone the repository
git clone https://github.com/shubhamkothavale0047-dev/AI-Agents.git
cd AI-Agents

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Copy and edit environment variables
cp .env.example .env

# 5. Start the dev server
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**

| Endpoint | Description |
|---|---|
| `http://127.0.0.1:8000` | Web UI |
| `http://127.0.0.1:8000/docs` | Swagger / OpenAPI |
| `http://127.0.0.1:8000/redoc` | ReDoc |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/api/agents` | List all 64 roles |

---

## Deploy to Render (Recommended)

1. Push this repository to GitHub (already done ✅)
2. Go to **https://dashboard.render.com** → **New + → Web Service**
3. Connect your `AI-Agents` repository
4. Use these settings:

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

5. Add environment variables in the Render dashboard:

| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.12.8` |
| `ALEX_OUTPUT_DIR` | `/tmp/alex_outputs` |
| `OPENAI_API_KEY` | *(optional — only if using OpenAI mode)* |

> **Note:** Render's free tier sleeps after 15 minutes of inactivity. Files written to disk are ephemeral — download reports immediately after each run, or connect a PostgreSQL database for persistence.

Alternatively, use **Blueprint** auto-detection — Render will read `render.yaml` automatically:
- **New + → Blueprint** → select this repository → deploy

---

## PostgreSQL (Optional — Persistent Job History)

To persist job results across Render restarts:

1. Create a **Render PostgreSQL** database (free tier available)
2. Copy the **Internal Database URL** from Render
3. Add it as an environment variable: `DATABASE_URL=postgresql://...`
4. The `PostgresJobStore` in `alex_design_studio_os/postgres_store.py` will auto-initialise the schema

---

## OpenAI Mode (Optional)

To enable live AI generation via the CLI:

```bash
export OPENAI_API_KEY=sk-...
python -m alex_design_studio_os --mode openai --workflow core \
  --brief "Bappu's Biryani — premium Instagram campaign"
```

---

## Execution Transparency

- 64 registered role implementations are orchestrated in dependency order using local template logic.
- The campaign endpoint returns Markdown and JSON deliverables plus a full execution report.
- **This build makes zero independent live LLM calls** by default.
- It does not claim 64 independent AI models, live market research, or generated image/video files.
- Do **not** publish generated offer prices or factual claims without client verification.


## ALEX ASI Library Stack Integration

The optional library registry is available at `/api/libraries`. It is metadata only; do not install every listed framework into the Render web service. Keep heavy GPU inference, image/video generation, and 3D rendering in separately provisioned workers/services if needed. Verify `/health` and `/api/libraries` after deployment.
