@echo off
setlocal EnableExtensions EnableDelayedExpansion
pushd "%~dp0.."

REM === Force UTF-8 console/encoding to avoid charmap errors ===
chcp 65001 >nul
set PYTHONUTF8=1

REM === Configure Port (defaults to 7777) ===
if "%APP_PORT%"=="" set "APP_PORT=7777"
echo Launching Server on Strict Port %APP_PORT%...

REM === Find a PID using the port (first match) ===
set "PID="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R /C:":%APP_PORT% " /C:":%APP_PORT%$"') do (
    echo Port %APP_PORT% is in use by PID %%a. Terminating...
    taskkill /PID %%a /F >nul 2>&1
)

REM === Start Vanna Agent ===
echo Starting Vanna agent...
python app/main.py

popd
endlocal
