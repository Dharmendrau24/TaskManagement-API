#!/bin/sh

echo "Running database migrations..."

python -m alembic upgrade head

echo "Starting FastAPI..."

exec uvicorn main:app --host 0.0.0.0 --port 8000