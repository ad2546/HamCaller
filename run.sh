#!/bin/bash

# HamCaller Run Script
# Simple script to start the application

set -e

echo "=========================================="
echo "  Starting HamCaller..."
echo "=========================================="
echo ""

# Find Python
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "✗ Python not found. Please run ./install.sh first"
    exit 1
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi

# Check if model exists
if ! ollama list | grep -q "hamcaller"; then
    echo "✗ HamCaller model not found. Please run ./install.sh first"
    exit 1
fi

echo "✓ Starting HamCaller web application..."
echo ""
echo "Open your browser to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
$PYTHON_CMD app.py
