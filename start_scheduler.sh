#!/bin/sh
echo "Starting scheduler..."
# Path to the virtualenv
VIRTUALENV_PATH=/app/venv

# Activate the virtualenv
. "$VIRTUALENV_PATH/bin/activate"

# Path to the project
PROJECT_DIR=/app

# Start the scheduler
cd "$PROJECT_DIR"
python manage.py start_scheduler
