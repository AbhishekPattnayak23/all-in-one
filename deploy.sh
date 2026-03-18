set -e

echo "=== Starting deployment ==="

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Build frontend
echo "Building frontend..."
npm run build

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
python -m pip install -r requirements.txt

# Initialize Django
echo "Initializing Django..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput || true

echo "Deployment completed successfully!"
echo "Run these commands to start:"
echo "Backend: cd backend && python manage.py runserver"
echo "Frontend: npm run dev"
