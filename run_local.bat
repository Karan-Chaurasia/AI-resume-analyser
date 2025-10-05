@echo off
echo Starting Resume Analyzer Application...
echo.

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm

echo.
echo Starting backend server...
start "Backend Server" cmd /k "python main.py"

echo.
echo Installing frontend dependencies...
cd ..\frontend
call npm install

echo.
echo Starting frontend development server...
start "Frontend Server" cmd /k "npm start"

echo.
echo Application is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause