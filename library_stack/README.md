# ALEX ASI Graphics Design Library Stack

This registry is integrated with ALEX DESIGN STUDIO OS v0.9 as an optional extension layer. The current Render deployment keeps the existing lightweight FastAPI runtime; heavyweight AI/vision/video/3D dependencies are not installed by default.

## Workflow
1. Review `registry/libraries.json`.
2. Verify each library and license for the intended use.
3. Implement an adapter under the relevant service/module.
4. Add tests and pin dependencies.
5. Only then promote the library to production.

See `policies/ADOPTION_POLICY.md` and `docs/RENDER_DEPLOYMENT.md`.
