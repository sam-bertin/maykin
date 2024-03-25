#!/bin/bash

# Path of the virtualenv
VIRTUALENV_PATH="/path/to/your/virtualenv"

# Start the virtualenv
source "${VIRTUALENV_PATH}/bin/activate"

# Path of the project
PROJECT_DIR="/path/to/your/project"

# Start the scheduler
cd "${PROJECT_DIR}" && python manage.py start_scheduler
