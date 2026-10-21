"""Integration tests for dependency graph and 64-role execution."""
import json
from .orchestrator import build_dependency_graph, topological_order, run_agents_with_dependencies

def main():
    graph = build_dependency_graph(); order = topological_order(graph)
    assert len(graph) == 64, f"expected 64 nodes, got {len(graph)}"
    assert len(order) == 64 and len(set(order)) == 64, "topological order incomplete/duplicated"
    report = run_agents_with_dependencies("Bappu's Biryani premium Instagram offer poster", {"deliverables": ["poster", "caption", "story"]})
    assert report["scheduled_roles"] == 64, report["scheduled_roles"]
    assert report["completed_roles"] == 64, report["failed_roles"]
    assert report["all_completed"] is True
    assert any(report["agent_results"][k]["upstream_result_count"] > 0 for k in order), "no upstream outputs passed"
    assert report["independent_llm_calls"] == 0
    print(json.dumps({"test_suite":"dependency orchestration integration", "nodes":len(graph), "roles_scheduled":report["scheduled_roles"], "roles_completed":report["completed_roles"], "failed_roles":report["failed_roles"], "upstream_data_flow_verified":True, "llm_calls":0, "status":"PASS"}, indent=2))
if __name__ == '__main__': main()
