from pathlib import Path
import tempfile
from .campaign_workflow import run_advertising_campaign
from .registry import create_all_agents

def main():
    assert len(create_all_agents()) == 64
    with tempfile.TemporaryDirectory() as d:
        result = run_advertising_campaign("Bappu's Biryani — premium Instagram offer poster", output_dir=d)
        c = result["campaign"]
        assert c["execution"]["registered_agent_roles"] == 64
        assert c["execution"]["agent_roles_executed"] == 64
        assert c["execution"]["separate_llm_calls"] == 0
        assert Path(result["json_path"]).exists() and Path(result["markdown_path"]).exists()
        assert c["price_confirmation_required"] is True
    print("PASS: 64 roles executed in local template mode; campaign JSON/Markdown generated; price verification required; no live LLM claims.")
if __name__ == "__main__": main()
