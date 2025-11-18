# Selenium Setup Guide

The Selenium-based scraper can extract JavaScript-rendered content from tv.nu sport pages to get accurate TV schedules.

## Installation

### Step 1: Install Selenium

```bash
pip install selenium
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Install Chrome Browser

Make sure you have Google Chrome installed. Download from: https://www.google.com/chrome/

### Step 3: Install ChromeDriver

**Option A: Automatic (Recommended for Chrome 115+)**

Chrome 115+ includes automatic ChromeDriver management. Just run the script - it should work!

**Option B: Manual Install**

1. Check your Chrome version: Chrome menu → Help → About Google Chrome
2. Download matching ChromeDriver: https://chromedriver.chromium.org/downloads
3. Extract `chromedriver.exe` to one of:
   - Same folder as script: `C:\Users\cpa\projects\winter-sports-tv-schedule\`
   - Or add to PATH: `C:\Windows\System32\`

## Usage

### Run the Selenium Scraper

```bash
python fetch_tvnu_selenium.py
```

This will:
1. 🔍 Open Chrome in headless mode (invisible)
2. 📺 Visit each sport category page on tv.nu
3. ⏱️ Wait for JavaScript to render the content
4. 📋 Extract all upcoming events with verified channels and times
5. 🔗 Merge with FIS/IBU calendar events
6. 💾 Update `script.js` and save to `tvnu_events_selenium.json`
7. 🔒 Close the browser

### Expected Output

```
🔍 Scraping tv.nu with Selenium (JavaScript rendering)...

🏅 Scraping langdskidakning...
  Loading https://www.tv.nu/sport/langdskidakning...
  Found 5 programs
🏅 Scraping skidskytte...
  Loading https://www.tv.nu/sport/skidskytte...
  Found 3 programs
...

✅ Found 15 verified events from tv.nu

🔗 Merging with FIS/IBU calendar...
  Loaded 58 events from FIS/IBU calendar
✅ Total: 60 events (15 verified, 45 from calendar)

📺 Combined schedule:
  ✅ ⛷️ 2025-11-21 11:00 - SVT1     - Längdskidåkning, Gällivare - Sprint
  ✅ ⛷️ 2025-11-22 10:00 - SVT1     - Längdskidåkning, Gällivare - 10 km klassiskt, herrar
  ...

✅ Saved to tvnu_events_selenium.json
✅ Updated script.js with 60 events

✨ Done! 60 total events
   ✅ 15 verified from TV schedules
   📅 45 from calendar (TBA)

🔒 Browser closed
```

## Troubleshooting

### "chromedriver not found"

**Solution**: Install ChromeDriver manually (see Step 3 above)

### "Chrome not found"

**Solution**: Install Google Chrome browser

### "Timeout waiting for content"

**Possible causes**:
- Slow internet connection
- tv.nu is down or blocked
- Page structure changed

**Solution**: The scraper will continue with other sports. Check tv.nu manually if issue persists.

### "No winter sports programs found"

**Possible causes**:
- No events scheduled yet (season hasn't started)
- Page structure changed on tv.nu

**Solution**: The calendar events (TBA) will still be included from FIS/IBU data

## Performance

- **Speed**: ~2-3 seconds per sport page
- **Total time**: ~15-20 seconds for all 8 sports
- **Resources**: Headless Chrome uses ~100-200 MB RAM

## Comparison: Simple vs Selenium

| Feature | fetch_tvnu_simple.py | fetch_tvnu_selenium.py |
|---------|---------------------|------------------------|
| Dependencies | None (stdlib only) | Selenium + Chrome |
| Speed | Fast (~2 seconds) | Moderate (~20 seconds) |
| JavaScript | ❌ Cannot parse | ✅ Full rendering |
| Accuracy | Low (sport pages empty) | ✅ High (gets actual data) |
| **Recommended** | No (doesn't work for sport pages) | **Yes** ✅ |

## Automation

Add to your scheduled task:

### Windows Task Scheduler

```powershell
# Step 1: Get FIS/IBU calendar
python C:\Users\cpa\projects\winter-sports-tv-schedule\parse_events_combined.py

# Step 2: Get verified TV schedules with Selenium
python C:\Users\cpa\projects\winter-sports-tv-schedule\fetch_tvnu_selenium.py
```

### Daily Update Script

Create `update_all.bat`:
```batch
@echo off
cd C:\Users\cpa\projects\winter-sports-tv-schedule
python parse_events_combined.py
python fetch_tvnu_selenium.py
echo Update complete!
pause
```

Run this daily to keep your schedule updated with the latest TV broadcasts!

## Notes

- Headless mode means Chrome runs invisibly in the background
- The browser automatically closes when scraping is done
- All verified events show ✅, calendar placeholders show 📅
- TBA events get replaced with verified data when TV schedules are published
