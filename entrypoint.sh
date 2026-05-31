#!/bin/bash
set -e

cd /app

# Install dependencies
pip install -r requirements.txt

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until python -c "
import os, sys
import psycopg2
try:
    psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'team_finder'),
        user=os.environ.get('POSTGRES_USER', 'team_finder'),
        password=os.environ.get('POSTGRES_PASSWORD', 'team_finder'),
        host=os.environ.get('POSTGRES_HOST', 'db'),
        port=os.environ.get('POSTGRES_PORT', '5432'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
  echo "PostgreSQL not ready, waiting..."
  sleep 2
done
echo "PostgreSQL is ready."

# Run migrations
python manage.py migrate --no-input

# Create test data
python manage.py create_test_data

# Start dev server
python manage.py runserver 0.0.0.0:8000
