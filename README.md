# Winter Sports TV Schedule

A webpage to track all Winter Olympic sports on Swedish TV channels, including the 2026 Milano-Cortina Winter Olympics.

## Features

- **All Winter Olympic Sports**: Längdskidor, Skidskytte, Alpint, Backhoppning, Ishockey, Konståkning, Skridsko, Curling, and more
- **Smart Filtering**: Toggle individual sports on/off
- **Verified TV Schedules**: Automatic scraping from tv.nu for accurate channel and times
- Shows channel, date, time, and competition details
- Responsive design for mobile and desktop
- Automatically fetches real events from FIS/IBU and tv.nu

## Sports Supported

All Winter Olympic sports:
- ⛷️ **Längdskidor** (Cross-Country Skiing)
- 🎯 **Skidskytte** (Biathlon)
- 🎿 **Alpint** (Alpine Skiing) - Slalom, Storslalom, Super-G, Störtlopp
- 🪂 **Backhoppning** (Ski Jumping)
- 🏒 **Ishockey** (Ice Hockey)
- ⛸️ **Konståkning** (Figure Skating)
- ⏱️ **Skridsko** (Speed Skating & Short Track)
- 🥌 **Curling**
- 🏆 **Övrigt** (Freestyle, Snowboard, Nordic Combined, Bobsleigh, Skeleton, Luge)

## Channels Supported

Primarily focuses on free Swedish TV:
- **SVT1, SVT2** - Main winter sports channels
- **TV4** - Additional coverage

## Usage

1. Open `index.html` in your browser
2. Use the checkboxes to filter by sport type
3. View upcoming competitions with their broadcast details

## Configuring Default Filters

You can customize which sports are selected by default when the page loads.

Edit `index.html` and set `data-default="true"` or `data-default="false"` on each filter checkbox:

```html
<!-- Selected by default -->
<input type="checkbox" id="filterCrossCountry" data-default="true">

<!-- Not selected by default -->
<input type="checkbox" id="filterIceHockey" data-default="false">
```

**Current defaults:**
- ✅ Längdskidor (Cross-Country)
- ✅ Skidskytte (Biathlon)
- ❌ Alpint
- ❌ Backhoppning
- ❌ Ishockey
- ❌ Konståkning
- ❌ Skridsko
- ❌ Curling
- ❌ Övrigt

Users can still toggle any filter on/off manually - these settings only control the initial state.

## Updating Events

### Automated Method (Recommended)

**Option 1: Get verified TV schedules from tv.nu (Best)**

```bash
python fetch_tvnu_simple.py
```

This will:
- Scrape SVT1, SVT2, and TV4 schedules from tv.nu
- Extract ALL winter sports programs for the next 21 days
- Automatically categorize by sport type
- Update `script.js` with verified channels and times
- No API key required!

**Option 2: Get World Cup calendar (FIS/IBU only)**

```bash
python parse_events_combined.py
```

This will:
- Fetch all Cross-Country World Cup events from FIS
- Fetch all Biathlon World Cup events from IBU
- Generate events with estimated TV channels (mostly SVT2)
- Update `script.js` automatically

**Recommended Workflow:**

```bash
# Step 1: Get the official competition calendar
python parse_events_combined.py
# This creates events.json with all FIS/IBU events marked as channel="TBA", time="TBA"

# Step 2: Get verified TV schedules
python fetch_tvnu_simple.py
# This merges tv.nu data with calendar events:
# - Verified events (from TV): show actual channel & time
# - Calendar events (no TV yet): show "TBA" for channel & time
```

**How it works:**
- FIS/IBU script creates a calendar of all World Cup events with "TBA" for unconfirmed broadcasts
- tv.nu scraper finds actual TV broadcasts and marks them as verified
- Events are merged: verified TV data takes precedence over calendar placeholders
- You get both: confirmed broadcasts AND upcoming events not yet scheduled on TV

### Manual Method

Edit the `events` array in `script.js`:

```javascript
{
    id: 7,
    sport: 'cross-country',  // or 'biathlon'
    title: 'Event Name',
    competition: 'Competition Type',
    channel: 'SVT1',
    date: '2025-12-15',  // YYYY-MM-DD format
    time: '14:00',       // HH:MM format
    description: 'Optional description'
}
```

## Verifying TV Channels

1. Visit [tv.nu](https://tv.nu)
2. Search for "längdskidor", "skidskytte", or specific event locations
3. Check which channels are broadcasting
4. Update `script.js` with correct channels and times

## Data Sources

- **TV Schedules**: [tv.nu](https://tv.nu) - Automatically scraped for all winter sports
- **Cross-Country Events**: [FIS Cross-Country Calendar](https://data.fis-ski.com/services/public/icalendar-feed-fis-events.html?seasoncode=2026&sectorcode=CC&categorycode=WC)
- **Biathlon Events**: [IBU Biathlon API](https://biathlonresults.com/modules/sportapi/api/Events?SeasonId=2526&Level=1)

## Current Status

✅ All Winter Olympic sports supported
✅ Automatic TV schedule scraping from tv.nu
✅ Ready for 2026 Milano-Cortina Winter Olympics
✅ FIS/IBU World Cup event calendar integration

## Automation (Nightly Updates)

Set up automatic nightly updates to keep your schedule current:

### Quick Setup:

**Right-click** `setup_scheduled_task.ps1` → **Run with PowerShell** (as Administrator)

This will:
- Create a Windows scheduled task
- Run every night at 2:00 AM
- Automatically fetch and update events
- Log all updates to `update_log.txt`

### Manual Setup:

See [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) for detailed instructions.

### Testing:

Test the update manually:
```bash
python update_events_auto.py
```

Or run the batch file:
```bash
.\update_events.bat
```

## Future Enhancements

- Integrate with tv.nu API for real-time channel data
- Add notifications for upcoming events
- Export to calendar (iCal format)
- Add more winter sports (alpine skiing, ski jumping, etc.)
- Email notifications when schedule changes
