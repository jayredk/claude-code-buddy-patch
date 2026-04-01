@echo off
setlocal
chcp 65001 >nul

set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 -X utf8 "%SCRIPT_DIR%patch-buddy.py"
    goto :end
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python -X utf8 "%SCRIPT_DIR%patch-buddy.py"
    goto :end
)

echo Python 3 was not found on PATH.
echo Install Python, then run this file again.
exit /b 1

:end
echo.
echo === Done! Restart Claude Code ===
pause
