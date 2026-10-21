# Render Deployment

The existing `render.yaml` deploys the FastAPI application from this project root. It does not install all candidate AI libraries.

1. Push the contents of `AI-Agents-main/` to a GitHub repository.
2. In Render, create a Blueprint and select the repository.
3. Confirm the root directory is the repository root and use `render.yaml`.
4. Set secrets such as `OPENAI_API_KEY` only in Render Environment settings, never in Git.
5. Verify `/health`, `/docs`, `/api/agents`, and `/api/libraries` after deployment.
6. Configure a managed PostgreSQL database and `DATABASE_URL` if persistent job storage is required.

Important: `/tmp` and the local filesystem on typical Render web services should not be treated as durable storage. Use PostgreSQL/object storage for production persistence. The free instance may sleep and is suitable for demos, not uptime guarantees.
