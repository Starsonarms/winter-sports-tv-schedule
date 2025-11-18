"""
Scrape tv.nu for winter sports schedules on SVT1, SVT2, and TV4.
"""

import json
import os
import re
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.parse import quote
from html.parser import HTMLParser

# Channels to search
CHANNELS = ['svt1', 'svt2', 'tv4']

# Search terms for winter sports
SEARCH_TERMS = ['längdskidor', 'skidskytte']

class TVNuParser(HTMLParser):
    """Parse tv.nu HTML to extract program information."""
    
    def __init__(self):
        super().__init__()
        self.programs = []
        self.current_program = {}
        self.in_program = False
        self.in_title = False
        self.in_time = False
        self.in_channel = False
        self.current_data = []
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Look for program containers
        if tag == 'div' and 'class' in attrs_dict:
            classes = attrs_dict['class']
            if 'program' in classes or 'schedule-item' in classes:
                self.in_program = True
                self.current_program = {}
        
        # Look for specific fields
        if self.in_program:
            if tag == 'h2' or tag == 'h3' or (tag == 'a' and 'program-title' in attrs_dict.get('class', '')):
                self.in_title = True
            elif tag == 'time' or (tag == 'span' and 'time' in attrs_dict.get('class', '')):
                self.in_time = True
                if 'datetime' in attrs_dict:
                    self.current_program['datetime'] = attrs_dict['datetime']
            elif tag == 'span' and 'channel' in attrs_dict.get('class', ''):
                self.in_channel = True
    
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_program:
            if self.current_program:
                self.programs.append(self.current_program.copy())
            self.in_program = False
            self.current_program = {}
        
        if tag in ['h2', 'h3', 'a']:
            self.in_title = False
        elif tag == 'time' or tag == 'span':
            self.in_time = False
            self.in_channel = False
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        
        if self.in_title:
            self.current_program['title'] = data
        elif self.in_time:
            self.current_program['time'] = data
        elif self.in_channel:
            self.current_program['channel'] = data

def fetch_tvnu_search(search_term, channel=None):
    """
    Fetch search results from tv.nu web API.
    
    Args:
        search_term: What to search for (e.g., 'längdskidor')
        channel: Optional channel filter
    
    Returns:
        JSON response from API
    """
    base_url = "https://web-api.tv.nu/search"
    
    # Build search URL
    params = f"q={quote(search_term)}"
    if channel:
        params += f"&channelIds={channel}"
    
    url = f"{base_url}?{params}"
    
    try:
        request = Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        request.add_header('Accept', 'application/json')
        
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error fetching tv.nu search for '{search_term}': {e}")
        return None

def parse_tvnu_json(api_response, channel_name):
    """
    Parse tv.nu API JSON response to extract program information.
    
    Args:
        api_response: JSON response from tv.nu API
        channel_name: Channel name to filter by
    
    Returns:
        List of program dictionaries
    """
    programs = []
    
    if not api_response or not isinstance(api_response, dict):
        return programs
    
    # API response structure: {"programs": [...], "broadcasts": [...], ...}
    broadcasts = api_response.get('broadcasts', [])
    program_info = {p['id']: p for p in api_response.get('programs', [])}
    channel_info = {c['id']: c for c in api_response.get('channels', [])}
    
    for broadcast in broadcasts:
        program_id = broadcast.get('program', {}).get('id') if isinstance(broadcast.get('program'), dict) else broadcast.get('program')
        channel_id = broadcast.get('channel', {}).get('id') if isinstance(broadcast.get('channel'), dict) else broadcast.get('channel')
        
        # Get program details
        program = program_info.get(program_id, broadcast.get('program', {}))
        if isinstance(program, str):
            program = {'id': program}
        
        # Get channel details  
        channel = channel_info.get(channel_id, broadcast.get('channel', {}))
        if isinstance(channel, str):
            channel = {'id': channel, 'name': channel}
        
        channel_slug = channel.get('slug', '').lower()
        
        # Filter by channel if specified
        if channel_name and channel_name.lower() not in channel_slug:
            continue
        
        # Get program title
        title = program.get('name', program.get('title', ''))
        
        # Get start time
        start_time = broadcast.get('start', broadcast.get('startTime', ''))
        
        if not title or not start_time:
            continue
        
        # Parse datetime
        try:
            dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        except:
            continue
        
        prog_dict = {
            'title': title,
            'channel': channel.get('name', channel_name).upper(),
            'datetime': start_time,
            'time': dt.strftime('%H:%M'),
            'date': dt.strftime('%Y-%m-%d')
        }
        programs.append(prog_dict)
    
    return programs

