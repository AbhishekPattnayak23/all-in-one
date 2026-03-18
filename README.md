
--- Tactical Deployment Fix Note (Coding Agent action):
The preview environment previously used branch 'agent/integration', but this branch has been removed from origin.
Repair: created `.deploy.yml` directing infra to check out 'main' instead.
No application logic was changed; this change solely affects deployment metadata.
