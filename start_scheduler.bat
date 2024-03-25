@echo off

:: Path to the virtualenv
set VIRTUALENV_PATH=C:\Users\samue\Documents\Git\GitHub\maykin\venv

:: Activate the virtualenv
call "%VIRTUALENV_PATH%\Scripts\activate.bat"

:: Path to the project
set PROJECT_DIR=C:\Users\samue\Documents\Git\GitHub\maykin

:: Start the scheduler
cd /d "%PROJECT_DIR%"
python manage.py start_scheduler
