# Agent - re-deploy recovery branch

This branch contains only the minimal configuration and meta files required
for the CI system to clone & boot the application the *first* time.

Once deployed, the normalized application tree is expected in:

/workspace/frontend   - React + Vite + TypeScript assets
/workspace/backend    - Django monolith with REST API and ASGI Channels

If you re-deploy a new revision of your application code, commit the actual
application code (beyond this skeleton) to any appropriate long-lived branch
and update your CI to target that branch.
