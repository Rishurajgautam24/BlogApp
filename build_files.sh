#!/bin/bash

echo "BUILD STARTED"

# Install dependencies (assuming no virtual environment)
python3.9 -m pip install django -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

# Handle potential errors (optional)
if [ $? -ne 0 ]; then
  echo "An error occurred during the build process. Please check the logs for details."
  exit 1
fi

echo "BUILD ENDED"
