@echo off
title Stopping JANUS Dashboard Server
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
taskkill /F /IM pythonw.exe >nul 2>&1
echo [OK] JANUS Dashboard Server stopped cleanly.
ping 127.0.0.1 -n 2 >nul
