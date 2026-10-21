"""Advertising campaign workflow orchestrating all 64 registered roles locally.

This is a deterministic local orchestration scaffold, not 64 independent LLM calls.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from .registry import create_all_agents
from .orchestrator import run_agents_with_dependencies


def run_advertising_campaign(brief: str, *, offer_price: str = "₹149", regular_price: str = "₹220", output_dir="outputs"):
    brief = brief.strip()
    if not brief:
        raise ValueError("Campaign brief cannot be empty.")
    agents = create_all_agents()
    payload = {
        "brief": brief,
        "workflow": "advertising_campaign",
        "brand_guidelines": {"palette": ["matte black", "premium gold", "rich red"], "tone": "premium, appetising, warm"},
        "deliverables": ["Instagram feed poster", "Instagram caption", "WhatsApp Status copy", "Instagram Story sequence", "creative direction", "pre-publish QA"],
        "offer_price": offer_price,
        "regular_price": regular_price,
    }
    # Execute all roles in dependency order, passing upstream summaries forward.
    orchestration = run_agents_with_dependencies(brief, payload)
    role_results = orchestration["agent_results"]
    # The deliverable below is authored campaign content; all prices are flagged for owner confirmation.
    campaign = {
        "campaign_name": "Bappu's Biryani — Biryani That Brings People Together",
        "client_brief": brief,
        "campaign_goal": "Promote a premium-looking chicken biryani offer across social channels",
        "creative_direction": {"palette": ["matte black", "premium gold", "rich red"], "hero": "steaming chicken biryani in a copper handi", "formats": {"Instagram feed": "1080x1350", "Instagram Story / WhatsApp Status": "1080x1920"}},
        "poster_copy": {"brand": "BAPPU'S BIRYANI", "headline": "SPECIAL OFFER", "product": "Chicken Biryani", "offer_price": offer_price, "regular_price": regular_price, "supporting_line": "Traditional Taste. Modern Experience.", "cta": "ORDER NOW"},
        "instagram_caption": "🍗 Biryani cravings? We've got you covered!\n\nExperience the rich flavours, aromatic rice and irresistible taste of Bappu's Biryani.\n\n🔥 Special Chicken Biryani Offer — " + offer_price + "*\n📲 Message us to order or ask about availability.\n\nBappu's Biryani — Biryani That Brings People Together.\n\n*Confirm offer price, dates and availability before publishing.\n\n#BappusBiryani #ChickenBiryani #BiryaniLovers #Foodie #BiryaniTime",
        "whatsapp_status": "🔥 BIRYANI LOVERS, THIS ONE'S FOR YOU!\n🍗 BAPPU'S BIRYANI\n❤️ Rich Flavours. Irresistible Taste.\nCHICKEN BIRYANI — " + offer_price + "*\n📲 Message us to order!\n*Confirm offer price and availability before posting.",
        "instagram_story_sequence": [{"frame": 1, "copy": "Biryani craving झालीये का? 🍗"}, {"frame": 2, "copy": "Bappu's Biryani — flavourful treat!"}, {"frame": 3, "copy": "Chicken Biryani " + offer_price + "*"}, {"frame": 4, "copy": "आजच मेसेज करा आणि availability विचारा!"}],
        "pre_publish_checks": ["Confirm actual selling price and regular price", "Confirm offer dates and terms", "Add verified contact/order link", "Mention delivery platforms only if currently listed", "Review food imagery, logo rights and all claims"],
        "price_confirmation_required": True,
        "execution": {"mode": orchestration["mode"], "registered_agent_roles": len(agents), "agent_roles_executed": orchestration["scheduled_roles"], "agent_roles_scheduled": orchestration["scheduled_roles"], "agent_roles_completed": orchestration["completed_roles"], "agent_roles_failed": orchestration["failed_roles"], "all_roles_completed": orchestration["all_completed"], "separate_llm_calls": orchestration["independent_llm_calls"], "dependency_aware": True, "live_web_research": False, "image_or_video_generated_by_this_module": False, "human_review_required": True},
        "orchestration_report": orchestration,
        "agent_results": role_results,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    json_path = out / f"bappus_biryani_campaign_{stamp}.json"
    md_path = out / f"bappus_biryani_campaign_{stamp}.md"
    json_path.write_text(json.dumps(campaign, indent=2, ensure_ascii=False), encoding='utf-8')
    md = f"""# {campaign['campaign_name']}

## Poster copy
**{campaign['poster_copy']['headline']}**

### {campaign['poster_copy']['product']} — {offer_price}*
~~{regular_price}~~

{campaign['poster_copy']['supporting_line']}

**CTA: {campaign['poster_copy']['cta']}**

## Instagram caption
{campaign['instagram_caption']}

## WhatsApp Status
{campaign['whatsapp_status']}

## Story sequence
""" + '\n'.join(f"{x['frame']}. {x['copy']}" for x in campaign['instagram_story_sequence']) + "\n\n## Creative direction\n- Matte black, premium gold and rich red.\n- Hero: steaming chicken biryani in a copper handi.\n- Feed: 1080 × 1350 px; Story/Status: 1080 × 1920 px.\n\n## Before publishing\n" + '\n'.join(f"- {x}" for x in campaign['pre_publish_checks']) + f"\n\n*Prices must be confirmed by the client.\n\n## Execution transparency\n- Registered roles: {len(agents)}; local role calls: {len(role_results)}.\n- Mode: local deterministic templates; 0 separate LLM calls.\n- This is not proof of 64 independent AI models. Human review required.\n"
    md_path.write_text(md, encoding='utf-8')
    return {"campaign": campaign, "json_path": str(json_path), "markdown_path": str(md_path)}
