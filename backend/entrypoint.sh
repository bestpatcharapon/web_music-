#!/bin/sh
# Use PORT from environment or default to 8080
PORT=${PORT:-8080}
echo "Starting gunicorn on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
