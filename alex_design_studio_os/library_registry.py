"""Read-only registry of optional ALEX creative libraries."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "library_stack" / "registry" / "libraries.json"

def get_library_registry() -> dict:
    if not REGISTRY_PATH.is_file():
        return {
            "schema_version": "1.0",
            "project": "ALEX DESIGN STUDIO OS",
            "stack": "ALEX ASI Graphics Design Library Stack",
            "libraries": [],
            "count": 0,
            "production_ready_claim": False,
            "warning": f"Registry file not found at {REGISTRY_PATH}",
        }
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "schema_version": "1.0",
            "project": "ALEX DESIGN STUDIO OS",
            "stack": "ALEX ASI Graphics Design Library Stack",
            "libraries": [],
            "count": 0,
            "production_ready_claim": False,
            "error": f"Failed to load registry: {exc}",
        }
    data["count"] = len(data.get("libraries", []))
    data["production_ready_claim"] = False
    return data
