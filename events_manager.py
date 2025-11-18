"""
Events manager - handles storing and retrieving TV schedule events from MongoDB
"""

import json
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class EventsManager:
    """Manage winter sports events in MongoDB"""
    
    def __init__(self):
        self.db_client = MongoDBClient()
        if self.db_client.is_connected():
            self.events_collection = self.db_client.db['events']
            self._initialize_collection()
        else:
            self.events_collection = None
            logger.warning("MongoDB not connected - EventsManager functionality limited")
    
    def _initialize_collection(self):
        """Initialize events collection with indexes"""
        try:
            # Create indexes
            self.events_collection.create_index('id', unique=True)
            self.events_collection.create_index('sport')
            self.events_collection.create_index('date')
            self.events_collection.create_index([('date', 1), ('time', 1)])
            
            logger.info("Events collection initialized")
        except Exception as e:
            logger.debug(f"Index creation note: {e}")
    
    def import_events_from_js(self) -> int:
        """Import events from script.js file into MongoDB"""
        script_path = Path(__file__).parent / 'script.js'
        
        if not script_path.exists():
            logger.error("script.js not found")
            return 0
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the events array in the JavaScript file
            match = re.search(r'const events = (\[[\s\S]*?\n\];)', content)
            
            if not match:
                logger.error("Could not find events array in script.js")
                return 0
            
            # Extract the JSON array
            json_str = match.group(1)
            # Remove trailing semicolon
            json_str = json_str.rstrip(';')
            
            # Parse JSON
            events = json.loads(json_str)
            
            # Import into MongoDB
            imported = 0
            for event in events:
                try:
                    # Upsert event (update if exists, insert if not)
                    self.events_collection.update_one(
                        {'id': event['id']},
                        {'$set': event},
                        upsert=True
                    )
                    imported += 1
                except Exception as e:
                    logger.error(f"Error importing event {event.get('id')}: {e}")
            
            logger.info(f"Imported {imported} events from script.js")
            return imported
            
        except Exception as e:
            logger.error(f"Error importing events from script.js: {e}")
            return 0
    
    def get_all_events(self) -> List[Dict]:
        """Get all events from MongoDB"""
        if self.events_collection is None:
            return []
        
        try:
            events = list(self.events_collection.find(
                {},
                {'_id': 0}  # Exclude MongoDB _id field
            ).sort([('date', 1), ('time', 1)]))
            
            return events
        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []
    
    def get_events_by_sport(self, sport: str) -> List[Dict]:
        """Get events filtered by sport"""
        if self.events_collection is None:
            return []
        
        try:
            events = list(self.events_collection.find(
                {'sport': sport},
                {'_id': 0}
            ).sort([('date', 1), ('time', 1)]))
            
            return events
        except Exception as e:
            logger.error(f"Error getting events by sport: {e}")
            return []
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get events happening in the next N days"""
        if self.events_collection is None:
            return []
        
        try:
            from datetime import timedelta
            today = datetime.now().date()
            end_date = today + timedelta(days=days)
            
            # Convert to string format (YYYY-MM-DD)
            today_str = today.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            events = list(self.events_collection.find(
                {
                    'date': {
                        '$gte': today_str,
                        '$lte': end_date_str
                    }
                },
                {'_id': 0}
            ).sort([('date', 1), ('time', 1)]))
            
            return events
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            return []
    
    def add_event(self, event: Dict) -> bool:
        """Add or update a single event"""
        if self.events_collection is None:
            return False
        
        try:
            # Ensure event has an ID
            if 'id' not in event:
                # Generate ID from existing events
                max_id = self.events_collection.find_one(
                    {},
                    sort=[('id', -1)]
                )
                event['id'] = (max_id['id'] + 1) if max_id else 1
            
            self.events_collection.update_one(
                {'id': event['id']},
                {'$set': event},
                upsert=True
            )
            
            logger.info(f"Added/updated event: {event.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Error adding event: {e}")
            return False
    
    def delete_event(self, event_id: int) -> bool:
        """Delete an event by ID"""
        if self.events_collection is None:
            return False
        
        try:
            result = self.events_collection.delete_one({'id': event_id})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted event {event_id}")
                return True
            else:
                logger.warning(f"Event {event_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
            return False
    
    def get_event_count(self) -> int:
        """Get total number of events"""
        if self.events_collection is None:
            return 0
        
        try:
            return self.events_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error counting events: {e}")
            return 0
    
    def get_sports_list(self) -> List[str]:
        """Get list of unique sports"""
        if self.events_collection is None:
            return []
        
        try:
            sports = self.events_collection.distinct('sport')
            return sorted(sports)
        except Exception as e:
            logger.error(f"Error getting sports list: {e}")
            return []
    
    def clear_all_events(self) -> bool:
        """Clear all events (use with caution!)"""
        if self.events_collection is None:
            return False
        
        try:
            result = self.events_collection.delete_many({})
            logger.info(f"Cleared {result.deleted_count} events")
            return True
        except Exception as e:
            logger.error(f"Error clearing events: {e}")
            return False
    
    def cleanup_past_events(self) -> int:
        """Delete events that have already passed"""
        if self.events_collection is None:
            return 0
        
        try:
            from datetime import datetime, timedelta
            
            # Get yesterday's date (to be safe, delete events from yesterday and before)
            yesterday = (datetime.now() - timedelta(days=1)).date()
            cutoff_date = yesterday.strftime('%Y-%m-%d')
            
            # Delete events before the cutoff date
            result = self.events_collection.delete_many({
                'date': {'$lt': cutoff_date}
            })
            
            if result.deleted_count > 0:
                logger.info(f"Cleaned up {result.deleted_count} past events")
            
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up past events: {e}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        if self.db_client:
            self.db_client.close()
