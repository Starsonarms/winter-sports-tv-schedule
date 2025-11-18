"""
Check for upcoming events and send reminders via Home Assistant
"""

import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from home_assistant import HomeAssistantNotifier
from mongodb_client import MongoDBClient
from config import get_config
from events_manager import EventsManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reminders.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def should_sync_events() -> bool:
    """Check if script.js has been modified since last sync"""
    script_path = Path(__file__).parent / 'script.js'
    sync_marker_path = Path(__file__).parent / '.last_event_sync'
    
    if not script_path.exists():
        return False
    
    script_mtime = script_path.stat().st_mtime
    
    # If marker file doesn't exist, we need to sync
    if not sync_marker_path.exists():
        return True
    
    try:
        with open(sync_marker_path, 'r') as f:
            last_sync_time = float(f.read().strip())
        
        # If script.js is newer than last sync, sync again
        return script_mtime > last_sync_time
    except:
        return True


def sync_events_to_mongodb() -> bool:
    """Sync events from script.js to MongoDB (only if changed)"""
    try:
        # Check if sync is needed
        if not should_sync_events():
            logger.debug("script.js hasn't changed, skipping sync")
            return True
        
        events_manager = EventsManager()
        
        if events_manager.events_collection is None:
            logger.warning("MongoDB not connected - skipping event sync")
            return False
        
        # Clean up past events first
        cleaned = events_manager.cleanup_past_events()
        if cleaned > 0:
            logger.info(f"Removed {cleaned} past events")
        
        # Import events from script.js
        imported = events_manager.import_events_from_js()
        events_manager.close()
        
        if imported > 0:
            logger.info(f"Synced {imported} events to MongoDB")
            
            # Update sync marker
            script_path = Path(__file__).parent / 'script.js'
            sync_marker_path = Path(__file__).parent / '.last_event_sync'
            
            with open(sync_marker_path, 'w') as f:
                f.write(str(script_path.stat().st_mtime))
            
            return True
        else:
            logger.warning("No events synced to MongoDB")
            return False
            
    except Exception as e:
        logger.error(f"Error syncing events to MongoDB: {e}")
        return False


def get_events_from_mongodb() -> List[Dict]:
    """Get all events from MongoDB"""
    try:
        events_manager = EventsManager()
        
        if not events_manager.events_collection:
            logger.warning("MongoDB not connected")
            return []
        
        events = events_manager.get_all_events()
        events_manager.close()
        
        logger.info(f"Loaded {len(events)} events from MongoDB")
        return events
        
    except Exception as e:
        logger.error(f"Error getting events from MongoDB: {e}")
        return []


def parse_event_datetime(event: Dict) -> datetime:
    """Parse event date and time into datetime object"""
    try:
        date_str = event.get('date', '')
        time_str = event.get('time', '')
        
        if not date_str or not time_str:
            return None
        
        # Skip TBA times
        if time_str.upper() == 'TBA':
            return None
        
        # Parse datetime
        datetime_str = f"{date_str} {time_str}"
        event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        return event_datetime
        
    except Exception as e:
        logger.debug(f"Error parsing datetime for event {event.get('id')}: {e}")
        return None


def check_and_send_reminders():
    """Check for upcoming events and send reminders"""
    logger.info("=== Starting reminder check ===")
    
    # Load configuration
    config = get_config()
    
    if not config.reminders_enabled:
        logger.info("Reminders are disabled in configuration")
        return
    
    # Sync events from script.js to MongoDB
    logger.info("Syncing events to MongoDB...")
    sync_events_to_mongodb()
    
    # Initialize services
    notifier = HomeAssistantNotifier()
    db_client = MongoDBClient()
    
    # Test Home Assistant connection
    if not notifier.test_connection():
        logger.error("Cannot connect to Home Assistant. Aborting reminder check.")
        return
    
    # Get events from MongoDB
    events = get_events_from_mongodb()
    
    if not events:
        logger.warning("No events found to check")
        return
    
    now = datetime.now()
    reminders_sent = 0
    reminders_skipped = 0
    
    # Check each event
    for event in events:
        event_datetime = parse_event_datetime(event)
        
        if not event_datetime:
            continue
        
        # Skip past events
        if event_datetime < now:
            continue
        
        # Check if event is in the next 24 hours
        if event_datetime > now + timedelta(hours=24):
            continue
        
        # Calculate time until event
        time_until_event = event_datetime - now
        minutes_until_event = int(time_until_event.total_seconds() / 60)
        
        # Check each reminder interval
        for reminder_minutes in config.reminder_intervals:
            # Check if we should send this reminder
            # Send if we're within a 10-minute window of the reminder time
            window = 10  # minutes
            
            if abs(minutes_until_event - reminder_minutes) <= window:
                event_id = str(event.get('id', 'unknown'))
                
                # Check if reminder already sent
                if db_client.is_connected() and db_client.has_reminder_been_sent(event_id, reminder_minutes):
                    logger.debug(f"Reminder already sent for event {event_id} ({reminder_minutes} min)")
                    reminders_skipped += 1
                    continue
                
                # Send reminder
                logger.info(f"Sending reminder for: {event.get('title')} (in {minutes_until_event} min)")
                
                if notifier.send_reminder(event, reminder_minutes):
                    # Mark as sent in database
                    if db_client.is_connected():
                        db_client.mark_reminder_sent(
                            event_id,
                            event.get('title', 'Unknown'),
                            reminder_minutes,
                            event_datetime
                        )
                    reminders_sent += 1
                else:
                    logger.error(f"Failed to send reminder for: {event.get('title')}")
    
    # Cleanup old reminders
    if db_client.is_connected():
        db_client.cleanup_old_reminders(days=7)
    
    logger.info(f"=== Reminder check complete: {reminders_sent} sent, {reminders_skipped} skipped ===")
    
    # Close connections
    db_client.close()


if __name__ == '__main__':
    try:
        check_and_send_reminders()
    except Exception as e:
        logger.error(f"Unexpected error in reminder check: {e}", exc_info=True)
