#!/bin/bash

# Exit on error
set -e

# Print environment information
echo "=== Environment Information ==="
python --version
pip --version
node --version
npm --version

# Backend setup
echo "=== Installing Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies if not already installed
if ! command -v node &> /dev/null; then
    echo "=== Installing Node.js ==="
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install serve globally if not already installed
if ! command -v serve &> /dev/null; then
    echo "=== Installing serve globally ==="
    npm install -g serve
fi

# Run database migrations
echo "=== Running database migrations ==="
python manage.py migrate --noinput

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Frontend setup
echo "=== Setting up frontend ==="
cd frontend

# Install Node.js dependencies
echo "=== Installing Node.js dependencies ==="
npm install

# Install serve as a dev dependency if not already installed
if ! grep -q "serve" package.json; then
    echo "=== Adding serve to package.json ==="
    npm install --save-dev serve
fi

# Build the frontend for production
echo "=== Building frontend for production ==="
npm run build:prod

# Create the frontend-dist directory in the project root if it doesn't exist
mkdir -p ../frontend-dist

# Copy build output to the frontend-dist directory
echo "=== Copying build output to frontend-dist ==="
cp -r dist/. ../frontend-dist/

# Go back to the project root
cd ..

# Install serve in the root directory
echo "=== Installing serve in root directory ==="
npm install serve --save

echo "=== Build completed successfully! ==="
