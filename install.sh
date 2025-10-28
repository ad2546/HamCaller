#!/bin/bash

# HamCaller Installation Script
# Works on macOS, Linux, and Windows (WSL/Git Bash)

set -e

echo "=========================================="
echo "  HamCaller - AI Spam Call Detection"
echo "=========================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*)    PLATFORM=Windows;;
    MINGW*)     PLATFORM=Windows;;
    MSYS*)      PLATFORM=Windows;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "Detected platform: $PLATFORM"
echo ""

# Step 1: Check if Ollama is installed
echo "Step 1/5: Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is already installed"
else
    echo "✗ Ollama not found. Installing..."

    if [ "$PLATFORM" = "Mac" ] || [ "$PLATFORM" = "Linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "Please install Ollama manually from: https://ollama.com/download"
        echo "Then run this script again."
        exit 1
    fi
fi
echo ""

# Step 2: Check if Ollama is running
echo "Step 2/5: Starting Ollama service..."
if pgrep -x "ollama" > /dev/null; then
    echo "✓ Ollama is already running"
else
    echo "Starting Ollama in background..."
    if [ "$PLATFORM" = "Mac" ]; then
        # On macOS, Ollama runs as a service
        ollama serve > /dev/null 2>&1 &
        sleep 3
    elif [ "$PLATFORM" = "Linux" ]; then
        # On Linux, start in background
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    echo "✓ Ollama started"
fi
echo ""

# Step 3: Pull base model and create HamCaller
echo "Step 3/5: Setting up HamCaller model..."
if ollama list | grep -q "gemma3:1b"; then
    echo "✓ Base model (gemma3:1b) already exists"
else
    echo "Downloading base model (gemma3:1b)... This may take a few minutes."
    ollama pull gemma3:1b
fi

if ollama list | grep -q "hamcaller"; then
    echo "✓ HamCaller model already exists"
else
    echo "Creating HamCaller model from Modelfile..."
    ollama create hamcaller -f model/Modelfile
    echo "✓ HamCaller model created"
fi
echo ""

# Step 4: Check Python and install dependencies
echo "Step 4/5: Setting up Python environment..."

# Try to find Python 3
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | grep -oP '(?<=Python )[0-9]+')
    if [ "$PYTHON_VERSION" = "3" ]; then
        PYTHON_CMD="python"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    echo "  Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Found Python: $($PYTHON_CMD --version)"

# Install Python dependencies
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install --upgrade pip --quiet
$PYTHON_CMD -m pip install -r requirements.txt --quiet
echo "✓ Python dependencies installed"
echo ""

# Step 5: Test the installation
echo "Step 5/5: Testing installation..."
TEST_RESULT=$(ollama run hamcaller "Your warranty is expiring. Press 1." 2>&1)
if echo "$TEST_RESULT" | grep -qi "spam"; then
    echo "✓ Installation test passed!"
else
    echo "⚠ Warning: Test may not have worked as expected"
    echo "  But you can still try running the app"
fi
echo ""

# Done!
echo "=========================================="
echo "  Installation Complete! 🎉"
echo "=========================================="
echo ""
echo "To start HamCaller, run:"
echo ""
echo "  $PYTHON_CMD app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:8000"
echo ""
echo "Or test from command line:"
echo "  ollama run hamcaller \"Your text here\""
echo ""
echo "=========================================="
