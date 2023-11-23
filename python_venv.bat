@echo off
if exist venv (
  venv\Scripts\activate.bat
) else (
  python -m venv venv
  venv\Scripts\activate.bat
)
echo on