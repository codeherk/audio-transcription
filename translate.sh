#!/bin/bash
# filepath: /Users/codeherk/dev/translate/run_script.sh

# Name of the virtual environment directory
VENV_DIR="venv"

# Path to the Python script
PYTHON_SCRIPT="main.py"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Please create it using 'make create-venv' and install dependencies using 'make install'."
    exit 1
fi

# Check if an audio file argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: ./run_script.sh <audio_file_path>"
    exit 1
fi

AUDIO_FILE=$1

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Run the Python script with the provided audio file
python "$PYTHON_SCRIPT" "$AUDIO_FILE"

# Deactivate the virtual environment
deactivate