#!/bin/sh
set -e

echo "Waiting for postgres..."

# Function to verify postgres connection
postgres_ready() {
    python << END
import sys
import psycopg2
import time
import os

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        psycopg2.connect(
            dbname="myapp",
            user="postgres",
            password="password",
            host="db"
        )
        sys.exit(0)
    except psycopg2.OperationalError:
        attempt += 1
        time.sleep(1)

sys.exit(-1)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Run database migrations
echo "Running database migrations..."
flask db upgrade || exit 1

# Start Gunicorn with error handling
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 \
    --workers 3 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --log-level debug \
    "app:create_app()"