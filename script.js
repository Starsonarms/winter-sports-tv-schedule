// Event data - updated from tv.nu (Selenium)
const events = [
    {
        "sport": "ice-hockey",
        "title": "Buffalo Sabres - Edmonton Oilers - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Premium",
        "date": "2025-11-17",
        "time": "01:05",
        "description": "Buffalo Sabres - Edmonton Oilers - Ishockey, NHL (H)",
        "id": 1
    },
    {
        "sport": "ice-hockey",
        "title": "Boston Bruins - Carolina Hurricanes - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Extra",
        "date": "2025-11-17",
        "time": "01:05",
        "description": "Boston Bruins - Carolina Hurricanes - Ishockey, NHL (H)",
        "id": 2
    },
    {
        "sport": "ice-hockey",
        "title": "Washington Capitals - Los Angeles Kings - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport 1",
        "date": "2025-11-17",
        "time": "01:05",
        "description": "Washington Capitals - Los Angeles Kings - Ishockey, NHL (H)",
        "id": 3
    },
    {
        "sport": "ice-hockey",
        "title": "Florida Panthers - Vancouver Canucks - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Vinter",
        "date": "2025-11-17",
        "time": "01:05",
        "description": "Florida Panthers - Vancouver Canucks - Ishockey, NHL (H)",
        "id": 4
    },
    {
        "sport": "ice-hockey",
        "title": "Columbus Blue Jackets - Montreal Canadiens - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Live 1",
        "date": "2025-11-17",
        "time": "01:35",
        "description": "Columbus Blue Jackets - Montreal Canadiens - Ishockey, NHL (H)",
        "id": 5
    },
    {
        "sport": "ice-hockey",
        "title": "Anaheim Ducks - Utah Hockey Club - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Vinter",
        "date": "2025-11-17",
        "time": "04:05",
        "description": "Anaheim Ducks - Utah Hockey Club - Ishockey, NHL (H)",
        "id": 6
    },
    {
        "sport": "ice-hockey",
        "title": "BIK Karlskoga - Östersunds IK - Ishockey, Hockeyallsvenskan (H)",
        "competition": "Världscup",
        "channel": "TV4 Hockey",
        "date": "2025-11-17",
        "time": "18:55",
        "description": "BIK Karlskoga - Östersunds IK - Ishockey, Hockeyallsvenskan (H)",
        "id": 7
    },
    {
        "sport": "ice-hockey",
        "title": "Toronto Maple Leafs - St. Louis Blues - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Extra",
        "date": "2025-11-18",
        "time": "01:05",
        "description": "Toronto Maple Leafs - St. Louis Blues - Ishockey, NHL (H)",
        "id": 8
    },
    {
        "sport": "ice-hockey",
        "title": "Detroit Red Wings - Seattle Kraken - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Premium",
        "date": "2025-11-18",
        "time": "01:05",
        "description": "Detroit Red Wings - Seattle Kraken - Ishockey, NHL (H)",
        "id": 9
    },
    {
        "sport": "ice-hockey",
        "title": "Tampa Bay Lightning - New Jersey Devils - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Vinter",
        "date": "2025-11-18",
        "time": "01:05",
        "description": "Tampa Bay Lightning - New Jersey Devils - Ishockey, NHL (H)",
        "id": 10
    },
    {
        "sport": "ice-hockey",
        "title": "Winnipeg Jets - Columbus Blue Jackets - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Live 1",
        "date": "2025-11-18",
        "time": "02:05",
        "description": "Winnipeg Jets - Columbus Blue Jackets - Ishockey, NHL (H)",
        "id": 11
    },
    {
        "sport": "ice-hockey",
        "title": "Dallas Stars - New York Islanders - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Live 2",
        "date": "2025-11-18",
        "time": "02:05",
        "description": "Dallas Stars - New York Islanders - Ishockey, NHL (H)",
        "id": 12
    },
    {
        "sport": "ice-hockey",
        "title": "Chicago Blackhawks - Calgary Flames - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport 1",
        "date": "2025-11-18",
        "time": "02:35",
        "description": "Chicago Blackhawks - Calgary Flames - Ishockey, NHL (H)",
        "id": 13
    },
    {
        "sport": "ice-hockey",
        "title": "Vegas Golden Knights - New York Rangers - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Vinter",
        "date": "2025-11-18",
        "time": "04:05",
        "description": "Vegas Golden Knights - New York Rangers - Ishockey, NHL (H)",
        "id": 14
    },
    {
        "sport": "ice-hockey",
        "title": "San Jose Sharks - Utah Hockey Club - Ishockey, NHL (H)",
        "competition": "Världscup",
        "channel": "V Sport Premium",
        "date": "2025-11-18",
        "time": "04:05",
        "description": "San Jose Sharks - Utah Hockey Club - Ishockey, NHL (H)",
        "id": 15
    },
    {
        "sport": "ice-hockey",
        "title": "HC Kometa Brno - Luleå HF - Ishockey, Champions Hockey League, Åttondelsfinal",
        "competition": "Världscup",
        "channel": "TV10",
        "date": "2025-11-18",
        "time": "17:55",
        "description": "HC Kometa Brno - Luleå HF - Ishockey, Champions Hockey League, Åttondelsfinal",
        "id": 16
    },
    {
        "sport": "ice-hockey",
        "title": "Frölunda HC - Grenoble Bruleurs de Loups - Ishockey, Champions Hockey League, Åttondelsfinal",
        "competition": "Världscup",
        "channel": "V Sport Vinter",
        "date": "2025-11-18",
        "time": "18:55",
        "description": "Frölunda HC - Grenoble Bruleurs de Loups - Ishockey, Champions Hockey League, Åttondelsfinal",
        "id": 17
    },
    {
        "sport": "ice-hockey",
        "title": "SC Bern - Brynäs IF - Ishockey, Champions Hockey League, Åttondelsfinal",
        "competition": "Världscup",
        "channel": "V Sport 1",
        "date": "2025-11-18",
        "time": "19:40",
        "description": "SC Bern - Brynäs IF - Ishockey, Champions Hockey League, Åttondelsfinal",
        "id": 18
    },
    {
        "sport": "cross-country",
        "title": "Sprint - Längdskidåkning, Gällivare",
        "competition": "Sprint",
        "channel": "SVT1",
        "date": "2025-11-21",
        "time": "11:00",
        "description": "Sprint - Längdskidåkning, Gällivare",
        "id": 19
    },
    {
        "sport": "figure-skating",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-21",
        "time": "13:00",
        "description": "Längdskidåkning",
        "id": 20
    },
    {
        "sport": "ski-jumping",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-21",
        "time": "15:50",
        "description": "Längdskidåkning",
        "id": 21
    },
    {
        "sport": "curling",
        "title": "Schweiz-Sverige, damer - Curling",
        "competition": "Världscup - Damer",
        "channel": "Kunskapskanalen",
        "date": "2025-11-22",
        "time": "08:00",
        "description": "Schweiz-Sverige, damer - Curling",
        "id": 22
    },
    {
        "sport": "cross-country",
        "title": "10 km klassiskt, herrar - Längdskidåkning, Gällivare",
        "competition": "Klassiskt - Herrar",
        "channel": "SVT1",
        "date": "2025-11-22",
        "time": "10:00",
        "description": "10 km klassiskt, herrar - Längdskidåkning, Gällivare",
        "id": 23
    },
    {
        "sport": "cross-country",
        "title": "10 km klassiskt, damer - Längdskidåkning, Gällivare",
        "competition": "Klassiskt - Damer",
        "channel": "SVT1",
        "date": "2025-11-22",
        "time": "11:30",
        "description": "10 km klassiskt, damer - Längdskidåkning, Gällivare",
        "id": 24
    },
    {
        "sport": "figure-skating",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-22",
        "time": "11:30",
        "description": "Längdskidåkning",
        "id": 25
    },
    {
        "sport": "ski-jumping",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-22",
        "time": "11:50",
        "description": "Längdskidåkning",
        "id": 26
    },
    {
        "sport": "curling",
        "title": "Schweiz-Sverige, herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "Kunskapskanalen",
        "date": "2025-11-22",
        "time": "13:30",
        "description": "Schweiz-Sverige, herrar - Curling",
        "id": 27
    },
    {
        "sport": "ski-jumping",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-22",
        "time": "15:50",
        "description": "Längdskidåkning",
        "id": 28
    },
    {
        "sport": "cross-country",
        "title": "10 km fri stil, herrar - Längdskidåkning, Gällivare",
        "competition": "Fristil - Herrar",
        "channel": "SVT1",
        "date": "2025-11-23",
        "time": "10:05",
        "description": "10 km fri stil, herrar - Längdskidåkning, Gällivare",
        "id": 29
    },
    {
        "sport": "cross-country",
        "title": "10 km fri stil, damer - Längdskidåkning, Gällivare",
        "competition": "Fristil - Damer",
        "channel": "SVT1",
        "date": "2025-11-23",
        "time": "11:30",
        "description": "10 km fri stil, damer - Längdskidåkning, Gällivare",
        "id": 30
    },
    {
        "sport": "ski-jumping",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-23",
        "time": "11:50",
        "description": "Längdskidåkning",
        "id": 31
    },
    {
        "sport": "ski-jumping",
        "title": "Längdskidåkning",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-11-23",
        "time": "15:50",
        "description": "Längdskidåkning",
        "id": 32
    },
    {
        "sport": "curling",
        "title": "Sverige-Norge, herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "SVT1",
        "date": "2025-11-24",
        "time": "11:00",
        "description": "Sverige-Norge, herrar - Curling",
        "id": 33
    },
    {
        "sport": "curling",
        "title": "Lohja Gruppspel Herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "Eurosport 1",
        "date": "2025-11-24",
        "time": "11:00",
        "description": "Lohja Gruppspel Herrar - Curling",
        "id": 34
    },
    {
        "sport": "curling",
        "title": "Lohja Gruppspel Damer - Curling",
        "competition": "Världscup - Damer",
        "channel": "Eurosport 1",
        "date": "2025-11-24",
        "time": "15:00",
        "description": "Lohja Gruppspel Damer - Curling",
        "id": 35
    },
    {
        "sport": "curling",
        "title": "Lohja Gruppspel Herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "Eurosport 2",
        "date": "2025-11-24",
        "time": "19:00",
        "description": "Lohja Gruppspel Herrar - Curling",
        "id": 36
    },
    {
        "sport": "curling",
        "title": "Sverige-Italien, herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "Kunskapskanalen",
        "date": "2025-11-26",
        "time": "08:00",
        "description": "Sverige-Italien, herrar - Curling",
        "id": 37
    },
    {
        "sport": "curling",
        "title": "Lohja Gruppspel Damer - Curling",
        "competition": "Världscup - Damer",
        "channel": "Eurosport 2",
        "date": "2025-11-26",
        "time": "13:00",
        "description": "Lohja Gruppspel Damer - Curling",
        "id": 38
    },
    {
        "sport": "curling",
        "title": "Sverige-Danmark, damer - Curling",
        "competition": "Världscup - Damer",
        "channel": "SVT2",
        "date": "2025-11-27",
        "time": "08:00",
        "description": "Sverige-Danmark, damer - Curling",
        "id": 39
    },
    {
        "sport": "curling",
        "title": "Österrike-Sverige, herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "SVT1",
        "date": "2025-11-27",
        "time": "13:00",
        "description": "Österrike-Sverige, herrar - Curling",
        "id": 40
    },
    {
        "sport": "curling",
        "title": "Lohja Gruppspel Herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "Eurosport 1",
        "date": "2025-11-27",
        "time": "13:00",
        "description": "Lohja Gruppspel Herrar - Curling",
        "id": 41
    },
    {
        "sport": "curling",
        "title": "Lohja Semifinal Damer - Curling, EM",
        "competition": "Världscup - Damer",
        "channel": "Eurosport 2",
        "date": "2025-11-27",
        "time": "18:00",
        "description": "Lohja Semifinal Damer - Curling, EM",
        "id": 42
    },
    {
        "id": 43,
        "sport": "cross-country",
        "title": "Världscupen i Ruka",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2025-11-28",
        "time": "TBA",
        "description": "Världscuptävling i Ruka"
    },
    {
        "id": 44,
        "sport": "cross-country",
        "title": "Världscupen i Ruka",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2025-11-28",
        "time": "TBA",
        "description": "Världscuptävling i Ruka"
    },
    {
        "sport": "curling",
        "title": "Final, damer - Curling",
        "competition": "Världscup - Damer",
        "channel": "SVT1",
        "date": "2025-11-29",
        "time": "09:00",
        "description": "Final, damer - Curling",
        "id": 45
    },
    {
        "sport": "curling",
        "title": "Lohja Damer - Curling, EM",
        "competition": "Världscup - Damer",
        "channel": "Eurosport 1",
        "date": "2025-11-29",
        "time": "09:00",
        "description": "Lohja Damer - Curling, EM",
        "id": 46
    },
    {
        "sport": "biathlon",
        "title": "Stafett, damer - Skidskytte, Världscupen",
        "competition": "Stafett - Damer",
        "channel": "SVT1",
        "date": "2025-11-29",
        "time": "13:15",
        "description": "Stafett, damer - Skidskytte, Världscupen",
        "id": 47
    },
    {
        "sport": "curling",
        "title": "Lohja Final Herrar - Curling, EM",
        "competition": "Världscup - Herrar",
        "channel": "Eurosport 1",
        "date": "2025-11-29",
        "time": "14:00",
        "description": "Lohja Final Herrar - Curling, EM",
        "id": 48
    },
    {
        "sport": "curling",
        "title": "Final, herrar - Curling",
        "competition": "Världscup - Herrar",
        "channel": "SVT2",
        "date": "2025-11-29",
        "time": "14:00",
        "description": "Final, herrar - Curling",
        "id": 49
    },
    {
        "sport": "biathlon",
        "title": "Stafett, herrar - Skidskytte, Världscupen",
        "competition": "Stafett - Herrar",
        "channel": "SVT1",
        "date": "2025-11-29",
        "time": "16:55",
        "description": "Stafett, herrar - Skidskytte, Världscupen",
        "id": 50
    },
    {
        "id": 51,
        "sport": "cross-country",
        "title": "Världscupen i Ruka",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2025-11-29",
        "time": "TBA",
        "description": "Världscuptävling i Ruka"
    },
    {
        "id": 52,
        "sport": "cross-country",
        "title": "Världscupen i Ruka",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2025-11-29",
        "time": "TBA",
        "description": "Världscuptävling i Ruka"
    },
    {
        "sport": "cross-country",
        "title": "20km fri stil, masstart (H) - Längdskidåkning",
        "competition": "Masstart",
        "channel": "Viaplay Sport",
        "date": "2025-11-30",
        "time": "10:00",
        "description": "20km fri stil, masstart (H) - Längdskidåkning",
        "id": 53
    },
    {
        "sport": "cross-country",
        "title": "20km fri stil, masstart (D) - Längdskidåkning",
        "competition": "Masstart",
        "channel": "Viaplay Sport",
        "date": "2025-11-30",
        "time": "11:45",
        "description": "20km fri stil, masstart (D) - Längdskidåkning",
        "id": 54
    },
    {
        "sport": "biathlon",
        "title": "Singlemixed - Skidskytte, Världscupen",
        "competition": "Världscup",
        "channel": "SVT1",
        "date": "2025-11-30",
        "time": "14:00",
        "description": "Singlemixed - Skidskytte, Världscupen",
        "id": 55
    },
    {
        "sport": "biathlon",
        "title": "Mixedstafett - Skidskytte, Världscupen",
        "competition": "Stafett",
        "channel": "SVT1",
        "date": "2025-11-30",
        "time": "16:40",
        "description": "Mixedstafett - Skidskytte, Världscupen",
        "id": 56
    },
    {
        "id": 57,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2025-12-05",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 58,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2025-12-05",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 59,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "Skiatlon - Herrar",
        "channel": "TBA",
        "date": "2025-12-06",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 60,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "Skiatlon - Damer",
        "channel": "TBA",
        "date": "2025-12-06",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 61,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2025-12-07",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 62,
        "sport": "cross-country",
        "title": "Världscupen i Trondheim",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2025-12-07",
        "time": "TBA",
        "description": "Världscuptävling i Trondheim"
    },
    {
        "id": 63,
        "sport": "biathlon",
        "title": "Världscupen i Hochfilzen",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-12-08",
        "time": "TBA",
        "description": "Skidskytte-världscup i Hochfilzen"
    },
    {
        "id": 64,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "Teamsprint - Damer",
        "channel": "TBA",
        "date": "2025-12-12",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 65,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "Teamsprint - Herrar",
        "channel": "TBA",
        "date": "2025-12-12",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 66,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2025-12-13",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 67,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2025-12-13",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 68,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2025-12-14",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 69,
        "sport": "cross-country",
        "title": "Världscupen i Davos",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2025-12-14",
        "time": "TBA",
        "description": "Världscuptävling i Davos"
    },
    {
        "id": 70,
        "sport": "biathlon",
        "title": "Världscupen i Annecy-Le Grand Bornand",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2025-12-15",
        "time": "TBA",
        "description": "Skidskytte-världscup i Annecy-Le Grand Bornand"
    },
    {
        "id": 71,
        "sport": "cross-country",
        "title": "Världscupen i Tour de Ski",
        "competition": "50 km - Damer",
        "channel": "TBA",
        "date": "2026-01-04",
        "time": "TBA",
        "description": "Världscuptävling i Tour de Ski"
    },
    {
        "id": 72,
        "sport": "cross-country",
        "title": "Världscupen i Tour de Ski",
        "competition": "50 km - Herrar",
        "channel": "TBA",
        "date": "2026-01-04",
        "time": "TBA",
        "description": "Världscuptävling i Tour de Ski"
    },
    {
        "id": 73,
        "sport": "biathlon",
        "title": "Världscupen i Oberhof",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-01-05",
        "time": "TBA",
        "description": "Skidskytte-världscup i Oberhof"
    },
    {
        "id": 74,
        "sport": "biathlon",
        "title": "Världscupen i Ruhpolding",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-01-12",
        "time": "TBA",
        "description": "Skidskytte-världscup i Ruhpolding"
    },
    {
        "id": 75,
        "sport": "cross-country",
        "title": "Världscupen i Oberhof",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-01-17",
        "time": "TBA",
        "description": "Världscuptävling i Oberhof"
    },
    {
        "id": 76,
        "sport": "cross-country",
        "title": "Världscupen i Oberhof",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-01-17",
        "time": "TBA",
        "description": "Världscuptävling i Oberhof"
    },
    {
        "id": 77,
        "sport": "cross-country",
        "title": "Världscupen i Oberhof",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2026-01-18",
        "time": "TBA",
        "description": "Världscuptävling i Oberhof"
    },
    {
        "id": 78,
        "sport": "cross-country",
        "title": "Världscupen i Oberhof",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2026-01-18",
        "time": "TBA",
        "description": "Världscuptävling i Oberhof"
    },
    {
        "id": 79,
        "sport": "biathlon",
        "title": "Världscupen i Nove Mesto na Morave",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-01-19",
        "time": "TBA",
        "description": "Skidskytte-världscup i Nove Mesto na Morave"
    },
    {
        "id": 80,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "Teamsprint - Herrar",
        "channel": "TBA",
        "date": "2026-01-23",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 81,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "Teamsprint - Damer",
        "channel": "TBA",
        "date": "2026-01-23",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 82,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-01-24",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 83,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-01-24",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 84,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "30 km - Herrar",
        "channel": "TBA",
        "date": "2026-01-25",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 85,
        "sport": "cross-country",
        "title": "Världscupen i Goms",
        "competition": "30 km - Damer",
        "channel": "TBA",
        "date": "2026-01-25",
        "time": "TBA",
        "description": "Världscuptävling i Goms"
    },
    {
        "id": 86,
        "sport": "biathlon",
        "title": "Världscupen i Antholz-Anterselva",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-02-06",
        "time": "TBA",
        "description": "Skidskytte-världscup i Antholz-Anterselva"
    },
    {
        "id": 87,
        "sport": "cross-country",
        "title": "Världscupen i Falun",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-02-28",
        "time": "TBA",
        "description": "Världscuptävling i Falun"
    },
    {
        "id": 88,
        "sport": "cross-country",
        "title": "Världscupen i Falun",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-02-28",
        "time": "TBA",
        "description": "Världscuptävling i Falun"
    },
    {
        "id": 89,
        "sport": "cross-country",
        "title": "Världscupen i Falun",
        "competition": "Skiatlon - Herrar",
        "channel": "TBA",
        "date": "2026-03-01",
        "time": "TBA",
        "description": "Världscuptävling i Falun"
    },
    {
        "id": 90,
        "sport": "cross-country",
        "title": "Världscupen i Falun",
        "competition": "Skiatlon - Damer",
        "channel": "TBA",
        "date": "2026-03-01",
        "time": "TBA",
        "description": "Världscuptävling i Falun"
    },
    {
        "id": 91,
        "sport": "biathlon",
        "title": "Världscupen i Kontiolahti",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-03-02",
        "time": "TBA",
        "description": "Skidskytte-världscup i Kontiolahti"
    },
    {
        "id": 92,
        "sport": "cross-country",
        "title": "Världscupen i Lahti",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-03-07",
        "time": "TBA",
        "description": "Världscuptävling i Lahti"
    },
    {
        "id": 93,
        "sport": "cross-country",
        "title": "Världscupen i Lahti",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-03-07",
        "time": "TBA",
        "description": "Världscuptävling i Lahti"
    },
    {
        "id": 94,
        "sport": "cross-country",
        "title": "Världscupen i Lahti",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2026-03-08",
        "time": "TBA",
        "description": "Världscuptävling i Lahti"
    },
    {
        "id": 95,
        "sport": "cross-country",
        "title": "Världscupen i Lahti",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2026-03-08",
        "time": "TBA",
        "description": "Världscuptävling i Lahti"
    },
    {
        "id": 96,
        "sport": "biathlon",
        "title": "Världscupen i Otepaa",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-03-09",
        "time": "TBA",
        "description": "Skidskytte-världscup i Otepaa"
    },
    {
        "id": 97,
        "sport": "cross-country",
        "title": "Världscupen i Drammen",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-03-12",
        "time": "TBA",
        "description": "Världscuptävling i Drammen"
    },
    {
        "id": 98,
        "sport": "cross-country",
        "title": "Världscupen i Drammen",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-03-12",
        "time": "TBA",
        "description": "Världscuptävling i Drammen"
    },
    {
        "id": 99,
        "sport": "cross-country",
        "title": "Världscupen i Oslo",
        "competition": "50 km - Herrar",
        "channel": "TBA",
        "date": "2026-03-14",
        "time": "TBA",
        "description": "Världscuptävling i Oslo"
    },
    {
        "id": 100,
        "sport": "cross-country",
        "title": "Världscupen i Oslo",
        "competition": "50 km - Damer",
        "channel": "TBA",
        "date": "2026-03-14",
        "time": "TBA",
        "description": "Världscuptävling i Oslo"
    },
    {
        "id": 101,
        "sport": "biathlon",
        "title": "Världscupen i Oslo Holmenkollen",
        "competition": "Världscup",
        "channel": "TBA",
        "date": "2026-03-16",
        "time": "TBA",
        "description": "Skidskytte-världscup i Oslo Holmenkollen"
    },
    {
        "id": 102,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "10 km - Damer",
        "channel": "TBA",
        "date": "2026-03-20",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    },
    {
        "id": 103,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "10 km - Herrar",
        "channel": "TBA",
        "date": "2026-03-20",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    },
    {
        "id": 104,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "Sprint - Damer",
        "channel": "TBA",
        "date": "2026-03-21",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    },
    {
        "id": 105,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "Sprint - Herrar",
        "channel": "TBA",
        "date": "2026-03-21",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    },
    {
        "id": 106,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "30 km - Damer",
        "channel": "TBA",
        "date": "2026-03-22",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    },
    {
        "id": 107,
        "sport": "cross-country",
        "title": "Världscupen i Lake Placid",
        "competition": "30 km - Herrar",
        "channel": "TBA",
        "date": "2026-03-22",
        "time": "TBA",
        "description": "Världscuptävling i Lake Placid"
    }
];














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

// Initialize filters based on data-default attributes
function initializeFilters() {
    const filterIds = [
        'filterCrossCountry',
        'filterBiathlon',
        'filterAlpine',
        'filterSkiJumping',
        'filterIceHockey',
        'filterFigureSkating',
        'filterSpeedSkating',
        'filterCurling',
        'filterOther'
    ];
    
    filterIds.forEach(id => {
        const checkbox = document.getElementById(id);
        if (checkbox) {
            // Set checked state based on data-default attribute
            const defaultValue = checkbox.getAttribute('data-default');
            checkbox.checked = defaultValue === 'true';
        }
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

// Initialize filters and render
initializeFilters();
renderSchedule();
