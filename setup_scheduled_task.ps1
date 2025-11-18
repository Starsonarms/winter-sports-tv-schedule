# PowerShell script to create a scheduled task for automatic updates
# Run this script as Administrator

$taskName = "WinterSportsTVScheduleUpdate"
$scriptPath = "C:\Users\cpa\projects\winter-sports-tv-schedule\update_events.bat"
$description = "Daily update of winter sports TV schedule from FIS and IBU"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create the trigger (daily at 2 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 2am

# Create principal (run whether user is logged in or not)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description $description

Write-Host ""
Write-Host "✅ Scheduled task created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Task details:" -ForegroundColor Cyan
Write-Host "  Name: $taskName"
Write-Host "  Schedule: Daily at 2:00 AM"
Write-Host "  Script: $scriptPath"
Write-Host ""
Write-Host "You can manage this task in Task Scheduler (taskschd.msc)" -ForegroundColor Yellow
Write-Host ""

# Test the task
$testNow = Read-Host "Do you want to test the task now? (y/n)"
if ($testNow -eq 'y' -or $testNow -eq 'Y') {
    Write-Host "Running task now..."
    Start-ScheduledTask -TaskName $taskName
    Start-Sleep -Seconds 5
    
    # Check log
    if (Test-Path "C:\Users\cpa\projects\winter-sports-tv-schedule\update_log.txt") {
        Write-Host ""
        Write-Host "Last few lines from update log:" -ForegroundColor Cyan
        Get-Content "C:\Users\cpa\projects\winter-sports-tv-schedule\update_log.txt" -Tail 10
    }
}
