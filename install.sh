#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     AI-IDS Linux Installer              ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found! Installing..."
    sudo apt-get install python3 python3-pip -y
fi

echo "Running setup..."
python3 setup.py

echo ""
echo "✅ Done! Starting AI-IDS now..."
python3 start_ids.py