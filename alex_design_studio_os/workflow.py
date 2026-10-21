import json
from datetime import datetime, timezone
from pathlib import Path
from .registry import create_all_agents


def run_core_pipeline(brief: str, brand_guidelines=None):
    brief = brief.strip()
    if not brief:
        raise ValueError("Client brief cannot be empty.")

    agents = create_all_agents()
    payload = {"brief": brief, "brand_guidelines": brand_guidelines or {}}

    # The core workflow has explicit, deterministic local steps.
    brief_result = agents["ClientBriefAnalyzer"].run(payload)
    trend_result = agents["TrendAnalysisAgent"].run(payload)
    ideas_result = agents["CreativeIntelligenceAgent"].run({
        **payload, "brief_analysis": brief_result, "trend_hypotheses": trend_result
    })
    concept_result = agents["AdvertisingConceptAgent"].run({
        **payload, "ideas": ideas_result
    })
    brand_result = agents["BrandConsistencyAgent"].run({
        **payload, "concept": concept_result
    })

    report = {
        "system": "ALEX DESIGN STUDIO OS",
        "version": "0.1.0-local-scaffold",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_mode": "LOCAL_TEMPLATE_NOT_LLM",
        "client_brief": brief,
        "core_pipeline": {
            "client_brief_analysis": brief_result,
            "trend_analysis": trend_result,
            "creative_ideas": ideas_result,
            "advertising_concept": concept_result,
            "brand_consistency": brand_result,
        },
        "all_registered_agents": len(agents),
        "limitations": [
            "No live trend search in this local workflow.",
            "No OpenAI call or image/video generation is performed.",
            "Human review is required before client delivery."
        ]
    }
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"alex_project_{stamp}.json"
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    report["output_file"] = str(output_path)
    return report


def run_all_agent_roles(brief: str):
    """Smoke-run all registered roles with the same brief."""
    agents = create_all_agents()
    payload = {"brief": brief}
    return {key: agent.run(payload) for key, agent in agents.items()}
