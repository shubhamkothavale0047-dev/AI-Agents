import pytest
from alex_design_studio_os.registry import create_all_agents
from alex_design_studio_os.agent_validation import validate_all_agents


def test_registered_agents_count_and_classes():
    agents = create_all_agents()
    assert len(agents) == 64, f"Expected 64 agents, found {len(agents)}"
    for key, agent in agents.items():
        assert hasattr(agent, "name")
        assert hasattr(agent, "spec")
        assert agent.spec.category
        assert agent.spec.responsibility


def test_agent_validation_contract():
    report = validate_all_agents("Unit test brief")
    assert report["all_passed"] is True
    assert report["roles_passed"] == 64
    assert report["roles_failed"] == 0
