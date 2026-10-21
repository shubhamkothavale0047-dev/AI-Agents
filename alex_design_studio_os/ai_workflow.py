"""One-call AI workflow for a complete creative brief; requires a valid API key."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .ai_provider import generate_text


def run_ai_pipeline(brief: str, model: str | None = None) -> dict:
    brief = brief.strip()
    if not brief:
        raise ValueError("Client brief cannot be empty.")
    prompt = f"""
Create a client-ready creative strategy pack for ALEX DESIGN STUDIO OS using the brief below.
Return clear Markdown with these headings:
1. Brief understanding
2. Target audience and objective
3. Three distinct creative concepts
4. Recommended concept and rationale
5. Visual direction (layout, palette, typography, imagery)
6. Marathi/Hindi/English copy options when appropriate
7. Deliverables and platform sizes
8. Production checklist
9. Licensing, factual claims, and brand-safety checks
10. Assumptions and items needing client approval

Rules:
- Do not claim you checked live trends, websites, or competitors.
- Do not invent client facts; mark unknowns as questions.
- Do not suggest copyrighted assets for commercial use unless the licence is verified.
- Clearly distinguish recommendations from verified facts.
- Make the result specific to the supplied brief.

CLIENT BRIEF:
{brief}
"""
    generated = generate_text(prompt, model=model)
    report = {
        "system": "ALEX DESIGN STUDIO OS",
        "version": "0.2.0-openai-provider",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_mode": "OPENAI_RESPONSES_API",
        "model": model or __import__("os").getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "client_brief": brief,
        "creative_strategy": generated,
        "limitations": [
            "This is one model call, not 64 independent AI agents.",
            "Live web research and image/video generation are not performed.",
            "Review all client-facing copy, claims, licences, and prices before delivery."
        ],
    }
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"alex_ai_project_{stamp}.json"
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    report["output_file"] = str(output_path)
    return report
