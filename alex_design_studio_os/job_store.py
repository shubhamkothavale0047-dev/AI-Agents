"""SQLite-backed durable job store for Android-friendly local runs."""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobStore:
    def __init__(self, db_path: str = "data/alex_jobs.sqlite3"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path, timeout=15)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    brief TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    result_json TEXT,
                    error TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")

    def create(self, brief: str) -> dict[str, Any]:
        brief = brief.strip()
        if not brief:
            raise ValueError("Brief cannot be empty.")
        job_id = "job_" + uuid.uuid4().hex[:12]
        now = utc_now()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO jobs(job_id, brief, status, created_at, updated_at) VALUES(?,?,?,?,?)",
                (job_id, brief, "QUEUED", now, now),
            )
        return self.get(job_id)

    def get(self, job_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown job ID: {job_id}")
        item = dict(row)
        if item.get("result_json"):
            item["result"] = json.loads(item.pop("result_json"))
        else:
            item.pop("result_json", None)
        return item

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 100))
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT job_id, brief, status, created_at, updated_at, error "
                "FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def set_running(self, job_id: str):
        now = utc_now()
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE jobs SET status='RUNNING', updated_at=?, error=NULL "
                "WHERE job_id=? AND status IN ('QUEUED','FAILED')",
                (now, job_id),
            )
            if cur.rowcount != 1:
                row = conn.execute("SELECT status FROM jobs WHERE job_id=?", (job_id,)).fetchone()
                if row is None:
                    raise KeyError(f"Unknown job ID: {job_id}")
                raise ValueError(f"Job cannot run from status {row['status']}")

    def succeed(self, job_id: str, result: dict[str, Any]):
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE jobs SET status='SUCCEEDED', updated_at=?, result_json=?, error=NULL "
                "WHERE job_id=? AND status='RUNNING'",
                (utc_now(), json.dumps(result, ensure_ascii=False), job_id),
            )
            if cur.rowcount != 1:
                raise ValueError("Job was not RUNNING; cannot mark SUCCEEDED.")

    def fail(self, job_id: str, error: str):
        with self._connect() as conn:
            conn.execute(
                "UPDATE jobs SET status='FAILED', updated_at=?, error=? WHERE job_id=? AND status='RUNNING'",
                (utc_now(), str(error)[:2000], job_id),
            )
