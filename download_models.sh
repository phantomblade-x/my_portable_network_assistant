#!/bin/bash
set -e

echo "=== Downloading Models ==="

mkdir -p models
cd models

# Whisper base.en (good balance of speed/accuracy for commands)
if [ ! -f "whisper-base.en.bin" ]; then
    echo "Downloading Whisper base.en..."
    wget -q --show-progress https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin -O whisper-base.en.bin
fi

# Llama 3.2 1B Q4 (fits easily in 8GB, fast inference)
if [ ! -f "llama-3.2-1b-q4_k_m.gguf" ]; then
    echo "Downloading Llama 3.2 1B Q4..."
    wget -q --show-progress https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf -O llama-3.2-1b-q4_k_m.gguf
fi

# Piper TTS voice
if [ ! -f "en_US-lessac-medium.onnx" ]; then
    echo "Downloading Piper voice..."
    wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
    wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
fi

echo ""
echo "=== Models downloaded ==="
ls -lh