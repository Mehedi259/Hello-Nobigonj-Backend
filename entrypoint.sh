#!/bin/sh
set -e

echo "==> Starting Hello Nobigonj Backend Service..."

# Wait for PostgreSQL if configured
if [ -n "$DB_HOST" ] && [ "$USE_SQLITE" != "True" ] && [ "$USE_SQLITE" != "true" ]; then
  echo "==> Checking PostgreSQL readiness on $DB_HOST:$DB_PORT..."
  python - << 'PYEOF'
import socket
import time
import os

host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', 5432))
connected = False
for i in range(30):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"==> Successfully connected to PostgreSQL on {host}:{port}")
            connected = True
            break
    except OSError:
        time.sleep(1)

if not connected:
    print(f"==> Warning: Could not connect to {host}:{port} within 30 seconds.")
PYEOF
fi

echo "==> Applying database migrations..."
python manage.py migrate --noinput

echo "==> Seeding initial realistic data..."
python manage.py seed_nobigonj_data || true

echo "==> Collecting static files..."
python manage.py collectstatic --noinput || true

echo "==> Starting Gunicorn Application Server..."
exec "$@"

