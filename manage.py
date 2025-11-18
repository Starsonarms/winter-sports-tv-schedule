"""
Management script for Winter Sports TV Schedule reminders
"""

import sys
import logging
from pathlib import Path
from home_assistant import HomeAssistantNotifier
from mongodb_client import MongoDBClient
from config import get_config
from check_reminders import check_and_send_reminders
from events_manager import EventsManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_ha_connection():
    """Test Home Assistant connection"""
    print("\n=== Testing Home Assistant Connection ===\n")
    
    config = get_config()
    
    if not config.home_assistant_url:
        print("❌ HOME_ASSISTANT_URL not configured in .env file")
        return False
    
    if not config.home_assistant_token:
        print("❌ HOME_ASSISTANT_TOKEN not configured in .env file")
        return False
    
    print(f"Home Assistant URL: {config.home_assistant_url}")
    print(f"Service: {config.home_assistant_service}")
    
    notifier = HomeAssistantNotifier()
    
    if notifier.test_connection():
        print("✅ Successfully connected to Home Assistant")
        
        # Get available services
        print("\n=== Available Notification Services ===\n")
        services = notifier.get_services()
        
        if services:
            print(f"Total services: {services['all_services']}")
            print(f"\nNotification services found: {len(services['notification_services'])}")
            
            for service in services['notification_services'][:10]:  # Show first 10
                domain = service.get('domain', 'unknown')
                print(f"  - {domain}")
            
            if len(services['notification_services']) > 10:
                print(f"  ... and {len(services['notification_services']) - 10} more")
        
        return True
    else:
        print("❌ Failed to connect to Home Assistant")
        print("\nTroubleshooting:")
        print("1. Check that Home Assistant is running")
        print("2. Verify the URL is correct (e.g., http://homeassistant.local:8123)")
        print("3. Ensure the access token is valid")
        return False


def test_notification():
    """Send a test notification"""
    print("\n=== Sending Test Notification ===\n")
    
    config = get_config()
    
    if not config.reminders_enabled:
        print("⚠️  Reminders are disabled in configuration")
        print("Set REMINDERS_ENABLED=true in .env file to enable")
        return False
    
    notifier = HomeAssistantNotifier()
    
    if notifier.send_test_notification():
        print("✅ Test notification sent successfully!")
        print(f"Check your {config.home_assistant_service} for the notification")
        return True
    else:
        print("❌ Failed to send test notification")
        return False


def test_mongodb():
    """Test MongoDB connection"""
    print("\n=== Testing MongoDB Connection ===\n")
    
    config = get_config()
    print(f"MongoDB Cluster: wintersportsreminders.y80xoa0.mongodb.net (MongoDB Atlas)")
    print(f"Database: {config.mongodb_database}")
    print(f"URI Configured: {'✅ Yes' if config.mongodb_uri else '❌ No'}")
    
    db_client = MongoDBClient()
    
    if db_client.is_connected():
        print("✅ Successfully connected to MongoDB")
        
        # Show recent reminders
        reminders = db_client.get_sent_reminders(limit=5)
        
        if reminders:
            print(f"\n=== Recent Reminders ({len(reminders)}) ===\n")
            for reminder in reminders:
                print(f"  - {reminder.get('event_title')} ({reminder.get('minutes_before')} min)")
                print(f"    Sent: {reminder.get('sent_at')}")
        else:
            print("\nNo reminders sent yet")
        
        db_client.close()
        return True
    else:
        print("⚠️  MongoDB connection failed")
        print("\nThis is optional - reminders will still work, but duplicates may occur")
        print("To enable MongoDB:")
        print("1. Check that MONGODB_URI is set in .env file")
        print("2. URI should be: mongodb+srv://palmchristian_db_admin:...@wintersportsreminders.y80xoa0.mongodb.net/...")
        print("3. Verify internet connection (MongoDB Atlas is cloud-based)")
        return False


def init_database():
    """Initialize MongoDB collections and indexes"""
    print("\n=== Initializing MongoDB Database ===\n")
    
    config = get_config()
    
    if not config.mongodb_uri:
        print("❌ MONGODB_URI not configured in .env file")
        return False
    
    db_client = MongoDBClient()
    
    if db_client.is_connected():
        print("✅ Successfully initialized MongoDB database")
        print(f"\nDatabase: {config.mongodb_database}")
        print(f"Collections created:")
        print(f"  - sent_reminders (tracks reminder notifications)")
        print(f"  - events (stores TV schedule events)")
        print(f"\nIndexes created:")
        print(f"  - event_id + minutes_before (unique, prevents duplicates)")
        print(f"  - event_datetime (for cleanup queries)")
        print(f"  - sent_at (for sorting recent reminders)")
        
        # Also initialize events collection
        events_manager = EventsManager()
        events_manager.close()
        
        db_client.close()
        return True
    else:
        print("❌ Failed to initialize MongoDB")
        return False


