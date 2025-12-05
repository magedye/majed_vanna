@echo off
setlocal EnableExtensions EnableDelayedExpansion
REM Phase 4.E: Strict Port Enforcement & Liberation

IF "%APP_PORT%"=="" SET APP_PORT=7777

echo >>> Checking Port %APP_PORT% availability...

FOR /F "tokens=5" %%a IN ('netstat -aon ^| findstr ":%APP_PORT%"') DO (
    IF NOT "%%a"=="" (
        echo [WARNING] Port %APP_PORT% is busy by PID %%a. Killing it...
        taskkill /F /PID %%a >nul 2>&1
        timeout /t 2 >nul
    )
)

echo >>> Launching Server on Strict Port %APP_PORT%...
uvicorn app.main:app --host 0.0.0.0 --port %APP_PORT%

endlocal
