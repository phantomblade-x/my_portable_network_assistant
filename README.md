# my_portable_network_assistant
A portable, voice-activated network assistant that runs on a Raspberry Pi 4B. Talk to your Cisco switches through the console port.

# Cisco Voice Assistant

A portable, voice-activated network assistant that runs on a Raspberry Pi 4B. Talk to your Cisco switches through the console port.

> "What VLAN is port 16 on?"
> "Shut down port 24" (requires spoken password confirmation)

## Features

- 🎤 Voice-activated queries using local Whisper STT
- 🔊 Spoken responses via Piper TTS
- 🧠 Local LLM for natural language understanding (no cloud required)
- 🔒 Exec mode with spoken password confirmation for dangerous commands
- 🔌 Serial console connection to Cisco IOS devices

## Hardware Requirements

- Raspberry Pi 4B (8GB recommended)
- USB-to-Serial adapter (FTDI/CH340) + console cable
- USB microphone or I2S mic (INMP441)
- Speaker or I2S DAC (MAX98357A)
- (Optional) LiPo battery + UPS hat for portability

## Software Requirements

- Raspberry Pi OS (64-bit) or Ubuntu Server
- Python 3.10+
- ~4GB free disk space for models

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/cisco-voice-assistant.git
cd cisco-voice-assistant

# Run setup script
chmod +x setup.sh
./setup.sh

# Copy and edit config
cp config.yaml.example config.yaml
nano config.yaml

# Download models
./download_models.sh

# Run it
python src/main.py


#Commercial Inquiries
#Interested in My Personal Network Assistant for your business? MassiveProfits2u@proton.me
