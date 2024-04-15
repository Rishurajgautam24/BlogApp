#!/bin/bash

echo "BUILD STARTED"

# Install dependencies within a virtual environment (recommended)
# Modify the following lines to match your virtual environment creation command
source venv/bin/activate  # Assuming your virtual environment is named 'venv'

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Deactivate virtual environment (optional, but recommended for clean separation)
deactivate

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

# Handle potential errors (optional)
if [ $? -ne 0 ]; then
  echo "An error occurred during the build process. Please check the logs for details."
  exit 1
fi

echo "BUILD ENDED"
