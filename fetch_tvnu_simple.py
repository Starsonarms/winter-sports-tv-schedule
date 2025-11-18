"""
Simple scraper to fetch winter sports from tv.nu channel pages.
"""

import json
import os
import re
from datetime import datetime, timedelta
from urllib.request import urlopen, Request

# Channels to check
CHANNELS = {
    'svt1': 'SVT1',
    'svt2': 'SVT2',
    'tv4': 'TV4'
}

# Sport category pages on tv.nu
SPORT_CATEGORIES = [
    'langdskidakning',  # Cross-country skiing
    'skidskytte',       # Biathlon
    'alpint',           # Alpine skiing
    'backhoppning',     # Ski jumping
    'ishockey',         # Ice hockey
    'konstakning',      # Figure skating
    'hastighetsskridskoakning',  # Speed skating
    'curling'
]

# Keywords for winter sports (all Winter Olympic sports)
WINTER_SPORTS_KEYWORDS = [
    # Cross-country skiing
    'längdskidor', 'längdsidåkning', 'längd', 'cross-country',
    # Biathlon
    'skidskytte', 'biathlon',
    # Alpine skiing  
    'alpint', 'alpine', 'slalom', 'storslalom', 'super-g', 'störtlopp', 'downhill',
    # Ski jumping
    'backhoppning', 'backhoppare', 'ski jumping', 'skidflygning',
    # Ice hockey
    'ishockey', 'hockey', 'ice hockey',
    # Figure skating
    'konståkning', 'figure skating',
    # Speed skating
    'skridsko', 'skridskor', 'speed skating', 'short track',
    # Curling
    'curling',
    # Freestyle & Snowboard
    'freestyle', 'snowboard', 'slopestyle', 'halfpipe', 'big air',
    # Nordic combined
    'nordisk kombination', 'nordic combined',
    # Bobsleigh, Skeleton, Luge
    'bob', 'bobsleigh', 'skeleton', 'rodel', 'luge',
    # General
    'världscup', 'world cup', 'vm', 'world championship', 'os', 'olympi',
    # Locations
    'ruka', 'trondheim', 'davos', 'falun', 'lillehammer', 'oslo', 'drammen',
    'kitzbühel', 'wengen', 'cortina', 'are', 'schladming', 'val gardena',
    'tour de ski'
]

def fetch_sport_category_page(sport_slug):
    """
    Fetch sport category page from tv.nu (e.g., tv.nu/sport/langdskidakning).
    
    Args:
        sport_slug: Sport category slug (e.g., 'langdskidakning')
    
    Returns:
        HTML content
    """
    url = f"https://www.tv.nu/sport/{sport_slug}"
    
    try:
        request = Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urlopen(request, timeout=15) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"  Error fetching sport page {sport_slug}: {e}")
        return None

def fetch_channel_page(channel_slug, date=None):
    """
    Fetch channel schedule page from tv.nu.
    
    Args:
        channel_slug: Channel slug (e.g., 'svt1')
        date: Date string YYYY-MM-DD (defaults to today)
    
    Returns:
        HTML content
    """
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    url = f"https://www.tv.nu/kanal/{channel_slug}"
    
    try:
        request = Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urlopen(request, timeout=15) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"  Error fetching {channel_slug} for {date}: {e}")
        return None

def extract_programs_from_sport_page(html):
    """
    Extract program information from tv.nu sport category page HTML.
    
    Args:
        html: HTML content from sport page
    
    Returns:
        List of programs
    """
    programs = []
    
    # Look for date patterns like "21 nov" followed by time and channel
    # Pattern: "21 nov 11:00" ... "SVT1" or "Viaplay"
    date_time_pattern = r'(\d{1,2})\s+(nov|dec|jan|feb|mar|apr)\s+(\d{1,2}:\d{2})'
    matches = re.finditer(date_time_pattern, html, re.IGNORECASE)
    
    current_year = datetime.now().year
    month_map = {
        'nov': 11, 'dec': 12, 'jan': 1, 'feb': 2, 
        'mar': 3, 'apr': 4, 'maj': 5, 'jun': 6
    }
    
    for match in matches:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        time_str = match.group(3)
        month = month_map.get(month_str, 11)
        
        # Handle year wraparound
        year = current_year
        if month < datetime.now().month - 1:
            year += 1
        
        try:
            event_date = datetime(year, month, day)
            date_str = event_date.strftime('%Y-%m-%d')
        except:
            continue
        
        # Look for channel info near this time (within 200 chars)
        pos = match.end()
        context = html[pos:pos+200]
        
        # Find channel
        channel = 'TBA'
        for ch in ['SVT1', 'SVT2', 'SVT24', 'SVT Play', 'TV4', 'Viaplay']:
            if ch in context:
                channel = ch
                break
        
        # Look for title/description before the date
        title_context = html[max(0, match.start()-300):match.start()]
        title_pattern = r'>([^<]{10,100})</'
        title_matches = re.findall(title_pattern, title_context)
        title = title_matches[-1].strip() if title_matches else f"Event {date_str}"
        
        program = {
            'title': title,
            'channel': channel,
            'date': date_str,
            'time': time_str,
            'datetime': f"{date_str}T{time_str}:00"
        }
        programs.append(program)
    
    return programs

