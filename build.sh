#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
# python manage.py migrate

# temp for fixing migrations
rm -rf src/booking/migrations
python manage.py migrate