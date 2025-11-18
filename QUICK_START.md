# Quick Start Guide

Get winter sports reminders on your phone in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create Configuration

```bash
python manage.py init-config
```

This creates `.env` file with MongoDB settings already configured.

## Step 3: Edit .env File

Open `.env` and add your Home Assistant settings:

```bash
HOME_ASSISTANT_URL=http://homeassistant.local:8123
HOME_ASSISTANT_TOKEN=your_long_lived_token_here
HOME_ASSISTANT_SERVICE=notify.mobile_app_your_phone
```

**Note**: MongoDB settings are already configured in `.env.example`, no changes needed!

## Step 4: Initialize Database and Import Events

```bash
python manage.py init-db
python manage.py import-events
```

This creates the MongoDB collections and imports your events from `script.js`.

Expected output:
```
✅ Successfully initialized MongoDB database

Database: winter_sports
Collections created:
  - sent_reminders (tracks reminder notifications)
  - events (stores TV schedule events)

✅ Imported 19 events
Total events in database: 19
Sports: cross-country, ice-hockey, figure-skating
```

**Note**: Events are automatically synced to MongoDB **only when `script.js` changes**. The reminder check (every 10 min) detects changes and syncs efficiently!

## Step 5: Test Everything

```bash
# Test Home Assistant connection
python manage.py test-ha

# Test MongoDB
python manage.py test-mongodb

# Send a test reminder to your phone
python manage.py test-notification
```

## Step 6: Set Up Automatic Reminders

**Right-click** `setup_reminder_task.ps1` → **Run with PowerShell** (as Administrator)

This creates a Windows scheduled task that checks for reminders every 10 minutes.

## Done! 🎉

You'll now receive notifications:
- **60 minutes** before events start
- **15 minutes** before events start

## MongoDB Details

Your reminder data is stored in:
- **Cluster**: `wintersportsreminders.y80xoa0.mongodb.net`
- **Database**: `winter_sports`
- **Collection**: `sent_reminders`

View your data at [cloud.mongodb.com](https://cloud.mongodb.com)

## Web Interface

Manage settings via web browser:
```bash
python manage.py start-web
```

Then open http://localhost:5001 in your browser.

**Features:**
- ⚙️ Edit reminder intervals
- 🕒 Configure notification times
- 🧪 Test Home Assistant and MongoDB connections
- 📱 Send test notifications

## Manual Checks

Check for reminders manually:
```bash
python manage.py check-reminders
```

## Troubleshooting

### "Cannot connect to Home Assistant"
1. Check URL in `.env` (e.g., `http://homeassistant.local:8123`)
2. Verify token is valid
3. Make sure Home Assistant is running

### "MongoDB connection failed"
The MongoDB URI is already configured in `.env.example`. If you see this error:
1. Check that you ran `python manage.py init-config`
2. Verify `.env` file exists and has `MONGODB_URI` set
3. Check internet connection (MongoDB Atlas is cloud-based)

### No reminders received
1. Check `reminders.log` for errors
2. Verify scheduled task is running (Task Scheduler)
3. Make sure events exist in `script.js` for the next 24 hours

## Next Steps

- Customize reminder intervals in `.env` (`REMINDER_INTERVALS=60,15`)
- Adjust notification times (weekday/weekend hours)
- Check logs: `reminders.log`

For detailed documentation, see:
- `REMINDERS_SETUP.md` - Complete setup guide
- `MONGODB_INFO.md` - Database details
- `manage.py help` - All available commands