def extract_programs_from_html(html, channel_name):
    """
    Extract program information from tv.nu HTML.
    
    Args:
        html: HTML content
        channel_name: Channel name for tagging
    
    Returns:
        List of programs
    """
    programs = []
    
    # Look for JSON-LD structured data
    json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    json_matches = re.findall(json_ld_pattern, html, re.DOTALL | re.IGNORECASE)
    
    for json_str in json_matches:
        try:
            data = json.loads(json_str)
            
            # Handle both single objects and arrays
            items = [data] if isinstance(data, dict) else data if isinstance(data, list) else []
            
            for item in items:
                if item.get('@type') in ['TVEpisode', 'BroadcastEvent']:
                    name = item.get('name', '')
                    start_date = item.get('startDate', '')
                    
                    if not name or not start_date:
                        continue
                    
                    # Check if it's a winter sports program
                    name_lower = name.lower()
                    if not any(kw in name_lower for kw in WINTER_SPORTS_KEYWORDS):
                        continue
                    
                    try:
                        dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except:
                        continue
                    
                    program = {
                        'title': name,
                        'channel': channel_name,
                        'date': dt.strftime('%Y-%m-%d'),
                        'time': dt.strftime('%H:%M'),
                        'datetime': start_date
                    }
                    programs.append(program)
        except json.JSONDecodeError:
            continue
        except Exception:
            continue
    
    return programs

def scrape_winter_sports_from_sport_pages():
    """
    Scrape winter sports programs from tv.nu sport category pages.
    
    Returns:
        List of all winter sports programs
    """
    all_programs = []
    
    print(f"🔍 Scraping winter sports from tv.nu sport pages...\n")
    
    sport_map = {
        'langdskidakning': 'cross-country',
        'skidskytte': 'biathlon',
        'alpint': 'alpine',
        'backhoppning': 'ski-jumping',
        'ishockey': 'ice-hockey',
        'konstakning': 'figure-skating',
        'hastighetsskridskoakning': 'speed-skating',
        'curling': 'curling'
    }
    
    for sport_slug in SPORT_CATEGORIES:
        print(f"🏅 Checking {sport_slug}...")
        
        html = fetch_sport_category_page(sport_slug)
        if not html:
            print(f"  Could not fetch {sport_slug}")
            continue
        
        # Extract programs using sport page parser
        programs = extract_programs_from_sport_page(html)
        
        # Tag with sport type
        sport_type = sport_map.get(sport_slug, 'other')
        for prog in programs:
            prog['sport_type'] = sport_type
        
        print(f"  Found {len(programs)} programs")
        all_programs.extend(programs)
    
    print()
    return all_programs

