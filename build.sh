#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# 1. Generate the database blueprints
python manage.py makemigrations

# 2. Build the database tables
python manage.py migrate

# 3. Add the dummy data
python setup_data.py