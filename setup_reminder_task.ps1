# PowerShell script to set up scheduled task for reminder checks
# Run this as Administrator

$taskName = "WinterSportsReminderCheck"
$scriptPath = "$PSScriptRoot\check_reminders.bat"
$description = "Check for upcoming winter sports events and send reminders via Home Assistant"

Write-Host "`n=== Winter Sports TV Schedule - Reminder Task Setup ===`n" -ForegroundColor Cyan

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script must be run as Administrator" -ForegroundColor Red
    Write-Host "`nTo run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click on this file" -ForegroundColor Yellow
    Write-Host "2. Select 'Run with PowerShell' (as Administrator)`n" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "⚠️  Task '$taskName' already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to replace it? (Y/N)"
    
    if ($response -ne 'Y' -and $response -ne 'y') {
        Write-Host "`nAborting...`n" -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "`nRemoving existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create triggers - every 10 minutes between 6 AM and midnight
$triggers = @()

# Create a trigger that repeats every 10 minutes throughout the day
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00"
$trigger.Repetition = New-ScheduledTaskTrigger -Once -At "06:00" -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Hours 18) | Select-Object -ExpandProperty Repetition

$triggers += $trigger

# Set task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

# Create the principal (run whether user is logged on or not)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest

# Register the scheduled task
Write-Host "`nCreating scheduled task..." -ForegroundColor Green

try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Description $description `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Force | Out-Null
    
    Write-Host "`n✅ Scheduled task created successfully!`n" -ForegroundColor Green
    
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $taskName"
    Write-Host "  Schedule: Every 10 minutes from 6:00 AM to midnight"
    Write-Host "  Script: $scriptPath"
    
    Write-Host "`nThe task will:" -ForegroundColor Cyan
    Write-Host "  - Check for upcoming events every 10 minutes"
    Write-Host "  - Send reminders based on configured intervals (60 min, 15 min)"
    Write-Host "  - Respect time restrictions set in .env file"
    Write-Host "  - Track sent reminders to avoid duplicates"
    
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. Configure your .env file with Home Assistant settings"
    Write-Host "2. Test with: python manage.py test-notification"
    Write-Host "3. Check logs in reminders.log"
    
    Write-Host "`nYou can manage this task in Task Scheduler (taskschd.msc)`n" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n❌ Failed to create scheduled task: $($_.Exception.Message)`n" -ForegroundColor Red
    exit 1
}

Read-Host "Press Enter to exit"
