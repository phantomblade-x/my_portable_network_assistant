#!/bin/bash
set -e

echo "=== Cisco Voice Assistant Setup ==="

# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    libsndfile1 \
    espeak-ng \
    ffmpeg \
    git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p models logs

# Add user to dialout group for serial access
sudo usermod -a -G dialout $USER

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "1. Log out and back in (for serial permissions)"
echo "2. Run: ./download_models.sh"
echo "3. Copy config.yaml.example to config.yaml and edit"
echo "4. Run: source venv/bin/activate && python src/main.py"