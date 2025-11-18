"""
Home Assistant integration for sending event reminders
"""

import requests
import logging
from typing import Dict, Optional
from datetime import datetime, time
from config import get_config

logger = logging.getLogger(__name__)

class HomeAssistantNotifier:
    """Send event reminders to Home Assistant"""
    
    def __init__(self, ha_url: str = None, ha_token: str = None):
        self.config = get_config()
        self.ha_url = ha_url or self.config.home_assistant_url
        self.ha_token = ha_token or self.config.home_assistant_token
        self.ha_service = self.config.home_assistant_service
        
        # Remove trailing slash from URL
        if self.ha_url and self.ha_url.endswith('/'):
            self.ha_url = self.ha_url[:-1]
        
        self.headers = {
            'Authorization': f'Bearer {self.ha_token}',
            'Content-Type': 'application/json',
        }
    
    def _is_notification_time_allowed(self) -> bool:
        """Check if current time is within allowed notification hours"""
        try:
            now = datetime.now()
            current_time = now.time()
            is_weekend = now.weekday() >= 5  # Saturday = 5, Sunday = 6
            
            if is_weekend:
                start_time = time(self.config.weekend_start_hour, 0)
                end_time = time(self.config.weekend_end_hour, 59, 59)
            else:
                start_time = time(self.config.weekday_start_hour, 0)
                end_time = time(self.config.weekday_end_hour, 59, 59)
            
            is_allowed = start_time <= current_time <= end_time
            
            if not is_allowed:
                day_type = "weekend" if is_weekend else "weekday"
                logger.info(f"Notification blocked - current time {current_time} is outside {day_type} allowed hours ({start_time}-{end_time})")
            
            return is_allowed
            
        except Exception as e:
            logger.error(f"Error checking notification time: {e}")
            return True  # Default to allowing notifications if check fails
    
    def test_connection(self) -> bool:
        """Test connection to Home Assistant"""
        try:
            if not self.ha_token:
                logger.error("Home Assistant token not configured")
                return False
            
            response = requests.get(
                f"{self.ha_url}/api/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info("Successfully connected to Home Assistant")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Home Assistant: {e}")
            return False
    
    def send_reminder(self, event: Dict, minutes_before: int) -> bool:
        """Send reminder notification about an upcoming event"""
        try:
            if not self.ha_token:
                logger.error("Home Assistant token not configured")
                return False
            
            # Check if reminders are enabled
            if not self.config.reminders_enabled:
                logger.info("Reminders are disabled in configuration")
                return False
            
            # Check time restrictions
            if not self._is_notification_time_allowed():
                logger.info(f"Reminder for '{event.get('title', 'Unknown')}' delayed due to time restrictions")
                return False
            
            # Prepare notification data
            if minutes_before <= 15:
                title = f"⏰ {event.get('title', 'Unknown')} börjar om {minutes_before} min!"
            else:
                hours = minutes_before // 60
                if hours == 1:
                    title = f"🏔️ {event.get('title', 'Unknown')} börjar om 1 timme"
                else:
                    title = f"🏔️ {event.get('title', 'Unknown')} börjar om {hours} timmar"
            
            message = self._format_message(event)
            
            # Send notification via Home Assistant service
            success = self._send_via_service(title, message, event)
            
            if success:
                logger.info(f"Reminder sent for event ({minutes_before} min): {event.get('title', 'Unknown')}")
            else:
                logger.error(f"Failed to send reminder for event: {event.get('title', 'Unknown')}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return False
    
    def _format_message(self, event: Dict) -> str:
        """Format the reminder message"""
        try:
            lines = []
            
            # Sport emoji mapping
            sport_emojis = {
                'cross-country': '⛷️',
                'biathlon': '🎯',
                'alpine': '🎿',
                'ski-jumping': '🪂',
                'ice-hockey': '🏒',
                'figure-skating': '⛸️',
                'speed-skating': '⏱️',
                'curling': '🥌',
                'other': '🏆'
            }
            
            sport = event.get('sport', 'other')
            emoji = sport_emojis.get(sport, '🏔️')
            
            # Event info
            if event.get('title'):
                lines.append(f"{emoji} {event['title']}")
            
            if event.get('competition'):
                lines.append(f"🏆 {event['competition']}")
            
            if event.get('channel'):
                lines.append(f"📺 {event['channel']}")
            
            if event.get('date') and event.get('time'):
                lines.append(f"🕐 {event['date']} kl. {event['time']}")
            
            if event.get('description'):
                desc = event['description'][:150]
                if len(event.get('description', '')) > 150:
                    desc += "..."
                lines.append(f"ℹ️ {desc}")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return f"Upcoming event: {event.get('title', 'Unknown')}"
    
    def _send_via_service(self, title: str, message: str, event: Dict) -> bool:
        """Send notification via Home Assistant service call"""
        try:
            # Parse service domain and name
            service_parts = self.ha_service.split('.')
            if len(service_parts) != 2:
                logger.error(f"Invalid service format: {self.ha_service}. Expected 'domain.service'")
                return False
            
            domain, service = service_parts
            
            # Prepare service call data
            service_data = {
                "title": title,
                "message": message,
            }
            
            # Add additional data for mobile notifications
            if "mobile_app" in domain or "mobile_app" in service:
                notification_data = {
                    "url": "homeassistant://navigate/dashboard-vintersport/0",
                    "group": "winter_sports_reminders",
                    "tag": f"event_{event.get('id', 'unknown')}",
                    "priority": "high",
                    "clickAction": "homeassistant://navigate/dashboard-vintersport/0",
                }
                
                service_data["data"] = notification_data
            
            # Make service call
            url = f"{self.ha_url}/api/services/{domain}/{service}"
            
            response = requests.post(
                url,
                json=service_data,
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            logger.debug(f"Service call successful: {response.status_code}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error sending notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending via service: {e}")
            return False
    
    def send_test_notification(self) -> bool:
        """Send a test notification"""
        try:
            test_event = {
                'id': 'test_123',
                'sport': 'cross-country',
                'title': 'Test Event - Vintersport TV-guide',
                'competition': 'Test Competition',
                'channel': 'SVT2',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '14:00',
                'description': 'This is a test reminder from your Winter Sports TV Schedule.'
            }
            
            return self.send_reminder(test_event, 60)
            
        except Exception as e:
            logger.error(f"Error sending test notification: {e}")
            return False
    
    def get_services(self) -> Optional[Dict]:
        """Get available Home Assistant services"""
        try:
            response = requests.get(
                f"{self.ha_url}/api/services",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            services = response.json()
            
            # Filter to notification services
            notification_services = []
            for service in services:
                domain = service.get('domain', '')
                if 'notify' in domain or 'mobile_app' in domain:
                    notification_services.append(service)
            
            return {
                'all_services': len(services),
                'notification_services': notification_services
            }
            
        except Exception as e:
            logger.error(f"Error getting services: {e}")
            return None
