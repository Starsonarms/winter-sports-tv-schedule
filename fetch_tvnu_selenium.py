"""
Scrape tv.nu sport pages using Selenium to handle JavaScript rendering.
"""

import json
import os
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Sport category pages on tv.nu
SPORT_CATEGORIES = {
    'langdskidakning': 'cross-country',
    'skidskytte': 'biathlon',
    'alpint': 'alpine',
    'backhoppning': 'ski-jumping',
    'ishockey': 'ice-hockey',
    'konstakning': 'figure-skating',
    'hastighetsskridskoakning': 'speed-skating',
    'curling': 'curling'
}

def create_driver():
    """Create a Selenium WebDriver with headless Chrome."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Error creating Chrome driver: {e}")
        print("ℹ️  Make sure you have Chrome and chromedriver installed:")
        print("   pip install selenium")
        print("   Download chromedriver: https://chromedriver.chromium.org/")
        return None

def scrape_sport_page(driver, sport_slug, sport_type):
    """
    Scrape a single sport category page.
    
    Args:
        driver: Selenium WebDriver
        sport_slug: Sport URL slug (e.g., 'langdskidakning')
        sport_type: Sport type for categorization
    
    Returns:
        List of program dictionaries
    """
    url = f"https://www.tv.nu/sport/{sport_slug}"
    programs = []
    
    try:
        print(f"  Loading {url}...")
        driver.get(url)
        
        # Wait for content to load (wait for date/time elements)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "time"))
            )
        except TimeoutException:
            print(f"  ⚠️  Timeout waiting for content to load")
            return programs
        
        # Give extra time for JavaScript to fully render
        driver.implicitly_wait(2)
        
        # Get the page source after JavaScript rendering
        page_source = driver.page_source
        
        # Save HTML for debugging
        debug_file = f'debug_{sport_slug}.html'
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"  Debug: Saved to {debug_file}")
        
        # Parse the rendered HTML
        programs = parse_rendered_html(page_source, sport_type)
        
        print(f"  Found {len(programs)} programs")
        
    except Exception as e:
        print(f"  ❌ Error scraping {sport_slug}: {e}")
    
    return programs

def parse_rendered_html(html, sport_type):
    """
    Parse the JavaScript-rendered HTML to extract events.
    First tries to parse embedded JSON data, falls back to HTML parsing.
    
    Args:
        html: Rendered HTML content
        sport_type: Sport type for events
    
    Returns:
        List of program dictionaries
    """
    # Try to extract JSON data from __INITIAL_STATE__
    programs = parse_json_data(html, sport_type)
    
    if programs:
        print(f"  ✅ Extracted {len(programs)} events from JSON data")
        return programs
    
    # Fallback to HTML parsing if JSON extraction fails
    print(f"  ⚠️ JSON extraction failed, falling back to HTML parsing")
    return parse_html_text(html, sport_type)

def parse_json_data(html, sport_type):
    """
    Extract event data from embedded JSON in the page.
    
    Args:
        html: HTML content
        sport_type: Sport type
    
    Returns:
        List of program dictionaries, or empty list if parsing fails
    """
    try:
        # Find the __INITIAL_STATE__ JSON data
        match = re.search(r'__INITIAL_STATE__\s*=\s*"({.*?})"', html, re.DOTALL)
        if not match:
            return []
        
        json_str = match.group(1)
        # Unescape the JSON string
        json_str = json_str.replace('\\u002F', '/')
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        
        data = json.loads(json_str)
        
        # Extract sport schedule
        if 'sportPageSchedule' not in data:
            return []
        
        schedule = data['sportPageSchedule']
        programs = []
        
        for event in schedule:
            if event.get('type') != 'sport':
                continue
            
            title = event.get('title', 'Sport event')
            date_str = event.get('scheduleDate', '')
            
            # Get channel and time from broadcasts
            broadcasts = event.get('broadcasts', [])
            if not broadcasts:
                continue
            
            # Use first broadcast
            broadcast = broadcasts[0]
            channel_info = broadcast.get('channel', {})
            channel = channel_info.get('name', 'TBA')
            
            # Convert timestamp to time
            start_time = broadcast.get('startTime')
            if start_time:
                # startTime is Unix timestamp in milliseconds
                dt = datetime.fromtimestamp(start_time / 1000)
                time_str = dt.strftime('%H:%M')
                
                # If date_str is empty, get it from timestamp
                if not date_str:
                    date_str = dt.strftime('%Y-%m-%d')
            else:
                time_str = 'TBA'
            
            # Extract additional info
            subtitle = event.get('subtitle', '')
            if subtitle and subtitle not in title:
                full_title = f"{title} - {subtitle}"
            else:
                full_title = title
            
            program = {
                'title': full_title,
                'channel': channel,
                'date': date_str,
                'time': time_str,
                'sport_type': sport_type,
                'datetime': f"{date_str}T{time_str}:00"
            }
            programs.append(program)
        
        return programs
        
    except Exception as e:
        print(f"  Debug: JSON parsing error: {e}")
        return []

def parse_html_text(html, sport_type):
    """
    Fallback HTML text parsing when JSON extraction fails.
    
    Args:
        html: HTML content
        sport_type: Sport type
    
    Returns:
        List of program dictionaries
    """
    programs = []
    current_year = datetime.now().year
    
    # Month mapping
    month_map = {
        'januari': 1, 'februari': 2, 'mars': 3, 'april': 4,
        'maj': 5, 'juni': 6, 'juli': 7, 'augusti': 8,
        'september': 9, 'oktober': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'nov': 11, 'dec': 12
    }
    
    # Strategy: Find date headers ("FREDAG 21 NOVEMBER"), then find times ("11:00") after them
    # Date headers format: "FREDAG 21 NOVEMBER" or "21 nov"
    date_header_pattern = r'(?:FREDAG|LÖRDAG|SÖNDAG|MÅNDAG|TISDAG|ONSDAG|TORSDAG)\s+(\d{1,2})\s+(NOVEMBER|DECEMBER|JANUARI|FEBRUARI)'
    
    date_headers = list(re.finditer(date_header_pattern, html, re.IGNORECASE))
    print(f"  Debug: Found {len(date_headers)} date headers")
    
    # For each date header, find all times that follow it (until next date header)
    for i, date_header in enumerate(date_headers):
        day = int(date_header.group(1))
        month_str = date_header.group(2).lower()
        
        month = month_map.get(month_str)
        if not month:
            continue
        
        # Handle year wraparound
        year = current_year
        if month < datetime.now().month:
            year += 1
        
        try:
            event_date = datetime(year, month, day)
            date_str = event_date.strftime('%Y-%m-%d')
        except:
            continue
        
        # Find the section of HTML for this date (until next date header)
        section_start = date_header.end()
        if i + 1 < len(date_headers):
            section_end = date_headers[i + 1].start()
        else:
            section_end = len(html)
        
        section = html[section_start:section_end]
        
        # Find all time patterns in this section ("11:00", "10:00", etc.)
        time_pattern = r'(\d{1,2}):(\d{2})'
        time_matches = re.finditer(time_pattern, section)
        
        for time_match in time_matches:
            hour = time_match.group(1)
            minute = time_match.group(2)
            time_str = f"{hour}:{minute}"
            
            # Get context around this time (400 chars window)
            ctx_start = max(0, time_match.start() - 200)
            ctx_end = min(len(section), time_match.end() + 200)
            context = section[ctx_start:ctx_end]
            
            # Find channel
            channel = 'TBA'
            for ch in ['SVT1', 'SVT2', 'SVT Play', 'TV4', 'Viaplay', 'TV6', 'TV10', 'SVT']:
                if ch in context:
                    channel = ch
                    break
            
            # Extract title from context
            title = extract_title_from_context(context, time_match.start() - ctx_start)
            
            # Look for competition info ("Sprint", "10 km klassiskt", etc.)
            comp_patterns = [
                r'(Sprint|10 km klassiskt|10 km fri stil|Stafett|Jaktstart)',
                r'(\d+ km [^,<]+)',
            ]
            for comp_pat in comp_patterns:
                comp_match = re.search(comp_pat, context, re.IGNORECASE)
                if comp_match:
                    comp_text = comp_match.group(1)
                    if not title or len(title) < 15:
                        title = f"Längdsidåkning - {comp_text}"
                    break
            
            # Skip if no meaningful content
            if not title or len(title) < 5:
                continue
            
            program = {
                'title': title,
                'channel': channel,
                'date': date_str,
                'time': time_str,
                'sport_type': sport_type,
                'datetime': f"{date_str}T{time_str}:00"
            }
            programs.append(program)
    
    # Remove duplicates based on date+time+title
    seen = set()
    unique_programs = []
    for prog in programs:
        key = (prog['date'], prog['time'], prog['title'][:50])
        if key not in seen:
            seen.add(key)
            unique_programs.append(prog)
    
    return unique_programs

def extract_title_from_context(context, match_position):
    """
    Extract event title from surrounding context.
    
    Args:
        context: Text context around the match
        match_position: Position of the match within context
    
    Returns:
        Event title string
    """
    # Look for text before the date/time
    before_text = context[:match_position]
    
    # Common patterns for titles
    title_patterns = [
        r'<h\d[^>]*>([^<]+)</h\d>',  # Heading tags
        r'title["\']>([^<]+)<',       # title attribute
        r'>([A-ZÅÄÖ][^<]{10,100})<', # Capitalized text
    ]
    
    for pattern in title_patterns:
        matches = re.findall(pattern, before_text[-300:])
        if matches:
            title = matches[-1].strip()
            # Clean up
            title = re.sub(r'\s+', ' ', title)
            if len(title) > 10 and 'längdskidåkning' in title.lower() or 'skidskytte' in title.lower():
                return title
    
    # Fallback: look for location names
    locations = ['Gällivare', 'Ruka', 'Trondheim', 'Davos', 'Falun', 'Lillehammer']
    for location in locations:
        if location in context:
            return f"Längdskidåkning, {location}"
    
    return "Längdskidåkning"

def merge_with_calendar_events(tvnu_events, calendar_file='events.json'):
    """
    Merge tv.nu verified events with FIS/IBU calendar events.
    """
    calendar_events = []
    if os.path.exists(calendar_file):
        try:
            with open(calendar_file, 'r', encoding='utf-8') as f:
                calendar_events = json.load(f)
            print(f"  Loaded {len(calendar_events)} events from FIS/IBU calendar")
        except:
            pass
    
    # Create a set of verified event dates+sports
    verified_keys = {(e['date'], e['sport_type']) for e in tvnu_events}
    
    # Start with verified tv.nu events
    merged = []
    for event in tvnu_events:
        merged.append({
            'sport': event['sport_type'],
            'title': event['title'],
            'competition': extract_competition(event['title']),
            'channel': event['channel'],
            'date': event['date'],
            'time': event['time'],
            'description': event['title'],
            'verified': True
        })
    
    # Add calendar events that don't have TV verification yet
    for cal_event in calendar_events:
        event_key = (cal_event.get('date'), cal_event.get('sport'))
        if event_key not in verified_keys:
            merged.append(cal_event)
    
    return merged

def extract_competition(title):
    """Extract competition type from title."""
    title_lower = title.lower()
    
    if 'sprint' in title_lower:
        comp = 'Sprint'
    elif 'stafett' in title_lower:
        comp = 'Stafett'
    elif 'jaktstart' in title_lower or 'jakt' in title_lower:
        comp = 'Jaktstart'
    elif 'masstart' in title_lower or 'mass' in title_lower:
        comp = 'Masstart'
    elif 'skiathlon' in title_lower or 'skiatlon' in title_lower:
        comp = 'Skiatlon'
    elif 'klassiskt' in title_lower:
        comp = 'Klassiskt'
    elif 'fri stil' in title_lower or 'fristil' in title_lower:
        comp = 'Fristil'
    else:
        comp = 'Världscup'
    
    # Add gender if found
    if 'dam' in title_lower:
        comp += ' - Damer'
    elif 'herr' in title_lower:
        comp += ' - Herrar'
    
    return comp

def update_script_js(events, output_file='script.js'):
    """Update script.js with event data."""
    # Sort and add IDs
    def sort_key(event):
        date = event.get('date', '')
        time = event.get('time', '')
        if time == 'TBA':
            time = '99:99'
        return (date, time)
    
    events.sort(key=sort_key)
    for i, event in enumerate(events, 1):
        event['id'] = i
        event.pop('verified', None)
    
    # Format as JavaScript
    js_content = "// Event data - updated from tv.nu (Selenium)\n"
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
    
    if existing_code:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
            f.write(existing_code)
        print(f"✅ Updated {output_file} with {len(events)} events")
    else:
        print("⚠️  Could not find rendering code in script.js")

def main():
    """Main execution."""
    print("🔍 Scraping tv.nu with Selenium (JavaScript rendering)...\n")
    
    # Create Selenium driver
    driver = create_driver()
    if not driver:
        return
    
    try:
        all_programs = []
        
        # Scrape each sport category
        for sport_slug, sport_type in SPORT_CATEGORIES.items():
            print(f"🏅 Scraping {sport_slug}...")
            programs = scrape_sport_page(driver, sport_slug, sport_type)
            all_programs.extend(programs)
        
        print()
        
        if not all_programs:
            print("⚠️  No winter sports programs found on tv.nu")
            print("ℹ️  This might mean no events are scheduled yet\n")
        else:
            print(f"✅ Found {len(all_programs)} verified events from tv.nu\n")
        
        # Merge with calendar
        print("🔗 Merging with FIS/IBU calendar...")
        all_events = merge_with_calendar_events(all_programs)
        
        if not all_events:
            print("❌ No events available")
            return
        
        print(f"✅ Total: {len(all_events)} events ({len(all_programs)} verified, {len(all_events) - len(all_programs)} from calendar)\n")
        
        # Display
        sport_icons = {
            'cross-country': '⛷️', 'biathlon': '🎯', 'alpine': '🎿',
            'ski-jumping': '🪂', 'ice-hockey': '🏒', 'figure-skating': '⛸️',
            'speed-skating': '⏱️', 'curling': '🥌', 'other': '🏆'
        }
        
        print("📺 Combined schedule:")
        for event in all_events[:20]:  # Show first 20
            icon = sport_icons.get(event['sport'], '🏆')
            channel = event.get('channel', 'TBA')
            time = event.get('time', 'TBA')
            verified = '✅' if event.get('verified') else '📅'
            print(f"  {verified} {icon} {event['date']} {time:5} - {channel:8} - {event['title'][:60]}")
        
        if len(all_events) > 20:
            print(f"  ... and {len(all_events) - 20} more events")
        
        # Save
        json_file = 'tvnu_events_selenium.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_events, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved to {json_file}")
        
        # Update script.js
        update_script_js(all_events)
        
        print(f"\n✨ Done! {len(all_events)} total events")
        print(f"   ✅ {len(all_programs)} verified from TV schedules")
        print(f"   📅 {len(all_events) - len(all_programs)} from calendar (TBA)")
        
    finally:
        # Always close the driver
        driver.quit()
        print("\n🔒 Browser closed")

if __name__ == '__main__':
    main()
