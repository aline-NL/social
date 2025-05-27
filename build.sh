#!/bin/bash

# Exit on error
set -e

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Running database migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Building frontend ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Build complete ==="
