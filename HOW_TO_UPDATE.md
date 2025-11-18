# How to Update with Real Event Data

## Finding Cross-Country Skiing Events

1. **Visit FIS Calendar**
   - Go to: https://www.fis-ski.com/DB/general/calendar-results.html
   - Select filters:
     - Discipline: Cross-Country
     - Season: 2026
     - Date range: Current season
   - Look for World Cup events

2. **Common Cross-Country Events to Watch**
   - Ruka Opening (Finland) - Late November
   - Lillehammer (Norway) - Early December
   - Davos (Switzerland) - Mid December
   - Tour de Ski - Late December/Early January
   - Falun (Sweden) - January
   - Lahti (Finland) - February
   - World Championships/Olympics - February/March

## Finding Biathlon Events

1. **Visit FIS Biathlon Calendar**
   - Go to: https://www.fis-ski.com/en/biathlon
   - Or: https://www.biathlonworld.com/calendar
   - Look for World Cup events

2. **Common Biathlon Events**
   - Kontiolahti (Finland) - Late November
   - Hochfilzen (Austria) - December
   - Oberhof (Germany) - January
   - Ruhpolding (Germany) - January
   - Antholz-Anterselva (Italy) - January
   - World Championships - February/March

## Checking Swedish TV Channels

### Method 1: TV.nu Direct Search
1. Go to: https://tv.nu
2. Use search box at top
3. Search for event names like:
   - "skidskytte"
   - "längdskidor"
   - "världscupen"
   - "biathlon"
   - Specific location names (e.g., "Ruka", "Lillehammer")

### Method 2: Check Specific Channel Pages
- **SVT Sport**: https://www.svt.se/sport/
- **TV4 Sport**: https://www.tv4.se/sport
- **TV6**: Often shows biathlon and cross-country
- **Eurosport** (via Discovery+)

### Method 3: Sports Schedule on TV.nu
1. Go to: https://tv.nu/sport
2. Browse by date
3. Filter by sport type if available

## Updating the Website

### Option 1: Edit JavaScript Directly
Edit `script.js` and update the `events` array:

```javascript
{
    id: 1,
    sport: 'cross-country',  // or 'biathlon'
    title: 'Event Name',
    competition: 'Race Type',
    channel: 'SVT2',
    date: '2025-12-01',  // YYYY-MM-DD
    time: '14:00',       // HH:MM (Swedish time)
    description: 'Optional info'
}
```

### Option 2: Use Python Script
1. Edit `fetch_events.py`
2. Add events using `add_event()` function
3. Run: `python fetch_events.py`
4. Uncomment `export_to_js()` to update script.js

## Swedish TV Channels Most Likely to Show Winter Sports

### Primary Channels
- **SVT1, SVT2** - National broadcaster, shows most World Cup events
- **SVT Play** - Streams many events online
- **TV4** - Sometimes has rights to specific competitions
- **TV6** - Often shows winter sports

### Less Common
- **Eurosport/Discovery+** - May have some events
- **TV10, TV12** - Occasionally show winter sports

## Tips

- World Cup events are usually on weekends
- Sprint events are typically shorter (1-2 hours)
- Distance races can be 2-4 hours
- Relay events are usually on Sundays
- Check SVT's sports schedule 1-2 weeks in advance for best accuracy
- Swedish channels prioritize events with Swedish athletes

## Automation Ideas (Future)

To fully automate this, you would need:
1. Selenium/Playwright to scrape JavaScript-rendered pages
2. FIS API access (if available)
3. TV.nu API or EPG (Electronic Program Guide) data
4. Schedule the script to run weekly

Example with Selenium:
```python
from selenium import webdriver
# Navigate to FIS calendar
# Extract event data
# Cross-reference with TV.nu
# Update events array
```
