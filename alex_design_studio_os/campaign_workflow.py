import json
import re
from datetime import datetime, timezone
from pathlib import Path
from .registry import create_all_agents
from .orchestrator import run_agents_with_dependencies


def _synthesize_campaign_content(brief: str, offer_price: str, regular_price: str) -> dict:
    b_lower = brief.lower()

    # 1. Biryani / Bappu
    if "biryani" in b_lower or "bappu" in b_lower:
        brand = "BAPPU'S BIRYANI"
        name = "Bappu's Biryani — Biryani That Brings People Together"
        goal = "Promote a premium-looking chicken biryani offer across social channels"
        product = "Chicken Biryani"
        supporting = "Traditional Taste. Modern Experience."
        palette = ["matte black", "premium gold", "rich red"]
        hero = "steaming chicken biryani in a copper handi"
        caption = (
            f"🍗 Biryani cravings? We've got you covered!\n\n"
            f"Experience the rich flavours, aromatic rice and irresistible taste of Bappu's Biryani.\n\n"
            f"🔥 Special Chicken Biryani Offer — {offer_price}*\n"
            f"📲 Message us to order or ask about availability.\n\n"
            f"Bappu's Biryani — Biryani That Brings People Together.\n\n"
            f"*Confirm offer price, dates and availability before publishing.\n\n"
            f"#BappusBiryani #ChickenBiryani #BiryaniLovers #Foodie #BiryaniTime"
        )
        whatsapp = (
            f"🔥 BIRYANI LOVERS, THIS ONE'S FOR YOU!\n"
            f"🍗 BAPPU'S BIRYANI\n"
            f"❤️ Rich Flavours. Irresistible Taste.\n"
            f"CHICKEN BIRYANI — {offer_price}*\n"
            f"📲 Message us to order!\n"
            f"*Confirm offer price and availability before posting."
        )
        stories = [
            {"frame": 1, "copy": "Biryani craving झालीये का? 🍗"},
            {"frame": 2, "copy": "Bappu's Biryani — flavourful treat!"},
            {"frame": 3, "copy": f"Chicken Biryani {offer_price}*"},
            {"frame": 4, "copy": "आजच मेसेज करा आणि availability विचारा!"},
        ]
        qa = [
            "Confirm actual selling price and regular price",
            "Confirm offer dates and terms",
            "Add verified contact/order link",
            "Mention delivery platforms only if currently listed",
            "Review food imagery, logo rights and all claims",
        ]

    # 2. Coffee / Cafe / Roastery
    elif any(k in b_lower for k in ["coffee", "cafe", "roast", "espresso", "latte", "bakery"]):
        brand = "ARTISAN ROASTERS & CAFE"
        name = "Artisan Roasters — Crafted Morning Rituals"
        goal = "Promote specialty coffee brew combo and fresh artisanal pastries"
        product = "Specialty Brew & Pastry Combo"
        supporting = "Small Batch Roasted. Perfectly Crafted."
        palette = ["deep espresso", "warm beige", "forest emerald"]
        hero = "freshly poured velvety latte art beside warm flaky croissant"
        caption = (
            f"☕ Elevate your daily coffee ritual.\n\n"
            f"Savor our single-origin specialty roast paired with a fresh-baked flaky pastry.\n\n"
            f"✨ Limited Time Combo Offer — {offer_price}* (Regular {regular_price})\n"
            f"📍 Drop by our cafe or DM us to reserve your morning order.\n\n"
            f"Artisan Roasters — Better Beans. Better Days.\n\n"
            f"*Confirm combo inclusions and store hours.\n\n"
            f"#ArtisanCoffee #CoffeeRoasters #SpecialtyCoffee #CafeVibes #MorningRitual"
        )
        whatsapp = (
            f"☕ COFFEE LOVERS SPECIAL!\n"
            f"✨ ARTISAN ROASTERS & CAFE\n"
            f"Fresh roast single-origin brew + pastry combo.\n"
            f"SPECIAL OFFER — {offer_price}* (was {regular_price})\n"
            f"📍 Drop by today or reply to reserve!"
        )
        stories = [
            {"frame": 1, "copy": "Need your morning coffee fix? ☕"},
            {"frame": 2, "copy": "Small-batch roasted single origin beans."},
            {"frame": 3, "copy": f"Brew & Pastry Combo at {offer_price}*"},
            {"frame": 4, "copy": "DM us or stop by our counter today!"},
        ]
        qa = [
            "Confirm participating cafe locations and hours",
            "Verify bean roast date and origin claims",
            "Confirm allergen warnings for bakery items",
            "Review food styling visuals and licensed branding",
        ]

    # 3. Watch / Luxury / Jewelry
    elif any(k in b_lower for k in ["watch", "chrono", "luxury", "jewelry", "timepiece"]):
        brand = "CHRONO LUXE GENEVA"
        name = "Chrono Luxe — Precision Engineering & Timeless Design"
        goal = "Launch luxury chronograph timepiece with limited reservation offer"
        product = "Heritage Chronograph Series"
        supporting = "Precision Engineering. Timeless Elegance."
        palette = ["obsidian black", "brushed titanium", "sapphire blue"]
        hero = "precision mechanical chronograph on dark slate with dramatic rim light"
        caption = (
            f"⌚ Time defined by precision.\n\n"
            f"Introducing the Heritage Chronograph — aerospace-grade titanium, sapphire crystal and mechanical excellence.\n\n"
            f"💎 Exclusive Launch Edition — {offer_price}* (Retail {regular_price})\n"
            f"🔒 Numbered series with certificate of authenticity.\n\n"
            f"Chrono Luxe — Elegance That Outlasts Trends.\n\n"
            f"*Limited reservation window. Terms apply.\n\n"
            f"#ChronoLuxe #LuxuryWatches #WatchCollector #Horology #PrecisionEngineered"
        )
        whatsapp = (
            f"⌚ HERITAGE CHRONOGRAPH LAUNCH\n"
            f"💎 CHRONO LUXE GENEVA\n"
            f"Aerospace titanium · Sapphire crystal · Automatic movement\n"
            f"EXCLUSIVE LAUNCH OFFER — {offer_price}*\n"
            f"📲 Reply to reserve your numbered piece."
        )
        stories = [
            {"frame": 1, "copy": "Precision engineering meets timeless design. ⌚"},
            {"frame": 2, "copy": "Aerospace-grade titanium & sapphire glass."},
            {"frame": 3, "copy": f"Launch Edition: {offer_price}* (Save from {regular_price})"},
            {"frame": 4, "copy": "Reserve your numbered piece now — link in bio!"},
        ]
        qa = [
            "Verify serial number allocation and authenticity cert",
            "Confirm warranty duration and terms",
            "Ensure luxury branding guidelines are strictly met",
            "Validate all technical movement specifications",
        ]

    # 4. Fashion / Streetwear / Apparel
    elif any(k in b_lower for k in ["fashion", "streetwear", "clothing", "apparel", "hoodie", "drop"]):
        brand = "URBAN THREADS STUDIO"
        name = "Urban Threads — New Season Drop 01"
        goal = "Drive hype and pre-orders for new season oversized streetwear drop"
        product = "Heavyweight Oversized Collection"
        supporting = "Elevated Everyday Wear. Designed For Movement."
        palette = ["electric cobalt", "acid lime", "deep charcoal"]
        hero = "editorial streetwear portrait with dramatic neon city rim lighting"
        caption = (
            f"⚡ The new drop is here.\n\n"
            f"Drop 01 features our custom 450GSM heavyweight French terry cut with an exaggerated oversized silhouette.\n\n"
            f"🔥 Drop Week Special — {offer_price}* (Regular {regular_price})\n"
            f"📦 Free domestic shipping on orders placed this weekend.\n\n"
            f"Urban Threads — Built For The Streets.\n\n"
            f"*While stock lasts. Strictly limited batch.\n\n"
            f"#UrbanThreads #StreetwearDrop #HeavyweightTerry #OOTD #FashionEditorial"
        )
        whatsapp = (
            f"⚡ NEW SEASON DROP IS LIVE!\n"
            f"🔥 URBAN THREADS STUDIO\n"
            f"450GSM Heavyweight Oversized Terry.\n"
            f"EARLY ACCESS PRICE — {offer_price}*\n"
            f"📲 Message us with your size before it sells out!"
        )
        stories = [
            {"frame": 1, "copy": "The new season drop is finally live! ⚡"},
            {"frame": 2, "copy": "450GSM Custom French Terry. Boxy cut."},
            {"frame": 3, "copy": f"Drop Special: {offer_price}* (Regular {regular_price})"},
            {"frame": 4, "copy": "Tap link in bio to shop before sizes sell out!"},
        ]
        qa = [
            "Verify sizing chart accuracy (S, M, L, XL, XXL)",
            "Confirm warehouse inventory levels before launch",
            "Test checkout link and payment gateway integration",
            "Check color grading on mobile OLED displays",
        ]

    # 5. Tech / SaaS / AI / App
    elif any(k in b_lower for k in ["tech", "saas", "ai", "software", "app", "startup", "code"]):
        brand = "NEXUS AI PLATFORM"
        name = "Nexus AI — Multi-Agent Creative Intelligence"
        goal = "Drive signups and trial conversions for AI workflow automation platform"
        product = "Nexus Pro Annual Membership"
        supporting = "Automate Workflows. Supercharge Creative Velocity."
        palette = ["deep cyber dark", "neon cyan", "electric purple"]
        hero = "floating glassmorphic workflow graph with glowing interconnected agent nodes"
        caption = (
            f"🤖 Supercharge your creative velocity with multi-agent intelligence.\n\n"
            f"Coordinate strategy, copy, design QA, and campaign planning in one unified interface.\n\n"
            f"🚀 Launch Promo — {offer_price}* / seat (Regular {regular_price})\n"
            f"⚡ Instant setup with zero complex infrastructure required.\n\n"
            f"Nexus AI — Where Autonomous Teams Deliver Faster.\n\n"
            f"*Billed annually. Full 14-day money-back guarantee.\n\n"
            f"#NexusAI #AgentOrchestration #CreativeAI #SaaS #FutureOfWork"
        )
        whatsapp = (
            f"🤖 AUTOMATE YOUR CREATIVE WORKFLOW\n"
            f"🚀 NEXUS AI PRO\n"
            f"64 Specialized agents for end-to-end campaigns.\n"
            f"LAUNCH SPECIAL — {offer_price}* (Regular {regular_price})\n"
            f"📲 Reply to activate your 14-day trial!"
        )
        stories = [
            {"frame": 1, "copy": "Ready to 10x your campaign turnaround? 🤖"},
            {"frame": 2, "copy": "64 Agent roles coordinating your deliverables."},
            {"frame": 3, "copy": f"Pro Access Special: {offer_price}*"},
            {"frame": 4, "copy": "Start your free 14-day trial today — link in bio!"},
        ]
        qa = [
            "Verify signup authentication flow and token security",
            "Confirm server capacity and auto-scaling rules",
            "Check terms of service and GDPR data privacy notices",
            "Validate discount coupon code in billing processor",
        ]

    # 6. Generic / Custom Tailored
    else:
        # Extract title or brand from brief
        first_part = brief.split("—")[0].split("-")[0].split(":")[0].strip()
        brand = first_part.upper() if len(first_part) <= 30 else "SPECIAL CAMPAIGN"
        name = f"{brand} — Promotional Campaign"
        goal = f"Drive awareness and immediate conversions for {brand}"
        product = "Signature Offering"
        supporting = "Premium Quality. Unmatched Value."
        palette = ["midnight navy", "champagne gold", "clean white"]
        hero = f"dynamic hero product showcase for {brand} with crisp studio lighting"
        caption = (
            f"✨ Special Announcement from {brand}!\n\n"
            f"{brief}\n\n"
            f"🔥 Special Offer Price — {offer_price}* (Regular {regular_price})\n"
            f"📲 Connect with us today to take advantage of this exclusive offer.\n\n"
            f"*Confirm terms and dates before publishing.\n\n"
            f"#{brand.replace(' ', '')} #SpecialOffer #ExclusiveDeal #QualityFirst"
        )
        whatsapp = (
            f"🔥 EXCLUSIVE OFFER — {brand}!\n"
            f"Special deal on our signature offering.\n"
            f"NOW ONLY — {offer_price}* (was {regular_price})\n"
            f"📲 Message us now to claim this offer!"
        )
        stories = [
            {"frame": 1, "copy": f"Big news from {brand}! ✨"},
            {"frame": 2, "copy": "Crafted with care, designed for you."},
            {"frame": 3, "copy": f"Special Offer: {offer_price}* (was {regular_price})"},
            {"frame": 4, "copy": "DM us or tap link in bio to learn more!"},
        ]
        qa = [
            "Confirm final promotional price and active dates",
            "Verify all claims against client brand guidelines",
            "Check direct purchase or messaging contact links",
            "Review legal terms, disclaimers, and platform policies",
        ]

    return {
        "brand": brand,
        "campaign_name": name,
        "campaign_goal": goal,
        "product": product,
        "supporting": supporting,
        "palette": palette,
        "hero": hero,
        "caption": caption,
        "whatsapp": whatsapp,
        "stories": stories,
        "qa": qa,
    }


