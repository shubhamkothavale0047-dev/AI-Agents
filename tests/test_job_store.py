import pytest
from alex_design_studio_os.job_store import JobStore


def test_job_store_lifecycle(tmp_path):
    db_file = tmp_path / "test_jobs.sqlite3"
    store = JobStore(str(db_file))

    # Empty brief error
    with pytest.raises(ValueError, match="cannot be empty"):
        store.create("  ")

    # Create job
    job = store.create("Test brief for social ad")
    assert job["status"] == "QUEUED"
    assert job["brief"] == "Test brief for social ad"
    job_id = job["job_id"]

    # Transition to RUNNING
    store.set_running(job_id)
    running_job = store.get(job_id)
    assert running_job["status"] == "RUNNING"

    # Transition to SUCCEEDED
    sample_result = {"status": "ok", "delivered": True}
    store.succeed(job_id, sample_result)
    succeeded_job = store.get(job_id)
    assert succeeded_job["status"] == "SUCCEEDED"
    assert succeeded_job["result"] == sample_result

    # List recent
    recent = store.list_recent(limit=10)
    assert len(recent) >= 1
    assert any(j["job_id"] == job_id for j in recent)
