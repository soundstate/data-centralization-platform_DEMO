@echo off
echo Starting LLM Backend Server...
echo.
echo Server will run on http://localhost:3001
echo.
echo Endpoints available:
echo - Health Check: http://localhost:3001/health
echo - Chat API: http://localhost:3001/api/chat
echo - Models: http://localhost:3001/api/models
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
npm run dev
