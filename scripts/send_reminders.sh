#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Go to project root directory
cd "$SCRIPT_DIR/.."

# Activate virtual environment (adjust path if needed)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run Django management command to send reminders
python manage.py send_reminders

# Deactivate virtual environment
deactivate 