"""
Automatic update script for winter sports events.
Runs without user prompts for scheduled automation.
"""

import json
import re
from datetime import datetime
from urllib.request import urlopen
import sys

# FIS Calendar URLs
FIS_CC_URL = "https://data.fis-ski.com/services/public/icalendar-feed-fis-events.html?seasoncode=2026&sectorcode=CC&categorycode=WC"

# IBU API URL for biathlon events
IBU_API_URL = "https://biathlonresults.com/modules/sportapi/api/Events?SeasonId=2526&Level=1"

def parse_ical_event(event_text):
    """Parse a single VEVENT from iCalendar format."""
    event = {}
    
    # Extract fields using regex
    summary_match = re.search(r'SUMMARY:(.+)', event_text)
    location_match = re.search(r'LOCATION:(.+)', event_text)
    dtstart_match = re.search(r'DTSTART(?:;VALUE=DATE)?:(\d{8})', event_text)
    description_match = re.search(r'DESCRIPTION:(.+?)(?=\n[A-Z])', event_text, re.DOTALL)
    
    if not summary_match or not location_match or not dtstart_match:
        return None
    
    summary = summary_match.group(1).strip()
    location = location_match.group(1).strip()
    date_str = dtstart_match.group(1)
    
    # Extract gender and discipline
    gender = None
    discipline = None
    category = None
    
    if description_match:
        desc = description_match.group(1)
        gender_match = re.search(r'Gender: ([WM])', desc)
        discipline_match = re.search(r'Discipline: (.+?)\\n', desc)
        category_match = re.search(r'Category: (.+?)\\n', desc)
        
        if gender_match:
            gender = gender_match.group(1)
        if discipline_match:
            discipline = discipline_match.group(1)
        if category_match:
            category = category_match.group(1)
    
    # Only include World Cup (WC) events
    if category != "WC":
        return None
    
    # Parse date
    try:
        event_date = datetime.strptime(date_str, "%Y%m%d")
    except:
        return None
    
    # Format discipline names
    discipline_map = {
        'SP': 'Sprint',
        '10k': '10 km',
        '30k': '30 km',
        '50k': '50 km',
        '15k': '15 km',
        'Skt': 'Skiatlon',
        'Tsp': 'Teamsprint',
        'HMS': 'Mass Start',
        'Pur': 'Pursuit'
    }
    
    discipline_name = discipline_map.get(discipline, discipline)
    gender_text = "Damer" if gender == "W" else "Herrar"
    
    event = {
        'location': location,
        'date': event_date.strftime("%Y-%m-%d"),
        'gender': gender,
        'discipline': discipline_name,
        'competition': f"{discipline_name} - {gender_text}",
        'summary': summary
    }
    
    return event

def fetch_and_parse_calendar(url):
    """Fetch and parse iCalendar data."""
    try:
        with urlopen(url) as response:
            ical_data = response.read().decode('utf-8')
        
        # Split into individual events
        events = []
        event_blocks = re.findall(r'BEGIN:VEVENT(.+?)END:VEVENT', ical_data, re.DOTALL)
        
        for block in event_blocks:
            event = parse_ical_event(block)
            if event:
                events.append(event)
        
        return events
    except Exception as e:
        print(f"Error fetching calendar: {e}", file=sys.stderr)
        return []

def fetch_biathlon_events():
    """Fetch biathlon events from IBU API."""
    try:
        with urlopen(IBU_API_URL) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        events = []
        # Check if data is a list or has a 'value' key
        items = data if isinstance(data, list) else data.get('value', [])
        
        for item in items:
            # Only include World Cup events (Level 1)
            if item.get('Level') != 1:
                continue
            
            start_date = datetime.fromisoformat(item['StartDate'].replace('Z', '+00:00'))
            
            event = {
                'location': item.get('ShortDescription', ''),
                'date': start_date.strftime('%Y-%m-%d'),
                'country': item.get('Nat', ''),
                'event_id': item.get('EventId', '')
            }
            events.append(event)
        
        return events
    except Exception as e:
        print(f"Error fetching biathlon events: {e}", file=sys.stderr)
        return []

def generate_js_events(cc_events, biathlon_events):
    """Generate JavaScript events array with channel placeholders."""
    js_events = []
    event_id = 1
    
    # Process cross-country events
    cc_events.sort(key=lambda x: x['date'])
    
    for event in cc_events:
        # Default channels for Swedish broadcasts
        channel = "SVT2"
        time = "13:00"
        
        # Special cases
        if "Falun" in event['location']:
            channel = "SVT1"
        elif "Oslo" in event['location'] or "Drammen" in event['location']:
            channel = "SVT2"
        
        js_event = {
            "id": event_id,
            "sport": "cross-country",
            "title": f"Världscupen i {event['location']}",
            "competition": event['competition'],
            "channel": channel,
            "date": event['date'],
            "time": time,
            "description": f"Världscuptävling i {event['location']}"
        }
        
        js_events.append(js_event)
        event_id += 1
    
    # Process biathlon events
    biathlon_events.sort(key=lambda x: x['date'])
    
    for event in biathlon_events:
        channel = "SVT2"
        time = "14:15"
        
        if event['country'] == 'SWE':
            channel = "SVT1"
        
        js_event = {
            "id": event_id,
            "sport": "biathlon",
            "title": f"Världscupen i {event['location']}",
            "competition": "Världscup",
            "channel": channel,
            "date": event['date'],
            "time": time,
            "description": f"Skidskytte-världscup i {event['location']}"
        }
        
        js_events.append(js_event)
        event_id += 1
    
    # Sort all events by date
    js_events.sort(key=lambda x: x['date'])
    
    # Renumber IDs
    for idx, event in enumerate(js_events, 1):
        event['id'] = idx
    
    return js_events

def update_script_js(events):
    """Update script.js with new events."""
    try:
        with open("script.js", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Generate JavaScript array
        js_code = "const events = " + json.dumps(events, indent=4, ensure_ascii=False) + ";"
        
        # Replace the existing events array
        start = content.find("const events = [")
        if start == -1:
            print("Could not find events array in script.js", file=sys.stderr)
            return False
        
        end = content.find("];", start) + 2
        
        new_content = content[:start] + js_code + content[end:]
        
        with open("script.js", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error updating script.js: {e}", file=sys.stderr)
        return False

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting automatic update...")
    
    print("Fetching FIS Cross-Country World Cup Calendar...")
    cc_events = fetch_and_parse_calendar(FIS_CC_URL)
    print(f"Found {len(cc_events)} cross-country World Cup events")
    
    print("Fetching IBU Biathlon World Cup Calendar...")
    biathlon_events = fetch_biathlon_events()
    print(f"Found {len(biathlon_events)} biathlon World Cup events")
    
    if not cc_events and not biathlon_events:
        print("ERROR: No events found or error fetching data", file=sys.stderr)
        sys.exit(1)
    
    # Generate JavaScript events
    js_events = generate_js_events(cc_events, biathlon_events)
    
    print(f"Generated {len(js_events)} total events")
    print(f"  - {len(cc_events)} cross-country events")
    print(f"  - {len(biathlon_events)} biathlon events")
    
    # Save to JSON for review
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(js_events, f, indent=2, ensure_ascii=False)
    
    print("Events saved to events.json")
    
    # Update script.js automatically
    if update_script_js(js_events):
        print("✅ script.js updated successfully!")
        sys.exit(0)
    else:
        print("❌ Failed to update script.js", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
