"""Offline checks for PostgreSQL adapter configuration and SQL contract."""
import os
from .postgres_store import (
    PostgresConfigurationError, PostgresJobStore, SCHEMA_SQL
)


def main():
    previous = os.environ.pop("DATABASE_URL", None)
    try:
        try:
            PostgresJobStore()
        except PostgresConfigurationError as exc:
            assert "DATABASE_URL is missing" in str(exc)
            print("PASS: PostgreSQL mode fails safely when DATABASE_URL is missing.")
        else:
            raise AssertionError("Expected missing DATABASE_URL failure.")
    finally:
        if previous is not None:
            os.environ["DATABASE_URL"] = previous

    assert "CREATE TABLE IF NOT EXISTS alex_jobs" in SCHEMA_SQL
    assert "JSONB" in SCHEMA_SQL
    assert "CHECK (status IN ('QUEUED','RUNNING','SUCCEEDED','FAILED'))" in SCHEMA_SQL
    print("PASS: PostgreSQL schema contract includes status constraints and JSONB results.")
    print("NOTE: This is an offline contract test, not a live database connection test.")


if __name__ == "__main__":
    main()
