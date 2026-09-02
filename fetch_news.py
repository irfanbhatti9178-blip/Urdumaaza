import json, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = [
    ("ایکسپریس", "#E10600", "https://www.express.pk/feed/"),
    ("جنگ", "#006400", "https://www.jang.com.pk/rss/1.1.0"),
    ("اردو پوائنٹ", "#0A2A5E", "https://www.urdupoint.com/rss/"),
    ("دنیا", "#d35400", "https://dunya.com.pk/rss"),
    ("جیو", "#c0392b", "https://urdu.geo.tv/rss/feeds/0.xml"),
]

UA = "Mozilla/5.0 (compatible; UrdumaazaNewsBot/1.0)"

def text(node, names):
    for name in names:
        x = node.find(name)
        if x is not None and x.text:
            return x.text.strip()
    return ""

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def parse(xml, source, color):
    root = ET.fromstring(xml)
    rows = []
    for item in root.findall(".//item")[:10]:
        title = text(item, ["title"])
        link = text(item, ["link"])
        pub = text(item, ["pubDate", "published", "date"])
        if title and link:
            rows.append({"title": title, "link": link, "source": source, "color": color, "date": pub})
    return rows

items = []
for source, color, url in FEEDS:
    try:
        items.extend(parse(fetch(url), source, color))
    except Exception as e:
        print("Feed failed:", source, repr(e))

# Deduplicate by title and keep source order/recency supplied by feeds.
seen = set()
clean = []
for x in items:
    key = " ".join(x["title"].split()).lower()
    if key in seen:
        continue
    seen.add(key)
    clean.append(x)

clean = clean[:40]

out = {
    "updated": int(time.time()),
    "items": clean
}
Path("news.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved", len(clean), "headlines")
