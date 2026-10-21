from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class AgentSpec:
    key: str
    name: str
    category: str
    responsibility: str


class BaseAgent:
    """Consistent interface for a local agent role; no external AI calls."""

    spec: AgentSpec

    @property
    def name(self) -> str:
        return self.spec.name

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = str(payload.get("brief", "")).strip()
        return {
            "agent": self.spec.name,
            "category": self.spec.category,
            "status": "COMPLETED",
            "mode": "LOCAL_TEMPLATE",
            "responsibility": self.spec.responsibility,
            "input_received": bool(brief),
            "summary": self._summary(payload),
            "human_review_required": True,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }

    def _summary(self, payload: Dict[str, Any]) -> str:
        brief = str(payload.get("brief", "")).strip()
        if brief:
            return f"{self.spec.responsibility} Input brief received: {brief[:240]}"
        return self.spec.responsibility
