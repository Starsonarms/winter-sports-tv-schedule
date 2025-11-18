@echo off
REM Batch file to update winter sports TV schedule automatically

cd /d "C:\Users\cpa\projects\winter-sports-tv-schedule"

echo Updating winter sports events...
echo %DATE% %TIME% >> update_log.txt
echo ================================ >> update_log.txt

REM Run the automatic Python script
python update_events_auto.py >> update_log.txt 2>&1

REM Check if update was successful
if %ERRORLEVEL% EQU 0 (
    echo Update completed successfully >> update_log.txt
) else (
    echo Update failed with error code %ERRORLEVEL% >> update_log.txt
)

echo. >> update_log.txt
