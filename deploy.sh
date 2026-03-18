set -e
echo "Starting BULLETPROOF deployment..."

# Function to handle errors gracefully
handle_error() {
    echo "ERROR: $1" >&2
    exit 1
}

# Create necessary directories
mkdir -p backend/authentication backend/backend backend/dashboard
mkdir -p /workspace/frontend/src /workspace/frontend/public

# Validate Python/Django installation
if ! command -v python3 >/dev/null 2>&1; then
    handle_error "Python3 not found - please install Python 3.8+"
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Django dependencies..."
pip install -r requirements.txt

# Create .env file with safe defaults
cat <<'ENVEOF' > /workspace/.env
DEBUG=true
SECRET_KEY=local-development-key-change-in-production
DATABASE_URL=sqlite:///app.db
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
ENVEOF

# Run Django migrations
echo "Running Django migrations..."
cd backend
python manage.py makemigrations || echo "No new migrations"
python manage.py migrate || handle_error "Migration failed"

# Collect static files
python manage.py collectstatic --noinput || echo "No static files to collect"

# Start Django server
echo "Starting Django server on http://localhost:8000"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Handle shutdown gracefully
trap "kill $DJANGO_PID 2>/dev/null || true" EXIT

wait $DJANGO_PID
