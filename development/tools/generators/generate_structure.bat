@echo off
REM Simple batch file to generate folder structure
REM This allows easy execution without typing the full PowerShell command

echo Generating JS-Codebase Folder Structure...
echo.

REM Change to the root directory (one level up from scripts)
cd /d "%~dp0.."

REM Execute the PowerShell script
powershell -ExecutionPolicy Bypass -File "scripts\generate_folder_structure_fixed.ps1"

echo.
echo Done! Check folder_structure.md for the results.
pause