def categorize_programs(programs):
    """
    Categorize programs into different Winter Olympic sports.
    
    Args:
        programs: List of program dicts
    
    Returns:
        List of categorized events
    """
    events = []
    
    for prog in programs:
        title_lower = prog['title'].lower()
        
        # Use pre-tagged sport_type if available (from sport category pages)
        if 'sport_type' in prog:
            sport = prog['sport_type']
        # Otherwise determine from title keywords
        elif any(kw in title_lower for kw in ['skidskytte', 'biathlon']):
            sport = 'biathlon'
        elif any(kw in title_lower for kw in ['alpint', 'alpine', 'slalom', 'storslalom', 'super-g', 'störtlopp', 'downhill']):
            sport = 'alpine'
        elif any(kw in title_lower for kw in ['backhoppning', 'backhoppare', 'ski jumping', 'skidflygning']):
            sport = 'ski-jumping'
        elif any(kw in title_lower for kw in ['ishockey', 'hockey']):
            sport = 'ice-hockey'
        elif any(kw in title_lower for kw in ['konståkning', 'figure skating']):
            sport = 'figure-skating'
        elif any(kw in title_lower for kw in ['skridsko', 'skridskor', 'speed skating', 'short track']):
            sport = 'speed-skating'
        elif any(kw in title_lower for kw in ['curling']):
            sport = 'curling'
        elif any(kw in title_lower for kw in ['freestyle', 'snowboard', 'slopestyle', 'halfpipe', 'big air']):
            sport = 'other'
        elif any(kw in title_lower for kw in ['nordisk kombination', 'nordic combined']):
            sport = 'other'
        elif any(kw in title_lower for kw in ['bob', 'bobsleigh', 'skeleton', 'rodel', 'luge']):
            sport = 'other'
        elif any(kw in title_lower for kw in ['längdskidor', 'längdsidåkning', 'längd', 'cross-country']):
            sport = 'cross-country'
        else:
            sport = 'other'
        
        # Extract location
        location_match = re.search(r'(?:i|från)\s+([A-ZÅÄÖ][a-zåäö]+)', prog['title'])
        location = location_match.group(1) if location_match else ''
        
        # Extract competition type
        competition = 'Världscup'
        if 'sprint' in title_lower:
            competition = 'Sprint'
        elif 'stafett' in title_lower:
            competition = 'Stafett'
        elif 'jakt' in title_lower:
            competition = 'Jaktstart'
        elif 'mass' in title_lower:
            competition = 'Masstart'
        elif 'skiatlon' in title_lower:
            competition = 'Skiatlon'
        
        # Gender
        if 'dam' in title_lower:
            competition += ' - Damer'
        elif 'herr' in title_lower:
            competition += ' - Herrar'
        
        event = {
            'sport': sport,
            'title': f"Världscupen i {location}" if location else prog['title'],
            'competition': competition,
            'channel': prog['channel'],
            'date': prog['date'],
            'time': prog['time'],
            'description': prog['title'],
            'verified': True  # Mark as verified since it's from actual TV schedule
        }
        events.append(event)
    
    return events

def merge_with_calendar_events(tvnu_events, calendar_file='events.json'):
    """
    Merge tv.nu verified events with FIS/IBU calendar events.
    
    Args:
        tvnu_events: Verified events from tv.nu
        calendar_file: JSON file with FIS/IBU calendar events
    
    Returns:
        Combined list with verified events taking precedence
    """
    # Load calendar events if they exist
    calendar_events = []
    if os.path.exists(calendar_file):
        try:
            with open(calendar_file, 'r', encoding='utf-8') as f:
                calendar_events = json.load(f)
            print(f"  Loaded {len(calendar_events)} events from FIS/IBU calendar")
        except:
            pass
    
    # Create a set of verified event dates+sports for quick lookup
    verified_keys = {(e['date'], e['sport']) for e in tvnu_events}
    
    # Start with verified tv.nu events
    merged = list(tvnu_events)
    
    # Add calendar events that don't have TV verification yet
    for cal_event in calendar_events:
        event_key = (cal_event.get('date'), cal_event.get('sport'))
        
        # Skip if we already have verified TV data for this date+sport
        if event_key in verified_keys:
            continue
        
        # Add calendar event (these are marked with TBA)
        merged.append(cal_event)
    
    return merged

