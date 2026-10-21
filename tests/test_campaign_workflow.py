import pytest
from alex_design_studio_os.campaign_workflow import run_advertising_campaign
from alex_design_studio_os.workflow import run_core_pipeline


def test_campaign_workflow_empty_brief_raises_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        run_advertising_campaign("   ")


def test_core_pipeline_empty_brief_raises_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        run_core_pipeline("")


def test_campaign_workflow_execution(tmp_path):
    result = run_advertising_campaign(
        "Test campaign brief for artisanal bakery",
        offer_price="₹99",
        regular_price="₹150",
        output_dir=str(tmp_path),
    )
    assert "campaign" in result
    c = result["campaign"]
    assert c["campaign_name"]
    assert c["poster_copy"]["offer_price"] == "₹99"
    assert c["poster_copy"]["regular_price"] == "₹150"
    assert c["execution"]["all_roles_completed"] is True
    assert c["execution"]["agent_roles_completed"] == 64
    assert len(c["execution"]["agent_roles_failed"]) == 0
    assert (tmp_path / f"{c['campaign_name']}").exists is not None
