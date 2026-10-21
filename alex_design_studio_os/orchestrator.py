"""Dependency-aware local orchestrator for the 64 registered ALEX OS roles.

This runs role implementations in-process in dependency order. Current roles are
local template agents; this is not a claim of 64 independent LLMs.
"""
from __future__ import annotations
from collections import defaultdict, deque
from datetime import datetime, timezone
from time import perf_counter
from typing import Any
from .registry import AGENT_REGISTRY, create_all_agents

# Explicit stage dependencies. Roles not named in the map are attached to the
# nearest stage using their category; every registered role is still scheduled.
STAGE_GROUPS = {
    "brief_strategy": ["AlexAIAssistant", "AlexAIDirector", "CreativeIntelligenceAgent", "ClientBriefAnalyzer", "CreativeStrategyAgent", "CampaignPlannerAgent", "ProjectManagementAgent"],
    "research": ["TrendAnalysisAgent", "ResearchAgent", "AudienceIntelligenceAgent", "MarketingAnalystAgent", "PerformanceAnalyticsAgent", "FeedbackLearningAgent"],
    "brand": ["BrandStrategistAgent", "BrandConsistencyAgent", "ColorIntelligenceAgent", "TypographyAgent", "MarathiTypographyAgent", "LocalizationAgent"],
    "content": ["AICopywriterAgent", "AdvertisingConceptAgent", "SocialMediaManagerAgent", "CTAOptimizationAgent", "ContentCalendarAgent", "PricingAssistantAgent", "PromptEngineeringAgent"],
    "design": ["AIArtDirector", "GraphicDesignerAgent", "DesignRecommendationEngine", "LayoutAgent", "ImageSelectionAgent", "IllustrationAgent", "BackgroundTextureAgent", "MockupAgent", "ThreeDDesignAgent", "DesignAdaptationAgent", "AutonomousCreativeDirector"],
    "media": ["ImageGenerationAgent", "ImageEditingAgent", "ProductPhotographyAgent", "FoodAdvertisingAgent", "AIVideoDirectorAgent", "VideoGenerationAgent", "MotionGraphicsAgent", "SceneContinuityAgent", "VoiceAudioAgent", "VideoEditingAgent"],
    "engineering": ["AssetPipelineAgent", "PluginRegistryAgent", "SecurityAgent", "SystemHealthAgent", "CostMonitoringAgent", "WorkflowOrchestratorAgent", "JobMonitoringAgent", "ErrorRecoveryAgent"],
    "qa_delivery": ["DesignQAAgent", "AIDesignCritic", "BrandComplianceAgent", "AssetLicensingAgent", "ExportAgent", "ClientDeliveryAgent", "RevisionAgent", "ClientManagementAgent"],
}
STAGE_ORDER = list(STAGE_GROUPS)

def build_dependency_graph() -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {key: [] for key in AGENT_REGISTRY}
    stage_for: dict[str, str] = {}
    for stage, keys in STAGE_GROUPS.items():
        for key in keys:
            if key in graph:
                stage_for[key] = stage
    # Fill unmapped roles into a stage based on names/categories, ensuring coverage.
    for key in graph:
        if key not in stage_for:
            low = key.lower()
            if any(s in low for s in ("brand", "color", "typography", "localization")): stage_for[key] = "brand"
            elif any(s in low for s in ("copy", "social", "campaign", "pricing", "prompt", "calendar")): stage_for[key] = "content"
            elif any(s in low for s in ("image", "video", "motion", "audio", "scene", "photography")): stage_for[key] = "media"
            elif any(s in low for s in ("qa", "compliance", "licensing", "export", "delivery", "revision")): stage_for[key] = "qa_delivery"
            elif any(s in low for s in ("research", "trend", "audience", "analytics", "feedback", "market")): stage_for[key] = "research"
            elif any(s in low for s in ("security", "system", "plugin", "pipeline", "monitor", "recovery", "cost")): stage_for[key] = "engineering"
            elif any(s in low for s in ("design", "layout", "mockup", "illustration", "texture", "artdirector")): stage_for[key] = "design"
            else: stage_for[key] = "brief_strategy"
    for key, stage in stage_for.items():
        idx = STAGE_ORDER.index(stage)
        if idx > 0:
            # Depend on all agents in the immediately previous stage, making
            # outputs flow forward without introducing cycles.
            graph[key] = [dep for dep in STAGE_GROUPS[STAGE_ORDER[idx - 1]] if dep in graph and dep != key]
    # Ensure first stage is independent; subsequent stages depend on previous stage.
    return graph

def topological_order(graph: dict[str, list[str]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    children: dict[str, list[str]] = defaultdict(list)
    for node, deps in graph.items():
        for dep in deps:
            if dep not in graph:
                raise ValueError(f"Unknown dependency {dep!r} for {node!r}")
            indegree[node] += 1
            children[dep].append(node)
    queue = deque(node for node in graph if indegree[node] == 0)
    ordered = []
    while queue:
        node = queue.popleft(); ordered.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0: queue.append(child)
    if len(ordered) != len(graph):
        raise ValueError("Dependency graph contains a cycle")
    return ordered

def run_agents_with_dependencies(brief: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not brief.strip(): raise ValueError("brief must not be empty")
    graph = build_dependency_graph(); order = topological_order(graph); agents = create_all_agents()
    base_payload = dict(payload or {}); base_payload["brief"] = brief
    results: dict[str, dict[str, Any]] = {}; execution_log = []
    started = datetime.now(timezone.utc).isoformat(); overall = perf_counter()
    for key in order:
        upstream = {dep: {"status": results[dep].get("status"), "summary": results[dep].get("summary"), "mode": results[dep].get("mode")} for dep in graph[key] if dep in results}
        agent_payload = {**base_payload, "agent_key": key, "dependencies": graph[key], "upstream_context": upstream}
        tick = perf_counter()
        try:
            result = agents[key].run(agent_payload)
            ok = isinstance(result, dict) and result.get("status") == "COMPLETED" and result.get("input_received") is True
            if not isinstance(result, dict): raise TypeError("Agent result must be a dictionary")
            result = {**result, "agent_key": key, "dependency_keys": graph[key], "upstream_result_count": len(upstream)}
            if not ok: result["status"] = "FAILED"
            results[key] = result
            execution_log.append({"agent_key": key, "status": result.get("status"), "dependency_count": len(graph[key]), "upstream_result_count": len(upstream), "duration_ms": round((perf_counter()-tick)*1000, 3), "error": None if ok else "Agent contract/status check failed"})
        except Exception as exc:
            results[key] = {"agent_key": key, "status": "FAILED", "mode": "LOCAL_TEMPLATE", "error": f"{type(exc).__name__}: {exc}"}
            execution_log.append({"agent_key": key, "status": "FAILED", "dependency_count": len(graph[key]), "upstream_result_count": len(upstream), "duration_ms": round((perf_counter()-tick)*1000, 3), "error": f"{type(exc).__name__}: {exc}"})
    failed = [x["agent_key"] for x in execution_log if x["status"] != "COMPLETED"]
    return {"started_at_utc": started, "duration_ms": round((perf_counter()-overall)*1000, 3), "registered_roles": len(agents), "scheduled_roles": len(order), "completed_roles": len(order)-len(failed), "failed_roles": failed, "all_completed": len(order)==64 and not failed, "mode": "LOCAL_TEMPLATE_DEPENDENCY_ORCHESTRATION", "independent_llm_calls": 0, "dependency_graph": graph, "execution_order": order, "execution_log": execution_log, "agent_results": results}
