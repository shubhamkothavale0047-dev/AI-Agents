# Library Adoption Policy

A candidate must not be treated as production-ready until the team records: exact upstream project/repository, pinned version, license and commercial-use terms, security review, dependency compatibility, privacy/data handling, smoke tests, and an ALEX adapter owner.

- Do not install every candidate into the web service.
- Keep large model weights outside Git; use approved model/object storage.
- Keep secrets out of source control; use Render environment variables or a secret manager.
- AI outputs must pass task-specific QA and human approval before client delivery.
- Browser, code-execution, cyber-security and voice/identity tools require explicit authorization and scoped policies.
