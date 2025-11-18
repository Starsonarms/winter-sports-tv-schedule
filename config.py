"""
Configuration management for Winter Sports TV Schedule
"""

import os
from pathlib import Path
from typing import List
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    
    # Home Assistant
    home_assistant_url: str = ""
    home_assistant_token: str = ""
    home_assistant_service: str = "notify.persistent_notification"
    
    # MongoDB
    mongodb_uri: str = ""
    mongodb_database: str = "winter_sports"
    
    # Reminders
    reminder_intervals: List[int] = None  # Minutes before event
    reminders_enabled: bool = True
    
    # Sport filters (which sports are shown by default)
    default_sports: List[str] = None
    
    # Time restrictions
    weekday_start_hour: int = 8
    weekday_end_hour: int = 23
    weekend_start_hour: int = 9
    weekend_end_hour: int = 23
    
    def __post_init__(self):
        if self.reminder_intervals is None:
            self.reminder_intervals = [60, 15]  # Default: 1 hour and 15 minutes
        if self.default_sports is None:
            self.default_sports = ['cross-country', 'biathlon']  # Default: längdskidor and skidskytte


def load_env_file(env_path: Path) -> dict:
    """Load environment variables from .env file"""
    env_vars = {}
    
    if not env_path.exists():
        return env_vars
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse key=value
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove inline comments
                if '#' in value:
                    value = value.split('#')[0].strip()
                
                env_vars[key] = value
    
    return env_vars


def get_config() -> Config:
    """Get application configuration from environment variables"""
    
    # Load .env file if it exists
    env_path = Path(__file__).parent / '.env'
    env_vars = load_env_file(env_path)
    
    # Merge with actual environment variables (actual env vars take precedence)
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
    
    # Parse reminder intervals
    reminder_intervals_str = os.getenv('REMINDER_INTERVALS', '60,15')
    reminder_intervals = [int(x.strip()) for x in reminder_intervals_str.split(',')]
    
    # Parse default sports
    default_sports_str = os.getenv('DEFAULT_SPORTS', 'cross-country,biathlon')
    default_sports = [x.strip() for x in default_sports_str.split(',') if x.strip()]
    
    # Parse boolean
    reminders_enabled = os.getenv('REMINDERS_ENABLED', 'true').lower() in ('true', '1', 'yes')
    
    return Config(
        home_assistant_url=os.getenv('HOME_ASSISTANT_URL', ''),
        home_assistant_token=os.getenv('HOME_ASSISTANT_TOKEN', ''),
        home_assistant_service=os.getenv('HOME_ASSISTANT_SERVICE', 'notify.persistent_notification'),
        mongodb_uri=os.getenv('MONGODB_URI', ''),
        mongodb_database=os.getenv('MONGODB_DATABASE', 'winter_sports'),
        reminder_intervals=reminder_intervals,
        reminders_enabled=reminders_enabled,
        default_sports=default_sports,
        weekday_start_hour=int(os.getenv('WEEKDAY_START_HOUR', '8')),
        weekday_end_hour=int(os.getenv('WEEKDAY_END_HOUR', '23')),
        weekend_start_hour=int(os.getenv('WEEKEND_START_HOUR', '9')),
        weekend_end_hour=int(os.getenv('WEEKEND_END_HOUR', '23')),
    )
