# ALEX DESIGN STUDIO OS — 64 Agent Starter Kit v0.2

A runnable local scaffold for 64 named agent roles, plus an **optional one-call OpenAI Responses API integration**.

## Run in Termux (Android)

1. Install Python if needed: `pkg install python`
2. Extract this ZIP, then enter the folder `alex_design_studio_os_agents_64`.
3. Run the offline demo:
   `python -m alex_design_studio_os`
4. Run the local verification:
   `python -m alex_design_studio_os.self_test`

## Enable the OpenAI API mode

You need your own valid API key and API billing/credits. Never paste the key into chat or commit it to GitHub.

In the same Termux session, set the key:
`export OPENAI_API_KEY='your-key-here'`

Optional model override:
`export OPENAI_MODEL='gpt-4.1-mini'`

Then run:
`python -m alex_design_studio_os --mode openai`

The generated strategy report is saved in `outputs/`. The key is read from the environment and is not written to the report.

## What is implemented

- 64 named agent-role classes and registry.
- Local template pipeline works offline with standard library only.
- Optional OpenAI Responses API client using standard-library HTTP.
- OpenAI mode creates a structured creative-strategy pack and saves a JSON report.
- Clear handling for missing API key, HTTP errors, connection errors, and empty responses.

## Important scope limits

- The 64 roles are not 64 independent models; most roles use local templates.
- OpenAI mode currently makes **one model call** for a strategy pack. It does not invoke all 64 agents as separate model calls.
- No live web research, image/video generation, PostgreSQL, Redis/Celery, or deployment is included.
- The package's tests can verify local code paths, but cannot verify your API key, billing, network, or Android device until you run it there.
- Review all output for accuracy, licensing, and client suitability before delivery.


## Test one live AI agent (real API call)

This test calls the OpenAI API for the `CreativeIntelligenceAgent` and saves a JSON report. It is **not** executed during package self-tests because it requires your own API key and may incur API usage charges.

In Termux, from this folder:
`export OPENAI_API_KEY='your-key-here'`
`python -m alex_design_studio_os.single_agent_live_test`

Optional:
`export OPENAI_MODEL='gpt-4.1-mini'`

Do not paste your API key into chat or commit it to source control. A `PASS` is shown only after a real API response contains non-empty model output. This tests one agent path, not all 64 agents.


## v0.4 — Durable local jobs and status

This release adds a SQLite job store (standard library) for a reliable Android-friendly local development step before PostgreSQL/Redis/Celery.

### Create a job
`python -m alex_design_studio_os.jobs_cli create --brief "Pune dairy farm Instagram campaign"`

Copy the returned `job_id`, then run:
`python -m alex_design_studio_os.jobs_cli run --job-id job_xxxxxxxxxxxx`

Check status:
`python -m alex_design_studio_os.jobs_cli status --job-id job_xxxxxxxxxxxx`

List recent jobs:
`python -m alex_design_studio_os.jobs_cli list`

Run lifecycle test:
`python -m alex_design_studio_os.job_store_self_test`

The local runner is synchronous: the job status is durable, but this is not yet a Redis/Celery background worker or a live WebSocket status feed. PostgreSQL integration is not included in this release.


## v0.5 — Optional PostgreSQL job store

Added `PostgresJobStore`, using PostgreSQL JSONB for job results and a status constraint.

### Configure
Install optional driver:
`pip install 'psycopg[binary]>=3.1'`

Set your connection string privately in Termux:
`export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DBNAME'`

Then a Python entry point can initialize the schema:
`python -c "from alex_design_studio_os.postgres_store import PostgresJobStore; PostgresJobStore().initialize(); print('Schema initialized')"`

Do not put real credentials in source code or share them in chat. A successful schema initialization message only confirms that your configured database was reachable and accepted the schema.

Offline adapter checks:
`python -m alex_design_studio_os.postgres_self_test`

The SQLite CLI remains the tested end-to-end job runner. This release adds the PostgreSQL storage adapter but does not yet switch the CLI runner to PostgreSQL or add Redis/Celery.


## v0.6 — Advertising campaign workflow across all 64 registered roles

Run in the extracted project directory:
`python -m alex_design_studio_os.campaign_self_test`

Run a campaign:
`python -c "from alex_design_studio_os.campaign_workflow import run_advertising_campaign; r=run_advertising_campaign("Bappu's Biryani — premium Instagram offer poster"); print(r['markdown_path']); print(r['json_path'])"`

This workflow calls each of the 64 registered role classes once in local template mode and records their outputs alongside a usable campaign copy pack. It makes zero separate LLM calls, does not perform live trend research, and does not generate image/video assets itself. Confirm all prices and offer terms before publishing.

## v0.7 — Integrated OS entry point

The advertising campaign workflow is now integrated into the main CLI alongside the existing core design workflow.

Run the Bappu's Biryani campaign (local template mode, all 64 registered roles called once):
`python -m alex_design_studio_os --workflow advertising --brief "Bappu's Biryani — premium Instagram offer poster"`

Optional offer values and output directory:
`python -m alex_design_studio_os --workflow advertising --brief "Bappu's Biryani — premium Instagram offer poster" --offer-price "₹149" --regular-price "₹220" --output-dir outputs`

Run the core workflow as before:
`python -m alex_design_studio_os --workflow core --mode local --brief "Pune dairy farm Instagram campaign"`

The advertising CLI currently runs all 64 registered roles in local template mode; it does not make 64 independent LLM calls, perform live research, or generate image/video files. Prices must be confirmed before publishing. PostgreSQL remains an optional adapter and is not wired into the CLI job runner; Redis/Celery and Android-device execution are not verified.

## v0.8 — 64-role contract validation

Run a repeatable interface check for every registered role:

```bash
python -m alex_design_studio_os.agent_validation
python -m alex_design_studio_os.agent_validation_self_test
```

This verifies that all 64 registered roles can be instantiated, accept the supplied brief, and return the documented local result fields. It intentionally does **not** claim independent LLM reasoning or live external-service integration.

## v0.9 — Dependency-aware 64-role orchestration

Run the dependency-graph integration test:

```bash
python -m alex_design_studio_os.orchestrator_self_test
```

Run the advertising campaign end-to-end in local mode:

```bash
python -m alex_design_studio_os --workflow advertising --brief "Bappu's Biryani — premium Instagram offer poster"
```

The campaign workflow now schedules all 64 registered roles in dependency order, passes upstream summaries into downstream roles, records per-role status/timing/errors and writes JSON + Markdown reports. To inspect detailed data-flow, open the generated JSON and look at `orchestration_report`, `dependency_graph`, `execution_order`, `execution_log`, and `agent_results`.

**Verified scope:** dependency-graph test and local campaign execution pass in this build; 64 roles scheduled/completed; upstream data flow verified; zero failed roles in the test run. This is still local template orchestration, not 64 independent LLMs. No live OpenAI API, live PostgreSQL server, Redis/Celery, image generation or Android-device deployment is verified by this test.
