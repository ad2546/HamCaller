@echo off
REM HamCaller Run Script for Windows

echo ==========================================
echo   Starting HamCaller...
echo ==========================================
echo.

REM Check if Python exists
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Python not found. Please run install.bat first
    pause
    exit /b 1
)

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting Ollama service...
    start /B ollama serve
    timeout /t 2 /nobreak >nul
)

REM Check if model exists
ollama list | find "hamcaller" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] HamCaller model not found. Please run install.bat first
    pause
    exit /b 1
)

echo [OK] Starting HamCaller web application...
echo.
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the app
python app.py
