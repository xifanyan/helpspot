#!/bin/bash
# Spark CLI wrapper - loads credentials from .env file securely
# Usage: ./spark.sh categories list --active-only

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file with your Spark credentials:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your credentials"
    exit 1
fi

# Load environment variables from .env file
set -a
source .env
set +a

# Run the helpspot command with all arguments passed to this script
uv run helpspot --no-verify-ssl "$@"
