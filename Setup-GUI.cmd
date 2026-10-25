@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 py -3.12 -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
  echo Please install 64-bit Python 3.11 or 3.12, then run this file again.
  pause
  exit /b 1
)
git submodule update --init --recursive
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip install -r requirements-gui.txt
if errorlevel 1 goto failed
echo Setup completed. Double-click Start-GUI.cmd to start.
pause
exit /b 0
:failed
echo Setup failed. Check the error above and retry.
pause
exit /b 1
