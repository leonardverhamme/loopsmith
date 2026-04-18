@echo off
setlocal
set SCRIPT_DIR=%~dp0
if "%CODEX_HOME%"=="" set CODEX_HOME=%SCRIPT_DIR:~0,-1%
python "%SCRIPT_DIR%agentctl\agentctl.py" %*