def import_events():
    """Import events from script.js into MongoDB"""
    print("\n=== Importing Events from script.js ===\n")
    
    try:
        events_manager = EventsManager()
        
        if events_manager.events_collection is None:
            print("❌ MongoDB not connected")
            return False
        
        # Get current count
        current_count = events_manager.get_event_count()
        print(f"Current events in database: {current_count}")
        
        # Import
        imported = events_manager.import_events_from_js()
        
        if imported > 0:
            new_count = events_manager.get_event_count()
            print(f"\n✅ Imported {imported} events")
            print(f"Total events in database: {new_count}")
            
            # Show sports breakdown
            sports = events_manager.get_sports_list()
            print(f"\nSports: {', '.join(sports)}")
            
            events_manager.close()
            return True
        else:
            print("\n❌ No events imported")
            events_manager.close()
            return False
            
    except Exception as e:
        print(f"\n❌ Error importing events: {e}")
        return False


def show_events():
    """Show event statistics"""
    print("\n=== Event Statistics ===\n")
    
    try:
        events_manager = EventsManager()
        
        if events_manager.events_collection is None:
            print("❌ MongoDB not connected")
            return False
        
        total = events_manager.get_event_count()
        sports = events_manager.get_sports_list()
        upcoming = events_manager.get_upcoming_events(days=7)
        
        print(f"Total events: {total}")
        print(f"Sports: {len(sports)}")
        print(f"Upcoming (next 7 days): {len(upcoming)}")
        
        if sports:
            print(f"\nAvailable sports:")
            for sport in sports:
                count = len(events_manager.get_events_by_sport(sport))
                print(f"  - {sport}: {count} events")
        
        events_manager.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def start_web_interface():
    """Start the web interface"""
    print("\n=== Starting Web Interface ===\n")
    print("Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop\n")
    
    try:
        from web_app import run_web_app
        run_web_app()
    except KeyboardInterrupt:
        print("\n\nWeb interface stopped")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")
        return False


def check_reminders_now():
    """Run reminder check now"""
    print("\n=== Checking for Reminders ===\n")
    
    try:
        check_and_send_reminders()
        print("\n✅ Reminder check complete")
        return True
    except Exception as e:
        print(f"\n❌ Error during reminder check: {e}")
        return False


def show_config():
    """Show current configuration"""
    print("\n=== Current Configuration ===\n")
    
    config = get_config()
    
    print(f"Reminders Enabled: {'✅ Yes' if config.reminders_enabled else '❌ No'}")
    print(f"Home Assistant URL: {config.home_assistant_url or '(not set)'}")
    print(f"HA Service: {config.home_assistant_service}")
    print(f"Reminder Intervals: {config.reminder_intervals} minutes")
    print(f"\nNotification Times:")
    print(f"  Weekdays: {config.weekday_start_hour}:00 - {config.weekday_end_hour}:59")
    print(f"  Weekends: {config.weekend_start_hour}:00 - {config.weekend_end_hour}:59")
    print(f"\nMongoDB Cluster: wintersportsreminders.y80xoa0.mongodb.net (MongoDB Atlas)")
    print(f"MongoDB Database: {config.mongodb_database}")
    print(f"MongoDB URI: {'✅ Configured' if config.mongodb_uri else '❌ Not configured'}")


def init_config():
    """Initialize configuration from example"""
    env_path = Path(__file__).parent / '.env'
    env_example_path = Path(__file__).parent / '.env.example'
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborting")
            return False
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    try:
        # Copy example to .env
        with open(env_example_path, 'r') as src:
            content = src.read()
        
        with open(env_path, 'w') as dst:
            dst.write(content)
        
        print(f"✅ Created {env_path}")
        print("\nNext steps:")
        print("1. Edit .env file with your Home Assistant settings")
        print("2. Run 'python manage.py test-ha' to test connection")
        print("3. Run 'python manage.py test-notification' to test notifications")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def show_help():
    """Show help message"""
    print("\n=== Winter Sports TV Schedule - Management Commands ===\n")
    print("Configuration:")
    print("  init-config           Create .env file from example")
    print("  show-config           Show current configuration")
    print("\nDatabase:")
    print("  init-db               Initialize MongoDB collections and indexes")
    print("  test-mongodb          Test MongoDB connection")
    print("\nEvents:")
    print("  import-events         Import events from script.js into MongoDB")
    print("  show-events           Show event statistics")
    print("\nTesting:")
    print("  test-ha               Test Home Assistant connection")
    print("  test-notification     Send a test notification")
    print("\nWeb Interface:")
    print("  start-web             Start web interface (http://localhost:5001)")
    print("\nReminders:")
    print("  check-reminders       Check for upcoming events and send reminders")
    print("\nHelp:")
    print("  help                  Show this help message")
    print()


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'init-config': init_config,
        'show-config': show_config,
        'init-db': init_database,
        'import-events': import_events,
        'show-events': show_events,
        'test-ha': test_ha_connection,
        'test-notification': test_notification,
        'test-mongodb': test_mongodb,
        'start-web': start_web_interface,
        'check-reminders': check_reminders_now,
        'help': show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()


if __name__ == '__main__':
    main()
