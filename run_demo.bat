@echo off
setlocal
cd /d %~dp0

where docker >nul 2>nul
if errorlevel 1 (
  echo Docker Desktop is required.
  pause
  exit /b 1
)

if not exist .env copy .env.example .env >nul
if "%APP_PORT%"=="" set APP_PORT=8080

echo Starting MedNova demo...
docker compose up --build -d

echo.
echo MedNova: http://localhost:%APP_PORT%
echo See DEMO_GUIDE.md for demo accounts and presentation flow.
echo To stop: docker compose down
pause
