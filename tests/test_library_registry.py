from alex_design_studio_os.library_registry import get_library_registry

def test_library_registry_has_candidates_and_does_not_claim_production_ready():
    data = get_library_registry()
    assert data["count"] == len(data["libraries"])
    assert data["count"] > 0
    assert data["production_ready_claim"] is False
    assert all(item["installed_by_default"] is False for item in data["libraries"])
