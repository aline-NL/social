#!/bin/bash

# Exit on error
set -e

# Start the Gunicorn server
echo "=== Starting Gunicorn server ==="
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 4 --worker-class gthread --threads 2 --log-file -
