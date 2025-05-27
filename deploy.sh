#!/bin/bash

# Exit on error
set -e

echo "=== Starting deployment to Render ==="

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "Error: render.yaml not found!"
    exit 1
fi

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "Render CLI not found. Installing..."
    curl -s https://cli.render.com/install.sh | bash
    
    # Add render to PATH if not already there
    if ! grep -q "render" ~/.bashrc; then
        echo 'export PATH="$HOME/.render/cli/current/render:$PATH"' >> ~/.bashrc
        source ~/.bashrc
    fi
    
    echo "Render CLI installed. Please log in to your Render account."
    render auth login
fi

# Deploy to Render
echo "=== Deploying to Render... ==="
render deploy

echo "=== Deployment complete! ==="
