@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -c "import PySide6" >nul 2>&1
  if not errorlevel 1 (
    start "COMSOL + Origin Auto Plot" ".venv\Scripts\pythonw.exe" "%~dp0gui_main.py" %*
    exit /b 0
  )
)
rem Compatibility with the original local project's installed GUI environment.
if exist "..\COMSOL-to-CSV-and-Origin-parser\.venv\Scripts\pythonw.exe" (
  start "COMSOL + Origin Auto Plot" "..\COMSOL-to-CSV-and-Origin-parser\.venv\Scripts\pythonw.exe" "%~dp0gui_main.py" %*
  exit /b 0
)
echo Please double-click Setup-GUI.cmd first to install the Python dependencies.
pause
exit /b 1
