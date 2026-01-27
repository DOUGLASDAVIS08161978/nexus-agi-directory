#!/bin/bash

echo "================================================================================"
echo "Ollama Installation Script for Autonomous Web3 Builder"
echo "================================================================================"
echo ""

# Install Ollama
echo "Step 1: Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Check if installation was successful
if command -v ollama &> /dev/null; then
    echo "✅ Ollama installed successfully!"
    echo ""
    echo "Step 2: Starting Ollama service..."

    # Start Ollama in background
    nohup ollama serve > ollama.log 2>&1 &
    OLLAMA_PID=$!
    echo "Ollama started with PID: $OLLAMA_PID"

    # Wait for Ollama to be ready
    echo "Waiting for Ollama to be ready..."
    sleep 5

    # Pull the model
    echo ""
    echo "Step 3: Downloading AI model (llama3.2)..."
    echo "This may take a few minutes depending on your internet connection..."
    ollama pull llama3.2

    if [ $? -eq 0 ]; then
        echo ""
        echo "================================================================================"
        echo "✅ Installation Complete!"
        echo "================================================================================"
        echo ""
        echo "Ollama is now running and ready to use."
        echo "The llama3.2 model has been downloaded."
        echo ""
        echo "To use the Autonomous Web3 Builder:"
        echo "  python3 autonomous_web3_builder.py"
        echo ""
        echo "To check Ollama status:"
        echo "  curl http://localhost:11434/api/version"
        echo ""
        echo "To view Ollama logs:"
        echo "  tail -f ollama.log"
        echo ""
    else
        echo "❌ Failed to download model. Please check your internet connection."
        exit 1
    fi
else
    echo "❌ Ollama installation failed. Please install manually:"
    echo "   curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi
