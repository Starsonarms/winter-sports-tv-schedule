@echo off
REM Batch file to check for upcoming event reminders

cd /d "%~dp0"

echo ================================================
echo Winter Sports TV Schedule - Reminder Check
echo ================================================
echo %date% %time%
echo.

python check_reminders.py

echo.
echo ================================================
echo Reminder check completed at %time%
echo ================================================
