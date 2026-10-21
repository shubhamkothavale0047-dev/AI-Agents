from pathlib import Path
from uuid import uuid4
import json, os, logging, re
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field

from alex_design_studio_os.registry import create_all_agents
from alex_design_studio_os.campaign_workflow import run_advertising_campaign
from alex_design_studio_os.library_registry import get_library_registry

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("alex_os")

BASE = Path(__file__).resolve().parent
OUT = Path(os.getenv("ALEX_OUTPUT_DIR", str(BASE / "outputs")))
OUT.mkdir(parents=True, exist_ok=True)
SAFE_JOB_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")

# ── Optional PostgreSQL Store ────────────────────────────────────────────────
pg_store = None
if os.getenv("DATABASE_URL"):
    try:
        from alex_design_studio_os.postgres_store import PostgresJobStore
        pg_store = PostgresJobStore()
        logger.info("PostgreSQL storage enabled via DATABASE_URL")
    except Exception as exc:
        logger.warning("PostgreSQL setup deferred or failed: %s", exc)

# ── Lifespan (startup / shutdown hooks) ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ALEX DESIGN STUDIO OS starting up…")
    logger.info("Output directory: %s", OUT)
    agents = create_all_agents()
    logger.info("Registered agent roles: %d", len(agents))
    if pg_store:
        try:
            pg_store.initialize()
            logger.info("PostgreSQL alex_jobs schema ready.")
        except Exception as exc:
            logger.warning("PostgreSQL schema initialization skipped: %s", exc)
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

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

if (BASE / "static").is_dir():
    app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

# ── Request / Response models ─────────────────────────────────────────────────
class CampaignRequest(BaseModel):
    brief: str = Field(min_length=3, max_length=4000, description="Project / campaign brief")
    offer_price: str = Field(default="₹149", max_length=40, description="Offer / sale price")
    regular_price: str = Field(default="₹220", max_length=40, description="Regular / MRP price")

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<rect width="100" height="100" rx="22" fill="#050b14"/>'
        '<text x="50" y="68" font-size="54" font-weight="900" font-family="sans-serif" '
        'fill="#00e5ff" text-anchor="middle">A</text></svg>'
    )
    return Response(content=svg, media_type="image/svg+xml")

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
        "storage": "postgresql (active)" if pg_store else "filesystem (local)",
        "output_dir": str(OUT),
    }

@app.get("/api/agents", tags=["Agents"], summary="List all registered agent roles")
def agents(category: str | None = None, search: str | None = None):
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
    if category and category.upper() != "ALL":
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    if search:
        q = search.lower()
        rows = [r for r in rows if q in r["name"].lower() or q in r["key"].lower() or q in r["responsibility"].lower()]
    return {"count": len(rows), "agents": rows}

@app.get("/api/libraries", tags=["Library Stack"], summary="List optional ALEX ASI library candidates")
def libraries(category: str | None = None, search: str | None = None):
    """Return candidate libraries; entries are not automatically installed or production-approved."""
    data = get_library_registry()
    libs = data.get("libraries", [])
    if category and category.upper() != "ALL":
        libs = [l for l in libs if l.get("category", "").lower() == category.lower()]
    if search:
        q = search.lower()
        libs = [l for l in libs if q in l.get("name", "").lower() or q in l.get("notes", "").lower()]
    data["libraries"] = libs
    data["count"] = len(libs)
    return data

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

        if pg_store:
            try:
                pg_job = pg_store.create(req.brief)
                pg_store.set_running(pg_job["job_id"])
                pg_store.succeed(pg_job["job_id"], campaign_data)
                logger.info("Synced campaign to PostgreSQL job: %s", pg_job["job_id"])
            except Exception as pg_err:
                logger.warning("PostgreSQL job sync warning: %s", pg_err)

        logger.info(
            "Campaign complete | job=%s completed=%d failed=%d",
            cid, exec_info["agent_roles_completed"], len(exec_info["agent_roles_failed"]),
        )
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
            name = (
                data.get("campaign_name")
                or data.get("client_brief")
                or data.get("campaign_goal")
                or data.get("system")
                or f.stem
            )
            if len(name) > 60:
                name = name[:57] + "…"
            
            exec_data = data.get("execution", {})
            if isinstance(exec_data, dict) and exec_data.get("all_roles_completed"):
                status = "SUCCEEDED"
            elif data.get("status") in ("SUCCEEDED", "PARTIAL", "FAILED"):
                status = data["status"]
            elif "creative_strategy" in data or "core_pipeline" in data:
                status = "SUCCEEDED"
            else:
                status = "PARTIAL"

            jobs.append({
                "job_id": f.stem,
                "campaign_name": name,
                "status": status,
                "created_at_utc": data.get("created_at_utc", ""),
            })
        except Exception:
            pass
    return {"count": len(jobs), "jobs": jobs}

@app.get("/api/jobs/{job_id}", tags=["Jobs"], summary="Get job JSON result")
def get_job(job_id: str):
    """Retrieve full JSON result for a completed campaign job."""
    return get_json(job_id)

@app.get("/api/jobs/{job_id}/json", tags=["Jobs"], summary="Download job result as JSON")
def get_json(job_id: str):
    if not SAFE_JOB_ID_RE.match(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    try:
        target = (OUT / f"{job_id}.json").resolve()
        if not target.is_relative_to(OUT.resolve()):
            raise HTTPException(status_code=400, detail="Access denied")
    except (ValueError, RuntimeError):
        raise HTTPException(status_code=400, detail="Invalid job path")

    if not target.is_file():
        raise HTTPException(status_code=404, detail="Job not found on this instance")
    try:
        content = json.loads(target.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read job file: {exc}")

    return JSONResponse(
        content,
        headers={"Content-Disposition": f'attachment; filename="alex-campaign-{job_id}.json"'},
    )

@app.get("/api/jobs/{job_id}/markdown", tags=["Jobs"], summary="Download job result as Markdown")
def get_markdown(job_id: str):
    if not SAFE_JOB_ID_RE.match(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    try:
        target = (OUT / f"{job_id}.md").resolve()
        if not target.is_relative_to(OUT.resolve()):
            raise HTTPException(status_code=400, detail="Access denied")
    except (ValueError, RuntimeError):
        raise HTTPException(status_code=400, detail="Invalid job path")

    if not target.is_file():
        raise HTTPException(status_code=404, detail="Job not found on this instance")
    return PlainTextResponse(
        target.read_text(encoding="utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="alex-campaign-{job_id}.md"'},
    )

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    index_file = BASE / "static" / "index.html"
    if not index_file.is_file():
        raise HTTPException(status_code=404, detail="Frontend index.html not found")
    return index_file.read_text(encoding="utf-8")

# ── Exception handlers ────────────────────────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=getattr(exc, "headers", None),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server exception for %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )
