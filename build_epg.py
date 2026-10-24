"""Builds out/epg.json (копия tools/build_epg.py для GitHub Actions): compact TV guide for the channels in channels.json.

Usage:  python build_epg.py [path/to/epg.xml.gz]
Without an argument it downloads https://iptvx.one/epg/epg.xml.gz (~70 MB).
Output format: {"<epgId>": [[startMinutesUtc, endMinutesUtc, "title"], ...]} for -6h..+48h.
"""
import gzip, json, sys, time, urllib.request, os
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(ROOT, 'channels.json')
OUT = os.path.join(ROOT, 'out', 'epg.json')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def parse_time(s):
    return int(datetime.strptime(s.replace(' ', ''), '%Y%m%d%H%M%S%z').timestamp() // 60)

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src:
        src = os.path.join(ROOT, 'epg.xml.gz')
        print('downloading...'); urllib.request.urlretrieve('https://iptvx.one/epg/epg.xml.gz', src)
    ids = {c['epg'] for c in json.load(open(CH, encoding='utf-8')) if c.get('epg')}
    now = int(time.time() // 60)
    lo, hi = now - 6 * 60, now + 48 * 60
    out = {i: [] for i in ids}
    for _, el in ET.iterparse(gzip.open(src), events=('end',)):
        if el.tag == 'programme':
            cid = el.get('channel')
            if cid in out:
                s, e = parse_time(el.get('start')), parse_time(el.get('stop'))
                if e > lo and s < hi:
                    t = el.find('title')
                    out[cid].append([s, e, (t.text or '').strip() if t is not None else ''])
            el.clear()
    for v in out.values():
        v.sort()
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('channels with programmes:', sum(1 for v in out.values() if v), 'of', len(out), '->', OUT, os.path.getsize(OUT) // 1024, 'KB')

main()
