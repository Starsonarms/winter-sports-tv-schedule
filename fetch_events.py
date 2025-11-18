"""
Helper script to structure winter sports events data.

Since FIS and TV.nu require JavaScript rendering, this script provides
a template for manually adding events you find on those sites.

Future enhancement: Use Selenium or Playwright to automate scraping.
"""

import json
from datetime import datetime

# Template for adding events
EVENTS = [
    # Example entries - replace with real data from FIS-ski.com and tv.nu
    {
        "id": 1,
        "sport": "cross-country",  # or "biathlon"
        "title": "Världscupen i Ruka",
        "competition": "10 km Klassisk - Herrar",
        "channel": "SVT2",
        "date": "2025-11-29",  # YYYY-MM-DD
        "time": "13:15",  # HH:MM
        "description": "Öppningstävling för världscupen",
        "source_fis": "https://www.fis-ski.com/...",
        "source_tv": "https://tv.nu/..."
    },
]

def add_event(sport, title, competition, channel, date, time, description=""):
    """Add a new event to the list."""
    event = {
        "id": len(EVENTS) + 1,
        "sport": sport,
        "title": title,
        "competition": competition,
        "channel": channel,
        "date": date,
        "time": time,
        "description": description
    }
    EVENTS.append(event)
    return event

def export_to_js():
    """Export events to JavaScript format."""
    with open("script.js", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find and replace the events array
    js_events = "const events = " + json.dumps(EVENTS, indent=4, ensure_ascii=False) + ";"
    
    # Replace the existing events array
    start = content.find("const events = [")
    end = content.find("];", start) + 2
    
    new_content = content[:start] + js_events + content[end:]
    
    with open("script.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Exported {len(EVENTS)} events to script.js")

def print_event_template():
    """Print a template for adding new events."""
    print("""
# How to add events:
# 1. Go to https://www.fis-ski.com/DB/general/calendar-results.html
# 2. Filter by Cross-Country or Biathlon
# 3. Note down: Date, Location, Competition type
# 4. Go to https://tv.nu and search for the event name
# 5. Check which Swedish channels are broadcasting
# 6. Add to EVENTS list above

# Example:
add_event(
    sport="cross-country",
    title="Världscupen i Davos",
    competition="Sprint - Damer",
    channel="SVT2",
    date="2025-12-14",
    time="14:00",
    description="Sprint i Schweiz"
)
    """)

if __name__ == "__main__":
    print("Winter Sports TV Schedule - Event Manager")
    print("=" * 50)
    print_event_template()
    print(f"\nCurrently {len(EVENTS)} events in database")
    
    # Uncomment to export
    # export_to_js()
