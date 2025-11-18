"""Test tv.nu API to understand its structure."""

import json
from urllib.request import urlopen, Request
from urllib.parse import quote

# Test search
search_term = quote("längdskidor")
url = f"https://web-api.tv.nu/search?q={search_term}"

print(f"Testing URL: {url}\n")

try:
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Accept', 'application/json')
    
    with urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("✅ Success!")
        print(f"\nKeys in response: {list(data.keys())}\n")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
