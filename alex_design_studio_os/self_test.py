from .registry import AGENT_REGISTRY, create_all_agents
from .workflow import run_core_pipeline, run_all_agent_roles


def main():
    agents = create_all_agents()
    assert len(AGENT_REGISTRY) == 64, f"Expected 64 agents, got {len(AGENT_REGISTRY)}"
    assert len(agents) == 64
    for key, agent in agents.items():
        result = agent.run({"brief": "Self-test brief"})
        assert result["agent"] == key
        assert result["status"] == "COMPLETED"
    outputs = run_all_agent_roles("Self-test brief")
    assert len(outputs) == 64
    report = run_core_pipeline("Business: Demo; Product: Creative services; Goal: campaign")
    assert report["all_registered_agents"] == 64
    assert report["core_pipeline"]["brand_consistency"]["status"] == "COMPLETED"
    print("PASS: 64 agent roles registered and callable.")
    print("PASS: Core pipeline completed in local template mode.")
    print("Output file:", report["output_file"])
    print("NOTE: This test does not verify external AI, Redis/Celery, PostgreSQL, or deployment.")


if __name__ == "__main__":
    main()
