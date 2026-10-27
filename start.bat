@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo  ================================================
echo   TITANIC SURVIVAL PREDICTOR - WEB LAUNCHER
echo  ================================================
echo.

REM ── Check if NGROK_AUTHTOKEN is already set ──────────────────────────────
if not "%NGROK_AUTHTOKEN%"=="" (
    echo  Auth token found in environment. Starting with public URL...
    echo.
    python app.py
    goto :end
)

REM ── Ask user for token ────────────────────────────────────────────────────
echo  To get a FREE public internet URL, you need an ngrok token.
echo.
echo  STEP 1: Sign up (free) at  https://ngrok.com
echo  STEP 2: Copy your token from:
echo          https://dashboard.ngrok.com/get-started/your-authtoken
echo.
set /p TOKEN="  Paste your ngrok token here (or press ENTER to run locally): "

if "%TOKEN%"=="" (
    echo.
    echo  Starting in LOCAL mode (http://127.0.0.1:5000) ...
    echo  Open your browser and visit: http://127.0.0.1:5000
    echo.
    python app.py
) else (
    echo.
    echo  Starting with public URL...
    echo.
    python app.py --token %TOKEN%
)

:end
pause
