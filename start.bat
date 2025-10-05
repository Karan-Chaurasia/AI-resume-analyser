@echo off
echo Starting Resume Analyzer...

cd backend
start "Backend" cmd /k "pip install -r requirements.txt --upgrade && python main.py"

cd ..\frontend
start "Frontend" cmd /k "npm start"

echo.
echo Application starting...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
pause