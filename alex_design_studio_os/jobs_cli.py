"""Create, run, and inspect durable local jobs."""
import argparse
import json
from .job_store import JobStore
from .workflow import run_core_pipeline


def main():
    parser = argparse.ArgumentParser(description="ALEX DESIGN STUDIO OS durable jobs")
    parser.add_argument("--db", default="data/alex_jobs.sqlite3", help="SQLite database path")
    sub = parser.add_subparsers(dest="action", required=True)
    create = sub.add_parser("create", help="Create a queued job")
    create.add_argument("--brief", required=True)
    run = sub.add_parser("run", help="Execute a queued job")
    run.add_argument("--job-id", required=True)
    status = sub.add_parser("status", help="Show one job")
    status.add_argument("--job-id", required=True)
    sub.add_parser("list", help="List recent jobs")
    args = parser.parse_args()
    store = JobStore(args.db)

    if args.action == "create":
        print(json.dumps(store.create(args.brief), indent=2, ensure_ascii=False))
    elif args.action == "status":
        print(json.dumps(store.get(args.job_id), indent=2, ensure_ascii=False))
    elif args.action == "list":
        print(json.dumps(store.list_recent(), indent=2, ensure_ascii=False))
    elif args.action == "run":
        job = store.get(args.job_id)
        store.set_running(args.job_id)
        try:
            result = run_core_pipeline(job["brief"])
            store.succeed(args.job_id, result)
        except Exception as exc:
            store.fail(args.job_id, f"{type(exc).__name__}: {exc}")
            raise SystemExit(f"JOB FAILED: {type(exc).__name__}: {exc}") from exc
        final = store.get(args.job_id)
        print(json.dumps({
            "job_id": final["job_id"],
            "status": final["status"],
            "output_file": final["result"].get("output_file"),
            "registered_agents": final["result"].get("all_registered_agents"),
        }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
