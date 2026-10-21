import pytest
from app import health, agents, libraries, list_jobs, SAFE_JOB_ID_RE


def test_health_endpoint():
    res = health()
    assert res["status"] == "ok"
    assert res["registered_roles"] == 64
    assert res["execution_mode"] == "local-template-orchestration"


def test_agents_endpoint():
    res = agents()
    assert res["count"] == 64
    assert len(res["agents"]) == 64
    for a in res["agents"]:
        assert a["key"]
        assert a["name"]
        assert a["category"]
        assert a["responsibility"]


def test_libraries_endpoint():
    res = libraries()
    assert res["count"] > 0
    assert res["production_ready_claim"] is False
    assert "libraries" in res


def test_list_jobs_endpoint():
    res = list_jobs()
    assert "count" in res
    assert isinstance(res["jobs"], list)


def test_safe_job_id_regex():
    assert SAFE_JOB_ID_RE.match("bappus_biryani_campaign_20261016_153717")
    assert SAFE_JOB_ID_RE.match("job_1234567890ab")
    assert SAFE_JOB_ID_RE.match("f9828a3994c3")
    assert SAFE_JOB_ID_RE.match("alex-campaign-test")

    # Reject traversal / injection
    assert not SAFE_JOB_ID_RE.match("../etc/passwd")
    assert not SAFE_JOB_ID_RE.match("job/id")
    assert not SAFE_JOB_ID_RE.match("<script>")
    assert not SAFE_JOB_ID_RE.match("job.json")


def test_fastapi_http_endpoints_via_testclient():
    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app)

    # Health check
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "ok"

    # HTML home & Contact Details verification
    r_home = client.get("/")
    assert r_home.status_code == 200
    assert "ALEX DESIGN STUDIO OS" in r_home.text
    assert "Contact Us" in r_home.text
    assert "shubhamkothavale81@gmail.com" in r_home.text
    assert "7057539094" in r_home.text
    assert "linkedin.com/in/shubham-kothavale-b06089318" in r_home.text
    assert "instagram.com/shubham.kothavale0047" in r_home.text
    assert "contactModal" in r_home.text

    # Agents list
    r_agents = client.get("/api/agents")
    assert r_agents.status_code == 200
    assert r_agents.json()["count"] == 64

    # Library registry
    r_lib = client.get("/api/libraries")
    assert r_lib.status_code == 200
    assert r_lib.json()["count"] > 0

    # Jobs list
    r_jobs = client.get("/api/jobs")
    assert r_jobs.status_code == 200
    assert "jobs" in r_jobs.json()

    # Invalid job ID format -> 400
    r_bad_id = client.get("/api/jobs/invalid!id/json")
    assert r_bad_id.status_code == 400

    # Nonexistent safe job ID -> 404
    r_not_found = client.get("/api/jobs/nonexistent_job_123/json")
    assert r_not_found.status_code == 404

    # Campaign validation failure (brief too short) -> 422
    r_short = client.post("/api/campaign", json={"brief": "ab"})
    assert r_short.status_code == 422

    # Successful campaign generation
    r_camp = client.post("/api/campaign", json={
        "brief": "Artisan coffee roaster spring campaign",
        "offer_price": "₹199",
        "regular_price": "₹280",
    })
    assert r_camp.status_code == 200
    camp_data = r_camp.json()
    assert camp_data["status"] == "SUCCEEDED"
    assert "job_id" in camp_data
    jid = camp_data["job_id"]

    # Favicon
    r_fav = client.get("/favicon.ico")
    assert r_fav.status_code == 200
    assert "svg" in r_fav.headers.get("content-type", "")

    # Filtered agents
    r_filtered_agents = client.get("/api/agents?search=Copywriter")
    assert r_filtered_agents.status_code == 200
    assert r_filtered_agents.json()["count"] >= 1

    # Filtered libraries
    r_filtered_libs = client.get("/api/libraries?search=LangGraph")
    assert r_filtered_libs.status_code == 200
    assert r_filtered_libs.json()["count"] >= 1

    # Verify download of generated job
    r_dl_json = client.get(f"/api/jobs/{jid}/json")
    assert r_dl_json.status_code == 200
    assert r_dl_json.json()["campaign_name"]

    # Direct get_job JSON endpoint
    r_get_job = client.get(f"/api/jobs/{jid}")
    assert r_get_job.status_code == 200
    assert r_get_job.json()["campaign_name"] == r_dl_json.json()["campaign_name"]

    r_dl_md = client.get(f"/api/jobs/{jid}/markdown")
    assert r_dl_md.status_code == 200
    assert "# " in r_dl_md.text
