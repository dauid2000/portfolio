@echo off
cd /d "%~dp0"
title David Musumali - Personal API

if not exist .venv (
    echo First run detected - creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo Starting API on http://127.0.0.1:8000  (docs: http://127.0.0.1:8000/docs)
echo Press CTRL+C to stop.
echo.
uvicorn main:app --reload
