from .agent_validation import validate_all_agents

def main():
    report = validate_all_agents("Bappu's Biryani premium Instagram offer poster")
    assert report["registered_roles"] == 64, report
    assert report["roles_tested"] == 64, report
    assert report["roles_passed"] == 64, report
    assert report["roles_failed"] == 0, report
    assert report["all_passed"] is True, report
    print("PASS: all 64 registered roles satisfy the local result contract and receive the supplied brief.")
    print("SCOPE: local templates only; this does not prove 64 independent AI models or live API connectivity.")

if __name__ == "__main__":
    main()
