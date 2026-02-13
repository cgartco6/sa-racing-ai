@echo off
REM Install Python 3.11
REM Install PostgreSQL 15
REM Create virtual environment
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Setup complete
