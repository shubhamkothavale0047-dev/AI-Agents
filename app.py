"""ALEX DESIGN STUDIO OS — Production FastAPI application."""
from pathlib import Path
from uuid import uuid4
import json, os, logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from alex_design_studio_os.registry import create_all_agents
from alex_design_studio_os.campaign_workflow import run_advertising_campaign

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("alex_os")

BASE = Path(__file__).resolve().parent
OUT = Path(os.getenv("ALEX_OUTPUT_DIR", str(BASE / "outputs")))
OUT.mkdir(parents=True, exist_ok=True)

# ── Lifespan (startup / shutdown hooks) ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ALEX DESIGN STUDIO OS starting up…")
    logger.info("Output directory: %s", OUT)
    agents = create_all_agents()
    logger.info("Registered agent roles: %d", len(agents))
    yield
    logger.info("ALEX DESIGN STUDIO OS shutting down.")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ALEX DESIGN STUDIO OS",
    version="1.0.0",
    description=(
        "64-role creative campaign orchestration platform. "
        "Produces poster copy, social captions, WhatsApp status, "
        "story frames, creative direction and QA checklists."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Request / Response models ─────────────────────────────────────────────────
class CampaignRequest(BaseModel):
    brief: str = Field(min_length=3, max_length=4000, description="Project / campaign brief")
    offer_price: str = Field(default="₹149", max_length=40, description="Offer / sale price")
    regular_price: str = Field(default="₹220", max_length=40, description="Regular / MRP price")

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check")
def health():
    agents = create_all_agents()
    return {
        "status": "ok",
        "app": "ALEX DESIGN STUDIO OS",
        "version": "1.0.0",
        "registered_roles": len(agents),
        "execution_mode": "local-template-orchestration",
        "live_llm_calls": 0,
        "output_dir": str(OUT),
    }

@app.get("/api/agents", tags=["Agents"], summary="List all registered agent roles")
def agents():
    registry = create_all_agents()
    rows = [
        {
            "key": key,
            "name": getattr(agent, "name", key),
            "category": getattr(agent.spec, "category", ""),
            "responsibility": getattr(agent.spec, "responsibility", ""),
            "class": agent.__class__.__name__,
            "mode": "LOCAL_TEMPLATE",
        }
        for key, agent in registry.items()
    ]
    return {"count": len(rows), "agents": rows}

@app.post("/api/campaign", tags=["Campaign"], summary="Run a full 64-role campaign workflow")
def campaign(req: CampaignRequest):
    logger.info("Campaign request received | brief_len=%d", len(req.brief))
    try:
        result = run_advertising_campaign(
            req.brief,
            offer_price=req.offer_price,
            regular_price=req.regular_price,
            output_dir=str(OUT),
        )
        campaign_data = result["campaign"]
        cid = uuid4().hex[:12]
        json_path = OUT / f"{cid}.json"
        md_path = OUT / f"{cid}.md"
        json_path.write_text(json.dumps(campaign_data, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(Path(result["markdown_path"]).read_text(encoding="utf-8"), encoding="utf-8")
        exec_info = campaign_data["execution"]
        logger.info(
            "Campaign complete | job=%s completed=%d failed=%d",
            cid, exec_info["agent_roles_completed"], len(exec_info["agent_roles_failed"]),
        )
        return {
            "job_id": cid,
            "status": "SUCCEEDED" if exec_info["all_roles_completed"] else "PARTIAL",
            "mode": exec_info["mode"],
            "registered_agents": exec_info["registered_agent_roles"],
            "completed_agents": exec_info["agent_roles_completed"],
            "failed_agents": exec_info["agent_roles_failed"],
            "live_llm_calls": exec_info["separate_llm_calls"],
            "campaign": campaign_data,
            "downloads": {
                "json": f"/api/jobs/{cid}/json",
                "markdown": f"/api/jobs/{cid}/markdown",
            },
        }
    except ValueError as e:
        logger.warning("Campaign validation error: %s", e)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Campaign execution failed")
        raise HTTPException(status_code=500, detail=f"Campaign execution failed: {type(e).__name__}: {e}")

@app.get("/api/jobs", tags=["Jobs"], summary="List all completed jobs")
def list_jobs():
    """Return metadata for all saved job files (newest first)."""
    jobs = []
    for f in sorted(OUT.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:50]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            jobs.append({
                "job_id": f.stem,
                "campaign_name": data.get("campaign_name", ""),
                "status": data.get("execution", {}).get("all_roles_completed") and "SUCCEEDED" or "PARTIAL",
                "created_at_utc": data.get("created_at_utc", ""),
            })
        except Exception:
            pass
    return {"count": len(jobs), "jobs": jobs}

@app.get("/api/jobs/{job_id}/json", tags=["Jobs"], summary="Download job result as JSON")
def get_json(job_id: str):
    if not job_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid job ID")
    p = OUT / f"{job_id}.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="Job not found on this instance")
    return JSONResponse(
        json.loads(p.read_text(encoding="utf-8")),
        headers={"Content-Disposition": f'attachment; filename="alex-campaign-{job_id}.json"'},
    )

@app.get("/api/jobs/{job_id}/markdown", tags=["Jobs"], summary="Download job result as Markdown")
def get_markdown(job_id: str):
    if not job_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid job ID")
    p = OUT / f"{job_id}.md"
    if not p.exists():
        raise HTTPException(status_code=404, detail="Job not found on this instance")
    return PlainTextResponse(
        p.read_text(encoding="utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="alex-campaign-{job_id}.md"'},
    )

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return (BASE / "static" / "index.html").read_text(encoding="utf-8")

# ── Global error handler ──────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception for %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )
