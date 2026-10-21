"""Optional PostgreSQL job store. Requires psycopg v3 and DATABASE_URL."""
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS alex_jobs (
    job_id TEXT PRIMARY KEY,
    brief TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('QUEUED','RUNNING','SUCCEEDED','FAILED')),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    result_json JSONB,
    error TEXT
);
CREATE INDEX IF NOT EXISTS idx_alex_jobs_status ON alex_jobs(status);
"""


class PostgresConfigurationError(RuntimeError):
    pass


def _load_psycopg():
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise PostgresConfigurationError(
            "PostgreSQL mode needs psycopg v3. Install with: pip install 'psycopg[binary]>=3.1'"
        ) from exc
    return psycopg, dict_row


class PostgresJobStore:
    """PostgreSQL equivalent for the local SQLite JobStore interface."""
    def __init__(self, database_url: str | None = None):
        self.database_url = (database_url or os.getenv("DATABASE_URL", "")).strip()
        if not self.database_url:
            raise PostgresConfigurationError(
                "DATABASE_URL is missing. Set it to your PostgreSQL connection string."
            )
        self.psycopg, self.dict_row = _load_psycopg()

    def _connect(self):
        return self.psycopg.connect(self.database_url, row_factory=self.dict_row, connect_timeout=8)

    def initialize(self):
        with self._connect() as conn:
            conn.execute(SCHEMA_SQL)

    @staticmethod
    def _now():
        return datetime.now(timezone.utc)

    def create(self, brief: str) -> dict[str, Any]:
        brief = brief.strip()
        if not brief:
            raise ValueError("Brief cannot be empty.")
        job_id = "job_" + uuid.uuid4().hex[:12]
        now = self._now()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO alex_jobs(job_id, brief, status, created_at, updated_at) "
                "VALUES (%s,%s,'QUEUED',%s,%s)",
                (job_id, brief, now, now),
            )
        return self.get(job_id)

    def get(self, job_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM alex_jobs WHERE job_id=%s", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown job ID: {job_id}")
        item = dict(row)
        if item.get("result_json") is not None:
            item["result"] = item.pop("result_json")
        else:
            item.pop("result_json", None)
        return item

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 100))
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT job_id, brief, status, created_at, updated_at, error "
                "FROM alex_jobs ORDER BY created_at DESC LIMIT %s", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def set_running(self, job_id: str):
        with self._connect() as conn:
            row = conn.execute(
                "UPDATE alex_jobs SET status='RUNNING', updated_at=%s, error=NULL "
                "WHERE job_id=%s AND status IN ('QUEUED','FAILED') RETURNING job_id",
                (self._now(), job_id),
            ).fetchone()
            if row is None:
                current = conn.execute("SELECT status FROM alex_jobs WHERE job_id=%s", (job_id,)).fetchone()
                if current is None:
                    raise KeyError(f"Unknown job ID: {job_id}")
                raise ValueError(f"Job cannot run from status {current['status']}")

    def succeed(self, job_id: str, result: dict[str, Any]):
        with self._connect() as conn:
            row = conn.execute(
                "UPDATE alex_jobs SET status='SUCCEEDED', updated_at=%s, result_json=%s::jsonb, error=NULL "
                "WHERE job_id=%s AND status='RUNNING' RETURNING job_id",
                (self._now(), json.dumps(result, ensure_ascii=False), job_id),
            ).fetchone()
            if row is None:
                raise ValueError("Job was not RUNNING; cannot mark SUCCEEDED.")

    def fail(self, job_id: str, error: str):
        with self._connect() as conn:
            conn.execute(
                "UPDATE alex_jobs SET status='FAILED', updated_at=%s, error=%s "
                "WHERE job_id=%s AND status='RUNNING'",
                (self._now(), str(error)[:2000], job_id),
            )
