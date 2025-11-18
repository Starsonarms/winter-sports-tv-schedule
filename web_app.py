"""
Web interface for Winter Sports TV Schedule settings
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import os
from pathlib import Path
from typing import Dict
from config import get_config
from home_assistant import HomeAssistantNotifier
from mongodb_client import MongoDBClient
from events_manager import EventsManager

logger = logging.getLogger(__name__)

def update_env_file(updates: Dict[str, str]):
    """Update .env file with new values"""
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        logger.warning(f".env file not found at {env_path}")
        return False
    
    try:
        # Read existing .env file
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Update values
        updated_lines = []
        updated_keys = set()
        
        for line in lines:
            stripped = line.strip()
            # Skip comments and empty lines
            if not stripped or stripped.startswith('#'):
                updated_lines.append(line)
                continue
            
            # Check if this line contains a key we want to update
            key_found = False
            for key, value in updates.items():
                if stripped.startswith(f"{key}="):
                    updated_lines.append(f"{key}={value}\n")
                    updated_keys.add(key)
                    key_found = True
                    break
            
            if not key_found:
                updated_lines.append(line)
        
        # Add any new keys that weren't found
        for key, value in updates.items():
            if key not in updated_keys:
                updated_lines.append(f"{key}={value}\n")
        
        # Write back to file
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        logger.info(f"Updated .env file with: {list(updates.keys())}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating .env file: {e}")
        return False


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Enable CORS
    CORS(app)
    
    config = get_config()
    
    @app.after_request
    def after_request(response):
        # Add cache-control headers for API endpoints
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html', config=config)
    
    @app.route('/settings')
    def settings():
        """Settings page"""
        config = get_config()
        return render_template('settings.html', config=config)
    
    @app.route('/schedule')
    def schedule():
        """TV schedule page - loads events from MongoDB"""
        config = get_config()
        return render_template('schedule.html', config=config)
    
    @app.route('/script.js')
    def script_js():
        """Serve script.js"""
        from flask import send_from_directory
        return send_from_directory('.', 'script.js')
    
    @app.route('/styles.css')
    def styles_css():
        """Serve styles.css"""
        from flask import send_from_directory
        return send_from_directory('.', 'styles.css')
    
    @app.route('/api/config/reminders', methods=['POST'])
    def update_reminder_config():
        """Update reminder configuration"""
        try:
            data = request.get_json()
            
            # Validate input
            reminder_intervals = data.get('reminder_intervals')
            reminders_enabled = data.get('reminders_enabled')
            
            if not isinstance(reminders_enabled, bool):
                return jsonify({
                    'status': 'error',
                    'error': 'reminders_enabled must be true or false'
                }), 400
            
            # Validate reminder intervals
            if not isinstance(reminder_intervals, list) or len(reminder_intervals) == 0:
                return jsonify({
                    'status': 'error',
                    'error': 'reminder_intervals must be a non-empty list'
                }), 400
            
            for interval in reminder_intervals:
                if not isinstance(interval, int) or interval < 1:
                    return jsonify({
                        'status': 'error',
                        'error': 'All reminder intervals must be positive integers'
                    }), 400
            
            # Persist to .env file
            env_updates = {
                'REMINDER_INTERVALS': ','.join(map(str, reminder_intervals)),
                'REMINDERS_ENABLED': 'true' if reminders_enabled else 'false'
            }
            update_env_file(env_updates)
            
            logger.info(f"Reminder settings updated: intervals={reminder_intervals}, enabled={reminders_enabled}")
            
            return jsonify({
                'status': 'success',
                'message': 'Reminder settings saved successfully!'
            })
            
        except Exception as e:
            logger.error(f"Error updating reminder config: {e}")
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    @app.route('/api/config/time', methods=['POST'])
    def update_time_config():
        """Update time-based notification configuration"""
        try:
            data = request.get_json()
            
            # Validate input
            weekday_start = data.get('weekday_start_hour')
            weekday_end = data.get('weekday_end_hour')
            weekend_start = data.get('weekend_start_hour')
            weekend_end = data.get('weekend_end_hour')
            
            # Validate hours (0-23)
            for hour, name in [
                (weekday_start, 'weekday_start'),
                (weekday_end, 'weekday_end'),
                (weekend_start, 'weekend_start'),
                (weekend_end, 'weekend_end')
            ]:
                if not isinstance(hour, int) or hour < 0 or hour > 23:
                    return jsonify({
                        'status': 'error',
                        'error': f'{name} must be between 0 and 23'
                    }), 400
            
            # Persist to .env file
            env_updates = {
                'WEEKDAY_START_HOUR': str(weekday_start),
                'WEEKDAY_END_HOUR': str(weekday_end),
                'WEEKEND_START_HOUR': str(weekend_start),
                'WEEKEND_END_HOUR': str(weekend_end)
            }
            update_env_file(env_updates)
            
            logger.info(f"Time settings updated: weekdays {weekday_start}-{weekday_end}, weekends {weekend_start}-{weekend_end}")
            
            return jsonify({
                'status': 'success',
                'message': 'Time settings saved successfully!'
            })
            
        except Exception as e:
            logger.error(f"Error updating time config: {e}")
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    @app.route('/api/config/sports', methods=['POST'])
    def update_sports_config():
        """Update default sport filters"""
        try:
            data = request.get_json()
            
            # Validate input
            default_sports = data.get('default_sports')
            
            if not isinstance(default_sports, list):
                return jsonify({
                    'status': 'error',
                    'error': 'default_sports must be a list'
                }), 400
            
            # Valid sport types
            valid_sports = [
                'cross-country', 'biathlon', 'alpine', 'ski-jumping',
                'ice-hockey', 'figure-skating', 'speed-skating', 'curling', 'other'
            ]
            
            for sport in default_sports:
                if sport not in valid_sports:
                    return jsonify({
                        'status': 'error',
                        'error': f'Invalid sport: {sport}'
                    }), 400
            
            # Persist to .env file
            env_updates = {
                'DEFAULT_SPORTS': ','.join(default_sports) if default_sports else 'cross-country,biathlon'
            }
            update_env_file(env_updates)
            
            logger.info(f"Sport filters updated: {default_sports}")
            
            return jsonify({
                'status': 'success',
                'message': 'Sport filters saved successfully!'
            })
            
        except Exception as e:
            logger.error(f"Error updating sport filters: {e}")
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    @app.route('/api/test-ha')
    def test_ha():
        """Test Home Assistant connection"""
        try:
            notifier = HomeAssistantNotifier()
            
            if notifier.test_connection():
                return jsonify({
                    'status': 'success',
                    'message': 'Successfully connected to Home Assistant!'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'error': 'Failed to connect to Home Assistant'
                }), 500
                
        except Exception as e:
            logger.error(f"Error testing Home Assistant: {e}")
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    @app.route('/api/test-notification')
    def test_notification():
        """Send test notification"""
        try:
            notifier = HomeAssistantNotifier()
            
            if notifier.send_test_notification():
                return jsonify({
                    'status': 'success',
                    'message': 'Test notification sent! Check your phone.'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'error': 'Failed to send test notification'
                }), 500
                
        except Exception as e:
            logger.error(f"Error sending test notification: {e}")
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    @app.route('/api/test-mongodb')
    def test_mongodb():
        """Test MongoDB connection"""
        try:
            db_client = MongoDBClient()
            
            if db_client.is_connected():
                reminders_count = len(db_client.get_sent_reminders(limit=1000))
                db_client.close()
                
                return jsonify({
                    'status': 'success',
                    'message': f'Successfully connected to MongoDB! ({reminders_count} reminders tracked)'
                })
            else:
                return jsonify({
                    'status': 'warning',
                    'message': 'MongoDB connection failed (optional - reminders will still work)'
                })
                
        except Exception as e:
            logger.error(f"Error testing MongoDB: {e}")
            return jsonify({
                'status': 'warning',
                'message': 'MongoDB connection failed (optional - reminders will still work)'
            })
    
    @app.route('/api/events')
    def get_events():
        """Get all events from MongoDB"""
        try:
            events_manager = EventsManager()
            events = events_manager.get_all_events()
            events_manager.close()
            
            return jsonify({
                'status': 'success',
                'events': events,
                'count': len(events)
            })
        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'events': [],
                'count': 0
            }), 500
    
    @app.route('/api/events/import', methods=['POST'])
    def import_events():
        """Import events from script.js into MongoDB"""
        try:
            events_manager = EventsManager()
            count = events_manager.import_events_from_js()
            events_manager.close()
            
            if count > 0:
                return jsonify({
                    'status': 'success',
                    'message': f'Imported {count} events successfully!'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'error': 'No events imported'
                }), 500
        except Exception as e:
            logger.error(f"Error importing events: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'API endpoint not found', 'status': 'error'}), 404
        return render_template('error.html', error="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error', 'status': 'error'}), 500
        return render_template('error.html', error="Internal server error"), 500
    
    return app


def run_web_app():
    """Run the web application"""
    app = create_app()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting web interface on http://localhost:5001")
    
    try:
        # Use Waitress for production-ready serving
        from waitress import serve
        serve(app, host='0.0.0.0', port=5001, threads=4)
    except ImportError:
        # Fallback to Flask development server
        logger.warning("Waitress not available, using Flask development server")
        app.run(host='0.0.0.0', port=5001, debug=False)


if __name__ == '__main__':
    run_web_app()
