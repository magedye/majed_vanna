@echo off
setlocal

rem Production startup script (native, no Docker)
rem Assumes venv exists at %~dp0..\\venv

pushd %~dp0..

if exist "venv\\Scripts\\activate.bat" (
    call "venv\\Scripts\\activate.bat"
) else (
    echo [WARN] venv not found. Using system python.
)

set HOST=0.0.0.0
set PORT=8000

echo [INFO] Starting uvicorn on %HOST%:%PORT% ...
python -m uvicorn app.main:app --host %HOST% --port %PORT% --workers 2 --log-level info

popd
endlocal
