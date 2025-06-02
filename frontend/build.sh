#!/bin/bash

# Exit on error
set -e

# Print environment information
echo "=== Environment Information ==="
node --version
npm --version

# Install dependencies
echo "=== Installing dependencies ==="
npm install

# Install serve globally
echo "=== Installing serve globally ==="
npm install -g serve

# Build the app for production
echo "=== Building the app for production ==="
npm run build:prod

echo "=== Build completed successfully! ==="

# Create the frontend-dist directory in the project root
mkdir -p ../frontend-dist

# Copy build output to the frontend-dist directory
echo "=== Copying build output to frontend-dist ==="
cp -r dist/. ../frontend-dist/

echo "=== Build output copied to frontend-dist successfully! ==="
