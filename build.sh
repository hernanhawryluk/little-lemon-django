#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
# python manage.py migrate

# temp for fixing migrations
python manage.py migrate booking zero
rm -f booking/migrations/*
python manage.py makemigrations booking
python manage.py migrate
