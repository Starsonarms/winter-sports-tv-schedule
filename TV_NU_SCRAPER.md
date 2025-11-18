# TV.nu Scraper

This script automatically fetches **all Winter Olympic sports** schedules from tv.nu for SVT1, SVT2, and TV4.

## Usage

Run the scraper to update your schedule:

```bash
python fetch_tvnu_simple.py
```

This will:
1. Check SVT1, SVT2, and TV4 schedules for the next 21 days
2. Extract ALL winter sports programs (all Olympic sports)
3. Automatically categorize by sport type
4. Update `script.js` with verified channel and time information
5. Save a backup JSON file to `tvnu_events.json`

## How It Works

The scraper:
- Visits each channel page on tv.nu (e.g., `https://www.tv.nu/kanal/svt1`)
- Extracts structured data (JSON-LD) from the HTML
- Filters for **ALL winter sports keywords** (see below)
- Automatically categorizes into 9 sport categories
- Updates your website with verified broadcast times

## Sport Categories

The scraper recognizes and categorizes:
1. **Längdskidor** (Cross-Country Skiing)
2. **Skidskytte** (Biathlon)
3. **Alpint** (Alpine Skiing) - Slalom, Super-G, Störtlopp, etc.
4. **Backhoppning** (Ski Jumping)
5. **Ishockey** (Ice Hockey)
6. **Konståkning** (Figure Skating)
7. **Skridsko** (Speed Skating & Short Track)
8. **Curling**
9. **Övrigt** (Freestyle, Snowboard, Nordic Combined, Bob, Skeleton, Luge)

## Keywords

The scraper looks for these keywords in program titles:
- **Cross-country**: längdskidor, längd, cross-country
- **Biathlon**: skidskytte, biathlon
- **Alpine**: alpint, alpine, slalom, storslalom, super-g, störtlopp, downhill
- **Ski Jumping**: backhoppning, backhoppare, ski jumping, skidflygning
- **Ice Hockey**: ishockey, hockey, ice hockey
- **Figure Skating**: konståkning, figure skating
- **Speed Skating**: skridsko, skridskor, speed skating, short track
- **Curling**: curling
- **Freestyle/Snowboard**: freestyle, snowboard, slopestyle, halfpipe, big air
- **Other**: nordisk kombination, bob, bobsleigh, skeleton, rodel, luge
- **General**: världscup, world cup, vm, world championship, os, olympi
- **Locations**: ruka, trondheim, davos, falun, lillehammer, oslo, kitzbühel, wengen, cortina, Åre, etc.

## Automation

Add this to your existing scheduled task or cron job:

### Windows Task Scheduler
```powershell
python C:\Users\cpa\projects\winter-sports-tv-schedule\fetch_tvnu_simple.py
```

### Combined with FIS/IBU Data
Run both scripts to get complete coverage:
```powershell
# Get event calendar from FIS/IBU
python parse_events_combined.py

# Get actual TV schedule from tv.nu  
python fetch_tvnu_simple.py
```

The tv.nu data will override estimated channels/times from the FIS/IBU script with verified broadcast information.

## Output

The script generates:
- `script.js` - Updated with verified events
- `tvnu_events.json` - Backup of scraped data for review

## Troubleshooting

**No programs found:**
- Check if winter sports season has started (usually late November)
- Verify tv.nu is accessible
- Check if tv.nu HTML structure has changed

**Wrong data:**
- Keywords might need adjustment if program titles change
- Check `tvnu_events.json` to see raw scraped data

## Notes

- The scraper respects tv.nu's structure and only reads public data
- No API key required
- Runs independently of FIS/IBU data
- Can be run as often as needed (recommended: once daily)