def scrape_channel_schedule(channel_name, days_ahead=14):
    """
    Scrape channel schedule from tv.nu.
    
    Args:
        channel_name: Channel name (e.g., 'svt1')
        days_ahead: How many days ahead to check
    
    Returns:
        List of winter sports programs
    """
    print(f"🔍 Searching {channel_name.upper()} for winter sports...")
    
    all_programs = []
    
    for search_term in SEARCH_TERMS:
        api_response = fetch_tvnu_search(search_term, channel_name)
        
        if not api_response:
            continue
        
        programs = parse_tvnu_json(api_response, channel_name)
        
        # Determine sport type
        sport_type = 'biathlon' if 'skytte' in search_term else 'cross-country'
        
        for prog in programs:
            prog['sport'] = sport_type
            prog['search_term'] = search_term
        
        all_programs.extend(programs)
        print(f"  Found {len(programs)} results for '{search_term}'")
    
    return all_programs

def extract_event_info(program):
    """
    Extract structured event information from program data.
    
    Args:
        program: Program dictionary from tv.nu
    
    Returns:
        Event dictionary
    """
    title = program['title']
    
    # Parse datetime
    date = ''
    time = program.get('time', '')
    
    if program.get('datetime'):
        try:
            dt = datetime.fromisoformat(program['datetime'].replace('Z', '+00:00'))
            date = dt.strftime('%Y-%m-%d')
            if not time:
                time = dt.strftime('%H:%M')
        except:
            pass
    
    # Extract location from title (e.g., "Längdskidor: Världscupen i Ruka")
    location_match = re.search(r'(?:i|från)\s+([A-ZÅÄÖ][a-zåäö]+)', title)
    location = location_match.group(1) if location_match else ''
    
    # Extract competition type
    competition = 'Världscup'
    if 'sprint' in title.lower():
        competition = 'Sprint'
    elif 'stafett' in title.lower():
        competition = 'Stafett'
    elif 'jakt' in title.lower():
        competition = 'Jaktstart'
    elif 'mass' in title.lower():
        competition = 'Masstart'
    
    # Gender
    gender = ''
    if 'dam' in title.lower():
        gender = 'Damer'
    elif 'herr' in title.lower():
        gender = 'Herrar'
    
    if gender:
        competition = f"{competition} - {gender}"
    
    event = {
        'sport': program['sport'],
        'title': f"Världscupen i {location}" if location else title,
        'competition': competition,
        'channel': program['channel'],
        'date': date,
        'time': time,
        'description': title,
        'verified': True,
        'source': 'tv.nu'
    }
    
    return event

def merge_with_existing_events(tvnu_events, events_file='events.json'):
    """
    Merge tv.nu events with existing FIS/IBU events.
    
    Args:
        tvnu_events: Events scraped from tv.nu
        events_file: Path to existing events JSON
    
    Returns:
        Merged list of events
    """
    # Load existing events
    existing_events = []
    if os.path.exists(events_file):
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                existing_events = json.load(f)
        except:
            pass
    
    # Create merged list
    merged = []
    tvnu_dates = {(e['date'], e['sport']) for e in tvnu_events if e.get('date')}
    
    # Add tv.nu events (they have verified channel/time)
    merged.extend(tvnu_events)
    
    # Add existing events that don't have tv.nu data
    for event in existing_events:
        event_key = (event.get('date', ''), event.get('sport', ''))
        if event_key not in tvnu_dates and event.get('date'):
            # Keep unverified events
            event['verified'] = False
            merged.append(event)
    
    # Sort by date
    merged.sort(key=lambda x: x.get('date', ''))
    
    return merged

