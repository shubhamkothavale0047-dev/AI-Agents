"""Contract and integration checks for all registered ALEX OS agent roles.

These checks validate the local agent interface and data propagation. They do not
claim that roles are independent LLMs or that external services are connected.
"""
from __future__ import annotations
from typing import Any
from .registry import create_all_agents

REQUIRED_RESULT_FIELDS = {
    "agent", "category", "status", "mode", "responsibility",
    "input_received", "summary", "human_review_required", "timestamp_utc",
}


def validate_all_agents(brief: str = "ALEX OS agent contract validation") -> dict[str, Any]:
    if not brief.strip():
        raise ValueError("brief must not be empty")
    agents = create_all_agents()
    checks: list[dict[str, Any]] = []
    for key, agent in agents.items():
        result = agent.run({"brief": brief, "upstream_context": {"source": "validator", "passed": True}})
        missing = sorted(REQUIRED_RESULT_FIELDS - set(result))
        checks.append({
            "key": key,
            "pass": not missing and result.get("status") == "COMPLETED"
                    and result.get("input_received") is True
                    and result.get("mode") == "LOCAL_TEMPLATE",
            "missing_fields": missing,
            "result_status": result.get("status"),
            "mode": result.get("mode"),
            "input_received": result.get("input_received"),
        })
    passed = sum(item["pass"] for item in checks)
    return {
        "suite": "ALEX OS 64-agent local contract validation",
        "registered_roles": len(agents),
        "roles_tested": len(checks),
        "roles_passed": passed,
        "roles_failed": len(checks) - passed,
        "all_passed": len(agents) == 64 and passed == len(agents),
        "execution_scope": "local template contract only; no external LLM/API/database calls",
        "checks": checks,
    }


def main() -> int:
    import json
    report = validate_all_agents()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["all_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
