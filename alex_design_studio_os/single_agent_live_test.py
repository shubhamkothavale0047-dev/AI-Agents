"""Run one live OpenAI-backed Creative Intelligence Agent test.

Usage:
  export OPENAI_API_KEY='your-key'
  python -m alex_design_studio_os.single_agent_live_test

This script makes a real API call only when you run it with your own key.
It never prints or saves the API key.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .ai_provider import AIProviderError, generate_text


def main():
    brief = input(
        "Client brief (e.g. Pune dairy farm Instagram campaign): "
    ).strip()
    if not brief:
        raise SystemExit("ERROR: Please enter a client brief.")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        raise SystemExit(
            "NOT RUN: OPENAI_API_KEY is missing. Set your own key in Termux; "
            "do not paste it into chat or save it in source code."
        )

    prompt = f"""
You are the Creative Intelligence Agent in ALEX DESIGN STUDIO OS.
Analyze this client brief and produce:
1. Brief interpretation
2. Target audience assumptions (label assumptions)
3. Three distinct creative concepts
4. Best concept with rationale
5. Visual direction and suggested palette
6. Short headline, supporting copy, and CTA
7. Production checklist
8. Risks, unverified claims, and human approvals required

Do not claim live research, image/video generation, or facts not in the brief.
Keep the output client-ready and clearly mark unknowns.

CLIENT BRIEF:
{brief}
"""
    try:
        result_text = generate_text(prompt)
    except AIProviderError as exc:
        raise SystemExit(f"LIVE API TEST FAILED: {exc}") from exc

    report = {
        "system": "ALEX DESIGN STUDIO OS",
        "test": "single_agent_live_test",
        "agent": "CreativeIntelligenceAgent",
        "status": "PASS — API returned non-empty model output",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "client_brief": brief,
        "result": result_text,
        "limitations": [
            "This validates one API-backed agent workflow only.",
            "It does not prove all 64 agents are independently AI-powered.",
            "Human review is required before client delivery."
        ]
    }
    outdir = Path("outputs")
    outdir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    outpath = outdir / f"single_agent_live_test_{stamp}.json"
    outpath.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n=== LIVE AGENT TEST: PASS ===")
    print("Agent:", report["agent"])
    print("Model:", report["model"])
    print("Output saved:", outpath)
    print("\n=== GENERATED RESULT ===\n")
    print(result_text)


if __name__ == "__main__":
    main()
