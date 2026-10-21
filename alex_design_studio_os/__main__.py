"""Unified CLI for ALEX DESIGN STUDIO OS workflows."""
import argparse
import json
from .workflow import run_core_pipeline
from .ai_workflow import run_ai_pipeline
from .campaign_workflow import run_advertising_campaign


def main():
    parser = argparse.ArgumentParser(description="ALEX DESIGN STUDIO OS — integrated 64-role workflow")
    parser.add_argument("--mode", choices=("local", "openai"), default="local",
                        help="local works offline; openai requires OPENAI_API_KEY")
    parser.add_argument("--workflow", choices=("core", "advertising"), default="core",
                        help="Choose the core design workflow or 64-role advertising campaign")
    parser.add_argument("--brief", default=None, help="Client brief; if omitted, prompt interactively")
    parser.add_argument("--model", default=None, help="Optional OpenAI model override")
    parser.add_argument("--offer-price", default="₹149", help="Campaign offer price (must be client-confirmed)")
    parser.add_argument("--regular-price", default="₹220", help="Regular price (must be client-confirmed)")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated campaign reports")
    args = parser.parse_args()

    print("ALEX DESIGN STUDIO OS — Integrated Workflow")
    print("Workflow:", args.workflow, "| Mode:", args.mode)
    brief = (args.brief or input("Enter client brief (business, product, audience, goal): ")).strip()
    try:
        if args.workflow == "advertising":
            if args.mode == "openai":
                print("Note: advertising workflow currently uses local role templates; OpenAI calls are not made in this workflow.")
            result = run_advertising_campaign(brief, offer_price=args.offer_price,
                                              regular_price=args.regular_price,
                                              output_dir=args.output_dir)
            print(json.dumps({"campaign_name": result["campaign"]["campaign_name"],
                              "execution": result["campaign"]["execution"],
                              "markdown_path": result["markdown_path"],
                              "json_path": result["json_path"]}, indent=2, ensure_ascii=False))
        elif args.mode == "openai":
            report = run_ai_pipeline(brief, model=args.model)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            print("\nSaved output:", report["output_file"])
        else:
            report = run_core_pipeline(brief)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            print("\nSaved output:", report["output_file"])
    except Exception as exc:
        print(f"Pipeline error: {type(exc).__name__}: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
