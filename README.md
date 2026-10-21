# ALEX DESIGN STUDIO OS

### AI-Powered Creative Automation & Multi-Agent Orchestration Platform

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-gold?style=flat-square)](LICENSE)

---

## Overview

**ALEX DESIGN STUDIO OS** is an AI-powered creative automation platform that streamlines graphic design workflows, advertising campaign creation, content generation, and creative project management through a centralized web-based interface.

The platform uses a **64-role agent architecture** to organize creative tasks into specialized stages — brief analysis, research, brand strategy, copywriting, design planning, quality assurance, and final delivery. A **dependency-aware orchestration engine** coordinates the roles and passes outputs between workflow stages in the correct order.

The system transforms a simple project brief into structured creative deliverables: Instagram campaign copy, promotional poster text, WhatsApp Status content, social media story sequences, and downloadable campaign reports in JSON and Markdown formats.

> **Transparency note:** The 64 roles represent specialized workflow responsibilities. They are not 64 independent AI models. Live AI generation and production infrastructure depend on the corresponding integrations being configured and verified.

---

## Live Demo & API

| Link | Description |
|------|-------------|
| 🌐 Web UI | `https://your-app.onrender.com` |
| 📖 Swagger Docs | `https://your-app.onrender.com/docs` |
| 📘 ReDoc | `https://your-app.onrender.com/redoc` |
| 💚 Health Check | `https://your-app.onrender.com/health` |
| 🤖 Agents JSON | `https://your-app.onrender.com/api/agents` |

---

## Table of Contents

