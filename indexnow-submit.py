#!/usr/bin/env python3
"""Submit all site URLs to Bing via IndexNow protocol."""

import json
import urllib.request
import os
from pathlib import Path

API_KEY = "45b13dbee7b6fa5e7a6757e76f381877"
HOST = "comunikoo.es"
ENDPOINT = "https://api.indexnow.org/indexnow"

def get_all_urls():
    """Find all index.html pages and return their URLs."""
    urls = []
    skip = {'node_modules', '.git', 'css', 'js', 'img', 'fonts', 'src', 'content'}
    site_dir = Path(__file__).parent

    for root, dirs, files in os.walk(site_dir):
        dirs[:] = [d for d in dirs if d not in skip]
        if 'index.html' in files:
            rel = os.path.relpath(root, site_dir)
            if rel == '.':
                urls.append(f'https://{HOST}/')
            else:
                urls.append(f'https://{HOST}/{rel}/')
    return sorted(urls)

def submit_to_indexnow(urls):
    """Submit URLs via IndexNow API (batch mode, max 10,000)."""
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": f"https://{HOST}/{API_KEY}.txt",
        "urlList": urls
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST'
    )

    try:
        response = urllib.request.urlopen(req)
        print(f"✅ {len(urls)} URLs enviadas a IndexNow")
        print(f"   Status: {response.status}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ Error: {e.code} — {e.reason}")
        if e.code == 202:
            print("   (202 = Aceptado, se procesará)")
            return True
        return False

if __name__ == '__main__':
    urls = get_all_urls()
    print(f"Encontradas {len(urls)} URLs")
    print(f"Enviando a IndexNow (Bing + Yandex + otros)...\n")

    # IndexNow acepta hasta 10,000 URLs por request
    submit_to_indexnow(urls)

    print(f"\nLas URLs serán rastreadas por Bing en las próximas horas.")
    print(f"Puedes verificar en: https://www.bing.com/webmaster/home/sitemaps")
