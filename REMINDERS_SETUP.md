# Event Reminders Setup

Get notifications on your phone before winter sports events start!

## Features

- 🔔 **Smart Reminders**: Get notified 60 minutes and 15 minutes before events
- 📱 **Home Assistant Integration**: Works with your existing Home Assistant setup
- ⏰ **Time Restrictions**: Only sends notifications during configured hours
- 🔄 **Automatic Tracking**: MongoDB tracks sent reminders to avoid duplicates
- 🎯 **Event Filtering**: Only get reminders for selected sports based on your filters

## Prerequisites

1. **Home Assistant** installed and running
2. **Home Assistant Mobile App** on your phone (iOS or Android)
3. **Python 3.7+** installed
4. **MongoDB** (optional, but recommended)

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Configuration

```bash
python manage.py init-config
```

This creates a `.env` file. Edit it with your settings:

```bash
# .env
HOME_ASSISTANT_URL=http://homeassistant.local:8123
HOME_ASSISTANT_TOKEN=your_token_here
HOME_ASSISTANT_SERVICE=notify.mobile_app_your_phone
```

### 3. Get Home Assistant Token

1. Go to Home Assistant → Profile → Security
2. Scroll down to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Give it a name like "Winter Sports Reminders"
5. Copy the token to your `.env` file

### 4. Find Your Notification Service

In Home Assistant, go to Developer Tools → Services and search for "notify". Common services:

- `notify.mobile_app_your_iphone` (iPhone)
- `notify.mobile_app_your_android` (Android)
- `notify.persistent_notification` (HA dashboard only)

Update `HOME_ASSISTANT_SERVICE` in `.env` with your service name.

### 5. Test Everything

```bash
# Test Home Assistant connection
python manage.py test-ha

# Send a test notification
python manage.py test-notification
```

If successful, you should receive a test notification on your phone!

### 6. Set Up Automatic Checking

**Right-click** `setup_reminder_task.ps1` → **Run with PowerShell** (as Administrator)

This creates a Windows scheduled task that checks for reminders every 10 minutes.

## Configuration Options

Edit `.env` to customize:

```bash
# Reminder intervals (minutes before event)
REMINDER_INTERVALS=60,15

# Enable/disable reminders
REMINDERS_ENABLED=true

# Notification time restrictions
WEEKDAY_START_HOUR=8   # 8 AM
WEEKDAY_END_HOUR=23    # 11 PM
WEEKEND_START_HOUR=9   # 9 AM
WEEKEND_END_HOUR=23    # 11 PM
```

## MongoDB Setup (Recommended)

MongoDB prevents duplicate reminders. Without it, you might get the same reminder multiple times.

### Dedicated MongoDB Atlas Cluster

This project has its own MongoDB Atlas cluster for tracking reminders.

**Your `.env` file should have:**
```bash
MONGODB_URI=mongodb+srv://palmchristian_db_admin:jIk9RizuxOLxtWDW@wintersportsreminders.y80xoa0.mongodb.net/?appName=wintersportsreminders
MONGODB_DATABASE=winter_sports
```

**These settings are already in `.env.example`** - just copy them to `.env`.

### Initialize Database

After configuring, initialize the database collections:

```bash
python manage.py init-db
```

This creates:
- `sent_reminders` collection
- Indexes for fast lookups and duplicate prevention

### Test MongoDB

```bash
python manage.py test-mongodb
```

## Management Commands

```bash
# Configuration
python manage.py init-config          # Create .env file
python manage.py show-config          # Show current settings

# Database
python manage.py init-db              # Initialize MongoDB collections
python manage.py test-mongodb         # Test MongoDB connection

# Testing
python manage.py test-ha              # Test Home Assistant
python manage.py test-notification    # Send test notification

# Manual check
python manage.py check-reminders      # Check for reminders now
```

## How It Works

1. **Every 10 minutes**, the scheduled task runs `check_reminders.py`
2. It reads events from `script.js`
3. For each upcoming event:
   - Checks if it's within 24 hours
   - Checks if a reminder should be sent (60 or 15 minutes before)
   - Checks if the reminder was already sent (MongoDB)
   - Respects time restrictions (no notifications at night)
4. Sends notifications via Home Assistant
5. Tracks sent reminders to avoid duplicates

## Troubleshooting

### "Cannot connect to Home Assistant"

- Check that Home Assistant is running
- Verify the URL: `http://homeassistant.local:8123` or your IP
- Ensure the token is valid (create a new one if needed)

### "Failed to send notification"

- Check the service name in `.env` matches your actual service
- Test in Home Assistant Developer Tools → Services first

### No reminders received

- Check `reminders.log` for errors
- Verify scheduled task is running (Task Scheduler → `WinterSportsReminderCheck`)
- Check time restrictions in `.env`
- Make sure events exist in `script.js` for the next 24 hours

### Duplicate reminders

- Install and configure MongoDB
- Run `python manage.py test-mongodb` to verify connection

## Logs

Check `reminders.log` for detailed information:

```bash
# View recent logs (PowerShell)
Get-Content reminders.log -Tail 50

# View recent logs (Command Prompt)
type reminders.log
```

## Raspberry Pi Deployment

When you deploy to Raspberry Pi:

1. Copy all Python files and `.env`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Set up cron job instead of Windows Task Scheduler:

```bash
# Edit crontab
crontab -e

# Add this line (check every 10 minutes)
*/10 * * * * cd /home/pi/winter-sports-tv-schedule && /usr/bin/python3 check_reminders.py >> /home/pi/winter-sports-tv-schedule/reminders.log 2>&1
```

## Uninstalling

To remove the scheduled task:

1. Open Task Scheduler (`taskschd.msc`)
2. Find "WinterSportsReminderCheck"
3. Right-click → Delete

Or run PowerShell as Administrator:

```powershell
Unregister-ScheduledTask -TaskName "WinterSportsReminderCheck" -Confirm:$false
```

## Support

For issues or questions, check:
- `reminders.log` for detailed error messages
- Home Assistant logs for notification issues
- Windows Event Viewer for scheduled task issues
