#!/bin/sh
set -e

# Apply database migrations
echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Checking for OctoxLab user"
poetry run python manage.py create_test_user

echo "Checking for OctoxLab user"
poetry run python manage.py init_mock_elastic_data

echo "Starting tests"
poetry run python manage.py test

echo "Starting the celery beat schedule"
poetry run python manage.py create_beat_task

echo "Starting the Django development server..."
poetry run python -m debugpy --listen '0.0.0.0:5678' manage.py runserver 0.0.0.0:8000