def update_script_js(events, output_file='script.js'):
    """
    Update script.js with event data.
    """
    # Sort and add IDs
    # TBA times should sort to end of day
    def sort_key(event):
        date = event.get('date', '')
        time = event.get('time', '')
        # Put TBA at end of each day
        if time == 'TBA':
            time = '99:99'
        return (date, time)
    
    events.sort(key=sort_key)
    for i, event in enumerate(events, 1):
        event['id'] = i
        # Remove internal 'verified' field before writing to JS
        event.pop('verified', None)
    
    # Format as JavaScript
    js_content = "// Event data - updated from tv.nu\n"
    js_content += "const events = "
    js_content += json.dumps(events, indent=4, ensure_ascii=False)
    js_content += ";\n\n"
    
    # Preserve existing rendering code
    existing_code = ""
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            const_match = re.search(r'const events = \[.*?\];', content, re.DOTALL)
            if const_match:
                existing_code = content[const_match.end():]
            elif 'function renderSchedule' in content:
                existing_code = '\n' + content[content.index('function renderSchedule'):]
    
    if not existing_code or 'function renderSchedule' not in existing_code:
        existing_code = """
// Sport display configuration
const sportConfig = {
    'cross-country': { emoji: '⛷️', name: 'Längdskidor' },
    'biathlon': { emoji: '🎯', name: 'Skidskytte' },
    'alpine': { emoji: '🎿', name: 'Alpint' },
    'ski-jumping': { emoji: '🪂', name: 'Backhoppning' },
    'ice-hockey': { emoji: '🏒', name: 'Ishockey' },
    'figure-skating': { emoji: '⛸️', name: 'Konståkning' },
    'speed-skating': { emoji: '⏱️', name: 'Skridsko' },
    'curling': { emoji: '🥌', name: 'Curling' },
    'other': { emoji: '🏆', name: 'Övrigt' }
};

function renderSchedule() {
    const container = document.getElementById('schedule-container');
    const filters = {
        'cross-country': document.getElementById('filterCrossCountry'),
        'biathlon': document.getElementById('filterBiathlon'),
        'alpine': document.getElementById('filterAlpine'),
        'ski-jumping': document.getElementById('filterSkiJumping'),
        'ice-hockey': document.getElementById('filterIceHockey'),
        'figure-skating': document.getElementById('filterFigureSkating'),
        'speed-skating': document.getElementById('filterSpeedSkating'),
        'curling': document.getElementById('filterCurling'),
        'other': document.getElementById('filterOther')
    };
    
    container.innerHTML = '';
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const filteredEvents = events.filter(event => {
        const eventDate = new Date(event.date);
        eventDate.setHours(0, 0, 0, 0);
        
        if (eventDate < today) return false;
        
        // Check if sport filter is active
        const filter = filters[event.sport];
        if (filter && !filter.checked) return false;
        
        return true;
    });
    
    if (filteredEvents.length === 0) {
        container.innerHTML = '<p class="no-events">Inga kommande tävlingar</p>';
        return;
    }
    
    filteredEvents.forEach(event => {
        const card = document.createElement('div');
        card.className = 'event-card';
        
        const config = sportConfig[event.sport] || sportConfig['other'];
        
        card.innerHTML = `
            <div class="event-header">
                <span class="event-sport">${config.emoji} ${config.name}</span>
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

// Add event listeners for all filters
document.getElementById('filterCrossCountry').addEventListener('change', renderSchedule);
document.getElementById('filterBiathlon').addEventListener('change', renderSchedule);
document.getElementById('filterAlpine').addEventListener('change', renderSchedule);
document.getElementById('filterSkiJumping').addEventListener('change', renderSchedule);
document.getElementById('filterIceHockey').addEventListener('change', renderSchedule);
document.getElementById('filterFigureSkating').addEventListener('change', renderSchedule);
document.getElementById('filterSpeedSkating').addEventListener('change', renderSchedule);
document.getElementById('filterCurling').addEventListener('change', renderSchedule);
document.getElementById('filterOther').addEventListener('change', renderSchedule);

renderSchedule();
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
        f.write(existing_code)
    
    print(f"✅ Updated {output_file} with {len(events)} events\n")

def main():
    """Main execution."""
    # Scrape programs from sport category pages
    programs = scrape_winter_sports_from_sport_pages()
    
    # Categorize tv.nu events
    tvnu_events = categorize_programs(programs) if programs else []
    
    if tvnu_events:
        print(f"✅ Found {len(tvnu_events)} verified events from tv.nu\n")
    else:
        print("⚠️  No winter sports programs found on tv.nu")
        print("ℹ️  This might mean no events are scheduled yet, or tv.nu structure has changed\n")
    
    # Merge with FIS/IBU calendar events
    print("🔗 Merging with FIS/IBU calendar...")
    all_events = merge_with_calendar_events(tvnu_events)
    
    if not all_events:
        print("❌ No events available")
        return
    
    print(f"✅ Total: {len(all_events)} events ({len(tvnu_events)} verified, {len(all_events) - len(tvnu_events)} from calendar)\n")
    
    # Display
    sport_icons = {
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
    
    print("📺 Combined schedule:")
    for event in sorted(all_events, key=lambda x: (x.get('date', ''), x.get('time', '') if x.get('time') != 'TBA' else 'ZZZ')):
        icon = sport_icons.get(event['sport'], '🏆')
        channel = event.get('channel', 'TBA')
        time = event.get('time', 'TBA')
        verified_marker = '✅' if event.get('verified') else '📅'
        print(f"  {verified_marker} {icon} {event['date']} {time:5} - {channel:4} - {event['title']}")
    
    # Save
    json_file = 'tvnu_events.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_events, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved to {json_file}")
    
    # Update script.js
    update_script_js(all_events)
    
    print(f"\n✨ Done! {len(all_events)} total events")
    print(f"   ✅ {len(tvnu_events)} verified from TV schedules")
    print(f"   📅 {len(all_events) - len(tvnu_events)} from calendar (TBA)")

if __name__ == '__main__':
    main()
