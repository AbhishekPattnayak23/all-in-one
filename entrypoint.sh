set -e

# Fix for container environments
export PYTHONPATH="/workspace/backend:$PYTHONPATH"

# Execute deployment with logging
exec /workspace/deploy.sh >>/workspace/logs/deployment.log 2>&1
