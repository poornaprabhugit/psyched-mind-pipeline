import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SHORTS, LONG
vids = []
for k, v in SHORTS.items():
    vids.append({"id": k, "lines": [{"n": i + 1, "text": t, "queries": q} for i, (t, q) in enumerate(v["lines"])]})
for k, (title, lines) in LONG.items():
    vids.append({"id": k, "aspect": "16:9", "lines": [{"n": i + 1, "text": t, "queries": q} for i, (t, q) in enumerate(lines)]})
os.makedirs("jobs/2026-11-14", exist_ok=True)
json.dump({"videos": vids}, open("jobs/2026-11-14/search.json", "w"), indent=1, ensure_ascii=False)
print(len(vids), sum(len(v["lines"]) for v in vids))
