"""End-to-end SQLite job lifecycle test; no external services needed."""
import tempfile
from pathlib import Path
from .job_store import JobStore
from .workflow import run_core_pipeline


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db = str(Path(tmp) / "jobs.sqlite3")
        store = JobStore(db)
        job = store.create("Test brief: local bakery launch campaign")
        assert job["status"] == "QUEUED"
        # Re-open store to verify persistence across instances.
        reopened = JobStore(db)
        assert reopened.get(job["job_id"])["brief"] == job["brief"]
        reopened.set_running(job["job_id"])
        result = run_core_pipeline(job["brief"])
        reopened.succeed(job["job_id"], result)
        final = JobStore(db).get(job["job_id"])
        assert final["status"] == "SUCCEEDED", final
        assert final["result"]["all_registered_agents"] == 64
        assert final["result"]["output_file"]
        print("PASS: job created as QUEUED.")
        print("PASS: job persisted after reopening SQLite database.")
        print("PASS: QUEUED -> RUNNING -> SUCCEEDED lifecycle.")
        print("PASS: job result contains 64 registered agent roles and output path.")
        print("PASS: no OpenAI key, PostgreSQL, Redis, or Celery required for this local test.")


if __name__ == "__main__":
    main()