def run_advertising_campaign(brief: str, *, offer_price: str = "₹149", regular_price: str = "₹220", output_dir="outputs"):
    brief = brief.strip()
    if not brief:
        raise ValueError("Campaign brief cannot be empty.")
    agents = create_all_agents()

    content = _synthesize_campaign_content(brief, offer_price, regular_price)

    payload = {
        "brief": brief,
        "workflow": "advertising_campaign",
        "brand_guidelines": {"palette": content["palette"], "tone": "premium, engaging, clear"},
        "deliverables": [
            "Instagram feed poster",
            "Instagram caption",
            "WhatsApp Status copy",
            "Instagram Story sequence",
            "creative direction",
            "pre-publish QA",
        ],
        "offer_price": offer_price,
        "regular_price": regular_price,
    }

    # Execute all roles in dependency order, passing upstream summaries forward.
    orchestration = run_agents_with_dependencies(brief, payload)
    role_results = orchestration["agent_results"]

    campaign = {
        "campaign_name": content["campaign_name"],
        "client_brief": brief,
        "campaign_goal": content["campaign_goal"],
        "creative_direction": {
            "palette": content["palette"],
            "hero": content["hero"],
            "formats": {
                "Instagram feed": "1080x1350",
                "Instagram Story / WhatsApp Status": "1080x1920",
            },
        },
        "poster_copy": {
            "brand": content["brand"],
            "headline": "SPECIAL OFFER",
            "product": content["product"],
            "offer_price": offer_price,
            "regular_price": regular_price,
            "supporting_line": content["supporting"],
            "cta": "ORDER NOW",
        },
        "instagram_caption": content["caption"],
        "whatsapp_status": content["whatsapp"],
        "instagram_story_sequence": content["stories"],
        "pre_publish_checks": content["qa"],
        "price_confirmation_required": True,
        "execution": {
            "mode": orchestration["mode"],
            "registered_agent_roles": len(agents),
            "agent_roles_executed": orchestration["scheduled_roles"],
            "agent_roles_scheduled": orchestration["scheduled_roles"],
            "agent_roles_completed": orchestration["completed_roles"],
            "agent_roles_failed": orchestration["failed_roles"],
            "all_roles_completed": orchestration["all_completed"],
            "separate_llm_calls": orchestration["independent_llm_calls"],
            "dependency_aware": True,
            "live_web_research": False,
            "image_or_video_generated_by_this_module": False,
            "human_review_required": True,
        },
        "orchestration_report": orchestration,
        "agent_results": role_results,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", content["brand"].lower()).strip("_") or "campaign"
    json_path = out / f"{slug}_{stamp}.json"
    md_path = out / f"{slug}_{stamp}.md"

    json_path.write_text(json.dumps(campaign, indent=2, ensure_ascii=False), encoding="utf-8")
    palette_str = ", ".join(content["palette"])
    story_str = "\n".join(f"{x['frame']}. {x['copy']}" for x in content["stories"])
    qa_str = "\n".join(f"- {x}" for x in content["qa"])

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
{story_str}

## Creative direction
- Palette: {palette_str}
- Hero visual: {content['hero']}
- Feed: 1080 × 1350 px; Story/Status: 1080 × 1920 px.

## Before publishing
{qa_str}

*Prices must be confirmed by the client.

## Execution transparency
- Registered roles: {len(agents)}; local role calls: {len(role_results)}.
- Mode: local deterministic templates; 0 separate LLM calls.
- This is not proof of 64 independent AI models. Human review required.
"""
    md_path.write_text(md, encoding="utf-8")
    return {"campaign": campaign, "json_path": str(json_path), "markdown_path": str(md_path)}