1. [Project Description](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Use Cases](#use-cases)
5. [Technology Stack](#technology-stack)
6. [Quick Start](#quick-start)
7. [API Reference](#api-reference)
8. [CLI Usage](#cli-usage)
9. [Environment Variables](#environment-variables)
10. [Deployment](#deployment)
11. [Version History](#version-history)
12. [Future Scope](#future-scope)
13. [Target Users](#target-users)

---

## Key Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **64-Agent Role Architecture** | Organizes creative and operational responsibilities into specialized named roles |
| 2 | **Dependency-Aware Orchestration** | Runs workflow stages in topological order, passing upstream outputs to downstream roles |
| 3 | **Campaign Generation** | Produces structured advertising content from a plain-text project brief |
| 4 | **Social Media Content** | Instagram captions, poster copy, WhatsApp Status messages, Story sequences |
| 5 | **Report Export** | Campaign outputs in Markdown and JSON formats, downloadable from the UI |
| 6 | **Web Dashboard** | Responsive single-page interface for campaign input, live status, and output review |
| 7 | **REST API** | FastAPI backend with full OpenAPI / Swagger documentation |
| 8 | **Jobs History** | View, browse, and download past campaign runs |
| 9 | **OpenAI Mode** | Optional live AI generation via OpenAI Responses API (requires API key) |
| 10 | **PostgreSQL Support** | Optional persistent job store for production history |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Dashboard (UI)                       │
│              static/index.html  ←→  FastAPI (app.py)         │
└────────────────────────────┬────────────────────────────────┘
                             │ POST /api/campaign
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              campaign_workflow.py                            │
│         run_advertising_campaign(brief, ...)                 │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              orchestrator.py                                 │
│    Builds dependency graph → topological sort →             │
│    Runs all 64 roles in order, passing upstream context     │
└────────────────────────────┬────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   [Stage 1]           [Stage 2–7]          [Stage 8]
  Brief & Strategy    Research, Brand,     QA & Delivery
  Research, etc.      Copy, Design,        Compliance,
                      Media, Eng.          Export
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │  outputs/  (JSON + MD)   │
              │  Postgres (optional)     │
              └──────────────────────────┘
```

### The 8 Workflow Stages

| Stage | Roles |
|-------|-------|
| **1. Brief & Strategy** | AlexAIAssistant, AlexAIDirector, CreativeIntelligenceAgent, ClientBriefAnalyzer, CreativeStrategyAgent, CampaignPlannerAgent, ProjectManagementAgent |
| **2. Research** | TrendAnalysisAgent, ResearchAgent, AudienceIntelligenceAgent, MarketingAnalystAgent, PerformanceAnalyticsAgent, FeedbackLearningAgent |
| **3. Brand** | BrandStrategistAgent, BrandConsistencyAgent, ColorIntelligenceAgent, TypographyAgent, MarathiTypographyAgent, LocalizationAgent |
| **4. Content** | AICopywriterAgent, AdvertisingConceptAgent, SocialMediaManagerAgent, CTAOptimizationAgent, ContentCalendarAgent, PricingAssistantAgent, PromptEngineeringAgent |
| **5. Design** | AIArtDirector, GraphicDesignerAgent, DesignRecommendationEngine, LayoutAgent, ImageSelectionAgent, IllustrationAgent, BackgroundTextureAgent, MockupAgent, ThreeDDesignAgent, DesignAdaptationAgent, AutonomousCreativeDirector |
| **6. Media** | ImageGenerationAgent, ImageEditingAgent, ProductPhotographyAgent, FoodAdvertisingAgent, AIVideoDirectorAgent, VideoGenerationAgent, MotionGraphicsAgent, SceneContinuityAgent, VoiceAudioAgent, VideoEditingAgent |
| **7. Engineering** | AssetPipelineAgent, PluginRegistryAgent, SecurityAgent, SystemHealthAgent, CostMonitoringAgent, WorkflowOrchestratorAgent, JobMonitoringAgent, ErrorRecoveryAgent |
| **8. QA & Delivery** | DesignQAAgent, AIDesignCritic, BrandComplianceAgent, AssetLicensingAgent, ExportAgent, ClientDeliveryAgent, RevisionAgent, ClientManagementAgent |

---

## Use Cases

### 🍗 Social Media Advertising
A business provides its product name, offer, audience, and campaign objective. The system organizes the brief into a campaign plan and generates promotional copy for social media.

**Example:** *Bappu's Biryani — premium Instagram offer campaign*

**Output:** Campaign headline, offer copy, Instagram caption, WhatsApp Status content, and Story sequence.

---

### 🎨 Graphic Design Planning
A designer enters a poster or banner brief. The system structures the creative direction, including visual style, colour palette, typography guidance, layout suggestions, and required copy.

**Output:** A design brief and production-ready creative specifications. Actual image rendering requires an image-generation or design-tool integration.

---

### 🏪 Small Business Marketing
Local businesses can prepare promotional campaigns for restaurants, salons, retail stores, and service providers.

**Output:** Promotional messaging, campaign variations, calls to action, and reusable marketing content.

---

### 📱 Instagram & WhatsApp Content
Content creators can convert one campaign brief into several platform-specific formats.

**Output:** Instagram captions, Story frames, short promotional messages, and campaign hashtags.

---

### 🏢 Creative Agency Workflow
A design studio can use the platform as a structured starting point for campaign intake, task organization, copy development, quality checks, and deliverable preparation.

**Output:** A standardized campaign workflow and downloadable reports for review.

---

### 🔬 AI Agent Orchestration Research
Developers and students can explore multi-agent architecture, dependency graphs, role-based task execution, output passing, workflow validation, and API integration.

**Output:** An extensible development platform for experimenting with agent orchestration.

---

### 🎓 Academic & Portfolio Projects
Students can demonstrate API development, workflow automation, testing, responsive dashboards, and deployment configuration in a portfolio.

**Output:** A runnable project scaffold with documented implementation.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Frontend** | HTML5, Vanilla CSS, JavaScript (no framework) |
| **Agent Architecture** | 64 specialized workflow roles, custom dependency graph |
| **Orchestration** | Topological-sort dependency-aware execution engine |
| **Output Formats** | JSON, Markdown |
| **Optional AI** | OpenAI Responses API (`gpt-4.1-mini` or custom model) |
| **Optional DB** | PostgreSQL via psycopg v3 |
| **Deployment** | Render (backend + UI), Netlify (static frontend only) |
| **Future** | Redis, Celery, authentication, monitoring, image/video generation |

---

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/shubhamkothavale0047-dev/AI-Agents.git
cd AI-Agents

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional)
cp .env.example .env
# Edit .env as needed

# 5. Start the server
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in your browser.

---

## API Reference

### `GET /health`
System health check and role count.

```json
{
  "status": "ok",
  "app": "ALEX DESIGN STUDIO OS",
  "version": "1.0.0",
  "registered_roles": 64,
  "execution_mode": "local-template-orchestration",
  "live_llm_calls": 0
}
```

### `GET /api/agents`
List all 64 registered agent roles with category and responsibility.

### `POST /api/campaign`
Run the full 64-role campaign workflow.

**Request body:**
```json
{
  "brief": "Bappu's Biryani — premium Instagram offer poster",
  "offer_price": "₹149",
  "regular_price": "₹220"
}
```

**Response:** Full campaign object including poster copy, Instagram caption, WhatsApp Status, Story sequence, creative direction, QA checklist, and download links.

### `GET /api/jobs`
List all recent completed job runs.

### `GET /api/jobs/{job_id}/json`
Download a job's full output as a JSON file.

### `GET /api/jobs/{job_id}/markdown`
Download a job's campaign report as a Markdown file.

---

## CLI Usage

```bash
# Run the advertising campaign (local mode, all 64 roles)
python -m alex_design_studio_os --workflow advertising \
  --brief "Bappu's Biryani — premium Instagram offer poster" \
  --offer-price "₹149" --regular-price "₹220"

# Run the core design workflow
python -m alex_design_studio_os --workflow core --mode local \
  --brief "Pune dairy farm Instagram campaign"

# Run with OpenAI (requires OPENAI_API_KEY)
export OPENAI_API_KEY='sk-...'
python -m alex_design_studio_os --mode openai \
  --brief "Organic skincare brand campaign"

# SQLite job store CLI
python -m alex_design_studio_os.jobs_cli create --brief "My campaign"
python -m alex_design_studio_os.jobs_cli run   --job-id job_xxxxxxxxxxxx
python -m alex_design_studio_os.jobs_cli status --job-id job_xxxxxxxxxxxx
python -m alex_design_studio_os.jobs_cli list

# Self tests
python -m alex_design_studio_os.self_test
python -m alex_design_studio_os.agent_validation
python -m alex_design_studio_os.orchestrator_self_test
python -m alex_design_studio_os.campaign_self_test
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `ALEX_OUTPUT_DIR` | `./outputs` | Directory for generated campaign files |
| `DATABASE_URL` | *(unset)* | PostgreSQL connection string (optional) |
| `OPENAI_API_KEY` | *(unset)* | OpenAI API key for live AI mode (optional) |
| `OPENAI_MODEL` | `gpt-4.1-mini` | OpenAI model override (optional) |
| `PYTHON_VERSION` | `3.12.8` | Python version hint for cloud platforms |

> ⚠️ Never commit your API key or database credentials to source control.

---

## Deployment

### Render (Recommended — Backend + UI)

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Runtime** | Python 3 |
| **Plan** | Free |

**Environment variables to add in Render dashboard:**
- `PYTHON_VERSION` = `3.12.8`
- `ALEX_OUTPUT_DIR` = `/tmp/alex_outputs`
- `OPENAI_API_KEY` = *(your key, if using OpenAI mode)*

Alternatively, connect the repo and use **New + → Blueprint** — Render auto-detects `render.yaml`.

> **Note:** Render's free tier sleeps after 15 minutes. Files on disk are ephemeral — download reports after each run, or connect PostgreSQL for persistence.

### PostgreSQL (Persistent Job History)

```bash
# Initialize schema
python -c "
from alex_design_studio_os.postgres_store import PostgresJobStore
PostgresJobStore().initialize()
print('Schema initialized')
"
```

Set `DATABASE_URL` in your environment or Render dashboard to activate.

---

## Version History

| Version | Highlights |
|---------|-----------|
| **v0.1** | 64 named agent-role classes and registry; local template pipeline |
| **v0.2** | Optional OpenAI Responses API integration (one-call strategy pack) |
| **v0.3** | Single-agent live test for `CreativeIntelligenceAgent` |
| **v0.4** | SQLite durable job store + `jobs_cli` (create / run / status / list) |
| **v0.5** | Optional PostgreSQL job store with JSONB and status constraint |
| **v0.6** | 64-role advertising campaign workflow; JSON + Markdown reports |
| **v0.7** | Unified CLI (`--workflow advertising / core`, `--mode local / openai`) |
| **v0.8** | 64-role contract validation (`agent_validation`, `agent_validation_self_test`) |
| **v0.9** | Dependency-aware orchestration (topological sort, upstream context passing) |
| **v1.0** | FastAPI web app, responsive dashboard, CORS, logging, `/api/jobs` history, `.env.example`, production deployment |

---

## Future Scope

- 🤖 Connect live AI models to appropriate agent roles
- 🗄️ Persistent job storage and background processing (Redis, Celery)
- 🔐 Authentication, user accounts, and project history
- 🖼️ Image and video generation service integrations
- 📊 Workflow monitoring, retries, and error recovery dashboards
- 👥 Team collaboration and reusable brand profiles
- 🌍 Multi-language support beyond Marathi / Hindi / English
- 🔒 Production security controls, rate limiting, and audit logging

---

## Target Users

- 🎨 Graphic designers and creative studios
- 📣 Digital marketing agencies
- 🏪 Small business owners
- 📱 Social media managers and content creators
- 🔬 AI and automation developers
- 🎓 Students and researchers exploring multi-agent systems

---

## Project Structure

```
alex_design_studio_os_agents_64/
├── app.py                          # FastAPI application (main entry point)
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku/Render process definition
├── render.yaml                     # Render Blueprint config
├── netlify.toml                    # Netlify config (static frontend)
├── .env.example                    # Environment variable reference
├── DEPLOYMENT.md                   # Detailed deployment guide
├── static/
│   └── index.html                  # Web dashboard (single-page UI)
├── outputs/                        # Generated campaign files (gitignored)
└── alex_design_studio_os/
    ├── __init__.py
    ├── __main__.py                 # CLI entry point
    ├── agents.py                   # All 64 agent role classes
    ├── registry.py                 # Agent registry and factory
    ├── base.py                     # BaseAgent and AgentSpec
    ├── orchestrator.py             # Dependency graph + topological runner
    ├── campaign_workflow.py        # 64-role advertising campaign workflow
    ├── workflow.py                 # Core design workflow
    ├── ai_workflow.py              # OpenAI Responses API workflow
    ├── ai_provider.py              # OpenAI HTTP client
    ├── job_store.py                # SQLite durable job store
    ├── postgres_store.py           # PostgreSQL job store (optional)
    ├── jobs_cli.py                 # Job management CLI
    ├── agent_manifest.json         # Agent metadata manifest
    ├── agent_validation.py         # Role contract validation
    └── *_self_test.py              # Self-test modules
```

---

## Conclusion

ALEX DESIGN STUDIO OS is a modular creative automation platform combining a responsive web dashboard, a 64-role workflow architecture, and a dependency-aware task orchestration engine. It provides a solid foundation for organizing advertising and design workflows and can be extended with live AI providers and production infrastructure as those components are implemented and verified.

---

<div align="center">

**Built with ❤️ for creative automation**

[Web UI](https://your-app.onrender.com) · [API Docs](https://your-app.onrender.com/docs) · [GitHub](https://github.com/shubhamkothavale0047-dev/AI-Agents)

</div>
