#!/bin/bash
echo "Setting up Flask user registration backend..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Creating database tables..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
echo "Setup complete! Run 'source venv/bin/activate && python run.py' to start the server"
