# Automation Setup Instructions

This guide explains how to set up automatic nightly updates for your winter sports TV schedule.

## Quick Setup

### Option 1: Using PowerShell (Recommended)

1. **Right-click** on `setup_scheduled_task.ps1`
2. Select **"Run with PowerShell"** (as Administrator)
3. If prompted, allow execution by typing `Y` and pressing Enter
4. Follow the on-screen prompts

### Option 2: Manual Setup via Task Scheduler

1. Press `Win + R`, type `taskschd.msc`, and press Enter
2. Click **"Create Task"** in the right panel
3. **General Tab:**
   - Name: `WinterSportsTVScheduleUpdate`
   - Description: `Daily update of winter sports TV schedule`
   - Select **"Run whether user is logged on or not"**
   - Check **"Run with highest privileges"**

4. **Triggers Tab:**
   - Click **"New..."**
   - Begin the task: **"On a schedule"**
   - Settings: **"Daily"**
   - Start: Choose time (e.g., `2:00 AM`)
   - Click **OK**

5. **Actions Tab:**
   - Click **"New..."**
   - Action: **"Start a program"**
   - Program/script: `C:\Users\cpa\projects\winter-sports-tv-schedule\update_events.bat`
   - Click **OK**

6. **Settings Tab:**
   - Check **"Allow task to be run on demand"**
   - Check **"Run task as soon as possible after a scheduled start is missed"**
   - Check **"If the task fails, restart every"**: `15 minutes`
   - Uncheck **"Stop the task if it runs longer than"** or set to `1 hour`
   - Click **OK**

7. Click **OK** to save the task

## What It Does

The scheduled task will:
- Run every night at 2:00 AM
- Fetch latest cross-country skiing events from FIS
- Fetch latest biathlon events from IBU
- Update your webpage with new data
- Log all activity to `update_log.txt`

## Files Created

- **`update_events_auto.py`** - Python script that runs automatically (no user input required)
- **`update_events.bat`** - Batch file that runs the Python script and logs output
- **`update_log.txt`** - Log file with update history (created after first run)
- **`setup_scheduled_task.ps1`** - PowerShell script to create the scheduled task

## Testing the Automation

### Test the batch file manually:
```powershell
cd C:\Users\cpa\projects\winter-sports-tv-schedule
.\update_events.bat
```

Check `update_log.txt` to see if it worked.

### Test the scheduled task:
1. Open Task Scheduler (`taskschd.msc`)
2. Find **"WinterSportsTVScheduleUpdate"** in the task list
3. Right-click and select **"Run"**
4. Check `update_log.txt` for results

## Checking the Update Log

View recent updates:
```powershell
Get-Content C:\Users\cpa\projects\winter-sports-tv-schedule\update_log.txt -Tail 20
```

## Troubleshooting

### Task doesn't run:
- Check Task Scheduler for error codes
- Ensure Python is in your PATH: `python --version`
- Check `update_log.txt` for error messages

### Events not updating:
- Check internet connection
- Verify FIS and IBU websites are accessible
- Look for error messages in `update_log.txt`

### Permission errors:
- Ensure the batch file has write permissions in the project folder
- Run Task Scheduler as Administrator when setting up

## Modifying the Schedule

To change when updates run:
1. Open Task Scheduler (`taskschd.msc`)
2. Find **"WinterSportsTVScheduleUpdate"**
3. Right-click → **Properties**
4. Go to **Triggers** tab
5. Edit the trigger and change the time
6. Click **OK** to save

## Disabling Automatic Updates

To temporarily disable:
1. Open Task Scheduler (`taskschd.msc`)
2. Find **"WinterSportsTVScheduleUpdate"**
3. Right-click → **Disable**

To permanently remove:
1. Open Task Scheduler (`taskschd.msc`)
2. Find **"WinterSportsTVScheduleUpdate"**
3. Right-click → **Delete**

## Manual Updates

You can still update manually anytime by running:
```powershell
python parse_events_combined.py
```

This will prompt you to confirm before updating.
