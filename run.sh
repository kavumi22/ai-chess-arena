#!/bin/bash

echo "Starting AI Chess Arena..."

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Launching AI Chess Arena..."
python main.py
