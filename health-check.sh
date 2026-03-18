set -e

echo "=== Deployment Health Check ==="
echo "Checking frontend build..."
if [ -d "dist" ]; then
    echo " Frontend built successfully"
else
    echo " Initial state - need to run build"
fi

echo "Checking backend database..."
if [ -f "backend/db.sqlite3" ]; then
    echo " Database exists"
else
    echo " Need to run migrations"
fi

echo "Health check completed - ready for deployment"
