"""
MongoDB client for tracking sent reminders
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import get_config

logger = logging.getLogger(__name__)

class MongoDBClient:
    """MongoDB client for reminder tracking"""
    
    def __init__(self):
        self.config = get_config()
        self.client: Optional[MongoClient] = None
        self.db = None
        self.reminders_collection = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB Atlas"""
        try:
            # Get URI from config
            uri = self.config.mongodb_uri
            
            if not uri:
                logger.warning("MongoDB URI not configured. Reminders will work but duplicates may occur.")
                self.client = None
                self.db = None
                self.reminders_collection = None
                return
            
            # Create client with SSL/TLS settings
            self.client = MongoClient(
                uri,
                server_api=ServerApi('1'),
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.config.mongodb_database]
            self.reminders_collection = self.db['sent_reminders']
            
            # Initialize collections and indexes
            self._initialize_collections()
            
            logger.info(f"Successfully connected to MongoDB Atlas (database: {self.config.mongodb_database})")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"MongoDB connection failed: {e}. Reminders will work but duplicates may occur.")
            self.client = None
            self.db = None
            self.reminders_collection = None
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
            self.reminders_collection = None
    
    def _initialize_collections(self):
        """Initialize collections and indexes"""
        try:
            # Create index on event_id and minutes_before for faster lookups and to prevent duplicates
            self.reminders_collection.create_index([
                ('event_id', 1),
                ('minutes_before', 1)
            ], unique=True)
            
            # Create index on event_datetime for cleanup queries
            self.reminders_collection.create_index('event_datetime')
            
            # Create index on sent_at for sorting recent reminders
            self.reminders_collection.create_index([('sent_at', -1)])
            
            logger.info("MongoDB collections and indexes initialized")
            
        except Exception as e:
            # Indexes might already exist, which is fine
            logger.debug(f"Index creation note: {e}")
    
    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self.client is not None and self.db is not None
    
    def has_reminder_been_sent(self, event_id: str, minutes_before: int) -> bool:
        """Check if a reminder has already been sent for this event"""
        if not self.is_connected():
            logger.warning("MongoDB not connected, cannot check reminder status")
            return False
        
        try:
            result = self.reminders_collection.find_one({
                'event_id': event_id,
                'minutes_before': minutes_before
            })
            
            return result is not None
            
        except Exception as e:
            logger.error(f"Error checking reminder status: {e}")
            return False
    
    def mark_reminder_sent(self, event_id: str, event_title: str, minutes_before: int, 
                          event_datetime: datetime) -> bool:
        """Mark a reminder as sent"""
        if not self.is_connected():
            logger.warning("MongoDB not connected, cannot mark reminder as sent")
            return False
        
        try:
            self.reminders_collection.update_one(
                {
                    'event_id': event_id,
                    'minutes_before': minutes_before
                },
                {
                    '$set': {
                        'event_id': event_id,
                        'event_title': event_title,
                        'minutes_before': minutes_before,
                        'event_datetime': event_datetime,
                        'sent_at': datetime.now(),
                    }
                },
                upsert=True
            )
            
            logger.debug(f"Marked reminder as sent: {event_title} ({minutes_before} min)")
            return True
            
        except Exception as e:
            logger.error(f"Error marking reminder as sent: {e}")
            return False
    
    def get_sent_reminders(self, limit: int = 100) -> List[Dict]:
        """Get list of sent reminders"""
        if not self.is_connected():
            logger.warning("MongoDB not connected")
            return []
        
        try:
            reminders = list(self.reminders_collection.find(
                {},
                {'_id': 0}
            ).sort('sent_at', -1).limit(limit))
            
            return reminders
            
        except Exception as e:
            logger.error(f"Error getting sent reminders: {e}")
            return []
    
    def cleanup_old_reminders(self, days: int = 7) -> int:
        """Remove reminders older than specified days"""
        if not self.is_connected():
            logger.warning("MongoDB not connected")
            return 0
        
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            result = self.reminders_collection.delete_many({
                'event_datetime': {'$lt': cutoff_date}
            })
            
            deleted_count = result.deleted_count
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old reminders")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old reminders: {e}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
