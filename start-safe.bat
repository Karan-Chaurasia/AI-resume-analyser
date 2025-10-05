@echo off
echo Starting Resume Analyzer (Safe Mode)...

cd backend
start "Backend" cmd /k "python main.py"

cd ..\frontend
start "Frontend" cmd /k "npm start"

echo.
echo Application starting in safe mode...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
pause