def update_script_js(events, output_file='script.js'):
    """
    Update script.js with new event data.
    
    Args:
        events: List of event dictionaries
        output_file: Path to script.js file
    """
    # Filter future events
    today = datetime.now().date()
    future_events = [e for e in events if e.get('date') and datetime.strptime(e['date'], '%Y-%m-%d').date() >= today]
    
    # Add IDs
    for i, event in enumerate(future_events, 1):
        event['id'] = i
        # Remove internal fields
        event.pop('verified', None)
        event.pop('source', None)
        event.pop('search_term', None)
    
    # Format as JavaScript
    js_content = "// Event data - updated from tv.nu\n"
    js_content += "const events = "
    js_content += json.dumps(future_events, indent=4, ensure_ascii=False)
    js_content += ";\n\n"
    
    # Read existing script.js to preserve rendering code
    existing_code = ""
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find where events array ends and keep everything after
            const_match = re.search(r'const events = \[.*?\];', content, re.DOTALL)
            if const_match:
                existing_code = content[const_match.end():]
            elif 'function renderSchedule' in content:
                existing_code = '\n' + content[content.index('function renderSchedule'):]
    
    if not existing_code or 'function renderSchedule' not in existing_code:
        # Add default rendering code
        existing_code = """
function renderSchedule() {
    const container = document.getElementById('schedule-container');
    const filterCC = document.getElementById('filterCrossCountry');
    const filterBiathlon = document.getElementById('filterBiathlon');
    
    container.innerHTML = '';
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const filteredEvents = events.filter(event => {
        const eventDate = new Date(event.date);
        eventDate.setHours(0, 0, 0, 0);
        
        if (eventDate < today) return false;
        
        if (event.sport === 'cross-country' && !filterCC.checked) return false;
        if (event.sport === 'biathlon' && !filterBiathlon.checked) return false;
        
        return true;
    });
    
    if (filteredEvents.length === 0) {
        container.innerHTML = '<p class="no-events">Inga kommande tävlingar</p>';
        return;
    }
    
    filteredEvents.forEach(event => {
        const card = document.createElement('div');
        card.className = 'event-card';
        
        const sportEmoji = event.sport === 'biathlon' ? '🎯' : '⛷️';
        
        card.innerHTML = `
            <div class="event-header">
                <span class="event-sport">${sportEmoji} ${event.sport === 'biathlon' ? 'Skidskytte' : 'Längdskidor'}</span>
                <span class="event-channel">${event.channel}</span>
            </div>
            <h3 class="event-title">${event.title}</h3>
            <p class="event-competition">${event.competition}</p>
            <div class="event-meta">
                <span class="event-date">${new Date(event.date).toLocaleDateString('sv-SE', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
                <span class="event-time">${event.time}</span>
            </div>
        `;
        
        container.appendChild(card);
    });
}

document.getElementById('filterCrossCountry').addEventListener('change', renderSchedule);
document.getElementById('filterBiathlon').addEventListener('change', renderSchedule);

renderSchedule();
"""
    
    # Write updated script.js
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
        f.write(existing_code)
    
    print(f"✅ Updated {output_file} with {len(future_events)} events")

def main():
    """Main execution function."""
    print("🔍 Scraping tv.nu for winter sports schedules...\n")
    
    all_programs = []
    
    # Scrape each channel
    for channel in CHANNELS:
        programs = scrape_channel_schedule(channel)
        all_programs.extend(programs)
        print()
    
    if not all_programs:
        print("❌ No winter sports programs found on tv.nu")
        print("ℹ️  This could mean:")
        print("   - No events scheduled in the near future")
        print("   - tv.nu structure has changed (script needs updating)")
        return
    
    print(f"✅ Found {len(all_programs)} total winter sports programs\n")
    
    # Convert to events
    print("📋 Processing events...")
    events = [extract_event_info(prog) for prog in all_programs]
    
    # Filter out invalid events
    valid_events = [e for e in events if e.get('date') and e.get('time')]
    print(f"✅ {len(valid_events)} events with complete date/time info\n")
    
    # Display found events
    print("📺 Verified TV schedule:")
    for event in sorted(valid_events, key=lambda x: (x['date'], x['time'])):
        sport_icon = '🎯' if event['sport'] == 'biathlon' else '⛷️'
        print(f"  {sport_icon} {event['date']} {event['time']} - {event['channel']} - {event['title']}")
    
    # Merge with existing FIS/IBU events
    print("\n🔗 Merging with existing events...")
    merged_events = merge_with_existing_events(valid_events)
    
    # Update script.js
    print("\n💾 Updating script.js...")
    update_script_js(merged_events)
    
    # Save JSON for review
    json_file = 'tvnu_events.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(valid_events, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved event data to {json_file}")
    
    print(f"\n✨ Done! {len(valid_events)} verified events from tv.nu")

if __name__ == '__main__':
    main()
