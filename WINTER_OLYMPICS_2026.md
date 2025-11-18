# Winter Olympics 2026 Support

Your winter sports TV guide now supports **all Winter Olympic sports** in preparation for the Milano-Cortina 2026 Winter Olympics!

## Supported Sports

The application now tracks all 15 Olympic winter sport disciplines:

### ⛷️ Skiing Sports
- **Längdskidor** (Cross-Country Skiing)
- **Skidskytte** (Biathlon)  
- **Alpint** (Alpine Skiing) - Downhill, Slalom, Giant Slalom, Super-G, Combined
- **Freestyle** - Moguls, Aerials, Ski Cross, Halfpipe, Slopestyle, Big Air
- **Backhoppning** (Ski Jumping)
- **Nordisk Kombination** (Nordic Combined)

### 🏂 Snowboard
- Parallel Giant Slalom, Halfpipe, Slopestyle, Snowboard Cross, Big Air

### ⛸️ Ice Sports
- **Konståkning** (Figure Skating) - Singles, Pairs, Ice Dance
- **Skridsko** (Speed Skating) - Long Track & Short Track
- **Ishockey** (Ice Hockey)
- **Curling**

### 🛷 Sliding Sports
- **Bob** (Bobsleigh) - 2-man, 4-man, Women
- **Skeleton**
- **Rodel** (Luge) - Singles, Doubles, Team Relay

## Filter System

The website now has **9 filter buttons** to show/hide different sports:

1. ⛷️ **Längdskidor** - Cross-country skiing
2. 🎯 **Skidskytte** - Biathlon
3. 🎿 **Alpint** - Alpine skiing
4. 🪂 **Backhoppning** - Ski jumping
5. 🏒 **Ishockey** - Ice hockey
6. ⛸️ **Konståkning** - Figure skating
7. ⏱️ **Skridsko** - Speed skating (long & short track)
8. 🥌 **Curling**
9. 🏆 **Övrigt** - All other sports (freestyle, snowboard, nordic combined, sliding sports)

## Automatic Detection

The `fetch_tvnu_simple.py` scraper automatically recognizes and categorizes sports based on:

### Swedish Keywords
- Längdskidor, Alpint, Backhoppning, Skidskytte
- Ishockey, Konståkning, Skridsko, Curling
- Freestyle, Snowboard, Nordisk Kombination
- Bob, Skeleton, Rodel

### English Keywords
- Cross-country, Alpine, Ski jumping, Biathlon
- Ice hockey, Figure skating, Speed skating
- Bobsleigh, Luge
- Slalom, Downhill, Super-G, Halfpipe, Slopestyle

### Competition Keywords
- OS, Olympi*, Winter Olympics
- VM, World Championship
- Världscup, World Cup

### Location Keywords
The scraper recognizes major winter sports venues:
- **Nordic**: Ruka, Trondheim, Lillehammer, Falun, Oslo, Drammen, Åre
- **Alpine**: Kitzbühel, Wengen, Cortina, Val Gardena, Schladming
- **Swiss**: Davos, St. Moritz
- **Italian**: Cortina (2026 Olympics host)
- **Tour de Ski** stages

## Milano-Cortina 2026

The 2026 Winter Olympics will be held in **Milano-Cortina, Italy** from February 6-22, 2026.

### Olympic Venues
- **Milano** - Ice hockey, figure skating, short track
- **Cortina d'Ampezzo** - Alpine skiing, curling, sliding sports
- **Valtellina** - Snowboard, freestyle
- **Anterselva** - Biathlon
- **Val di Fiemme** - Cross-country, Nordic combined, ski jumping

The scraper will automatically detect Olympic broadcasts when they appear on Swedish TV!

## Usage During Olympics

### Before Olympics (Now)
Run regularly to catch:
- World Cup events
- World Championships
- National championships
- Olympic qualifiers

### During Olympics (Feb 2026)
The scraper will automatically find:
- All Olympic events on SVT1, SVT2, TV4
- Opening & closing ceremonies
- Medal ceremonies
- Highlights and replays

### Recommended Schedule
```bash
# Daily during Olympics
python fetch_tvnu_simple.py

# Weekly during regular season
python fetch_tvnu_simple.py
```

## TV Coverage

### Expected Olympic Coverage
- **SVT1** - Prime events, Swedish athletes, opening/closing
- **SVT2** - Extended coverage, multiple events
- **SVT Play** - Live streams of all Swedish athlete events
- **TV4** - Select events, highlights

## Testing

To test the full system with all sports:

```bash
# Run the scraper
python fetch_tvnu_simple.py

# Open index.html in browser
# Toggle different sport filters
# Verify all 9 filter buttons work correctly
```

## Data Structure

Events are stored with sport type:
```javascript
{
    "id": 1,
    "sport": "alpine",          // or: cross-country, biathlon, ski-jumping, 
                                 //     ice-hockey, figure-skating, speed-skating,
                                 //     curling, other
    "title": "Alpint: Världscupen från Kitzbühel",
    "competition": "Störtlopp - Herrar",
    "channel": "SVT2",
    "date": "2026-01-24",
    "time": "11:30",
    "description": "Alpint: Världscupen från Kitzbühel - Störtlopp herrar"
}
```

## Future Enhancements

Potential additions for Olympics coverage:
- [ ] Medal count tracker
- [ ] Swedish athlete focus mode
- [ ] Live score integration
- [ ] Push notifications for Swedish medals
- [ ] Paralympic Winter Games support (Milano-Cortina, March 2026)

## Support

For issues or questions about Olympic coverage:
1. Check that keywords are up to date in `fetch_tvnu_simple.py`
2. Verify tv.nu is showing the events
3. Check `tvnu_events.json` for raw scraped data
4. Adjust keywords if Swedish broadcasters use different terminology

---

**Ready for Milano-Cortina 2026! 🇮🇹⛷️🏅**
