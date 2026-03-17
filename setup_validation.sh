#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r project_root/backend/requirements.txt
cd project_root/backend
python manage.py makemigrations
python manage.py migrate
python manage.py check
