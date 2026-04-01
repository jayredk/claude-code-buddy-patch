@echo off
setlocal
chcp 65001 >nul

set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 -X utf8 "%SCRIPT_DIR%patch-buddy.py"
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    goto :run_claude
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python -X utf8 "%SCRIPT_DIR%patch-buddy.py"
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    goto :run_claude
)

echo Python 3 was not found on PATH.
echo Install Python, then run this file again.
exit /b 1

:run_claude
where claude >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Claude was not found on PATH.
    echo Install the npm-based Claude Code CLI, then run this file again.
    exit /b 1
)

call claude %*
