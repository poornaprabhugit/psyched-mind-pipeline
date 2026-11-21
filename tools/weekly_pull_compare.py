"""Compare two weekly top-Shorts pulls: each Short's views vs its channel's median (Shorts <=180 s), by topic, for Shorts published in the pull window.
Usage: python tools/weekly_pull_compare.py research/topshorts-A.json SINCE_A research/topshorts-B.json SINCE_B"""
import json, re, statistics as st, sys
TOP = {'money': r'(\$|\bmoney\b|\brich\b|wealth|million|billion|business|success|poor|salary|broke|price|buy|spend)',
       'brain/memory': r'\b(brain|memory|remember|forget|mind)\b', 'love': r'\b(love|crush|attract\w*|relationship|dating|ex)\b',
       'dark/power': r'\b(dark|manipulat\w*|power\w*|respect|alpha)\b', 'body/sleep/food': r'\b(sleep|body|eat|food|stress|anxiety)\b',
       'signs/people who': r'\b(signs?|people who|if you)\b', 'starts Why': r'^why\b', 'you/your': r'\byou(r)?\b'}
def an(f, since):
    d = json.load(open(f)); rows = []; used = 0
    for c in d['channels']:
        sh = [s for s in c.get('uploads', []) if (s.get('dur') or 999) <= 180]
        if len(sh) < 10: continue
        med = st.median([s.get('views') or 0 for s in sh]) or 1; used += 1
        for s in sh:
            if s.get('published', '') >= since:
                rows.append((s['title'], (s.get('views') or 0) / med, c['title'], s.get('views') or 0, s.get('dur')))
    return rows, used
for f, since in zip(sys.argv[1::2], sys.argv[2::2]):
    rows, used = an(f, since)
    print(f'{f}: {used} channels, {len(rows)} Shorts since {since}; all median {st.median([r[1] for r in rows]):.2f}x')
    for k, p in TOP.items():
        r = [x[1] for x in rows if re.search(p, x[0].lower())]
        if len(r) >= 5: print(f'  {k:18s} n={len(r):3d}  median {st.median(r):.2f}x  share>2x {sum(v>2 for v in r)/len(r):.0%}')
    durs = [x for x in rows if x[4]]
    for lo, hi in [(0, 30), (31, 60), (61, 180)]:
        r = [x[1] for x in durs if lo <= x[4] <= hi]
        if r: print(f'  length {lo}-{hi}s n={len(r)} median {st.median(r):.2f}x')
    for t in sorted(rows, key=lambda x: -x[1])[:8]: print(f'   {t[1]:5.1f}x {t[3]:>9,} {t[2][:18]:18s} | {t[0][:80]}')
