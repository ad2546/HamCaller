@echo off
REM HamCaller Installation Script for Windows

echo ==========================================
echo   HamCaller - AI Spam Call Detection
echo ==========================================
echo.

REM Step 1: Check if Ollama is installed
echo Step 1/5: Checking for Ollama...
where ollama >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Ollama is already installed
) else (
    echo [!] Ollama not found.
    echo Please download and install from: https://ollama.com/download
    echo Then run this script again.
    pause
    exit /b 1
)
echo.

REM Step 2: Start Ollama (it runs as a service on Windows)
echo Step 2/5: Checking Ollama service...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama is running
) else (
    echo Starting Ollama...
    start /B ollama serve
    timeout /t 3 /nobreak >nul
)
echo.

REM Step 3: Pull base model and create HamCaller
echo Step 3/5: Setting up HamCaller model...
ollama list | find "gemma3:1b" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Base model already exists
) else (
    echo Downloading base model... This may take a few minutes.
    ollama pull gemma3:1b
)

ollama list | find "hamcaller" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] HamCaller model already exists
) else (
    echo Creating HamCaller model...
    ollama create hamcaller -f model\Modelfile
    echo [OK] HamCaller model created
)
echo.

REM Step 4: Check Python and install dependencies
echo Step 4/5: Setting up Python environment...
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python --version
    echo [OK] Found Python
) else (
    echo [!] Python not found.
    echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
echo [OK] Python dependencies installed
echo.

REM Step 5: Test installation
echo Step 5/5: Testing installation...
ollama run hamcaller "Your warranty is expiring. Press 1." | find /I "spam" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Installation test passed!
) else (
    echo [!] Test may not have worked, but you can still try the app
)
echo.

REM Done
echo ==========================================
echo   Installation Complete!
echo ==========================================
echo.
echo To start HamCaller, run:
echo.
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:8000
echo.
echo Or test from command line:
echo   ollama run hamcaller "Your text here"
echo.
echo ==========================================
pause
