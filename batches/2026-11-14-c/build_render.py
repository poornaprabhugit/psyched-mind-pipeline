import json, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from content import SHORTS
R = "/home/claude/"
cands = {}
for d in ("res-c", "res-cg"):
    for f in glob.glob(f"{R}{d}/*_candidates.json"):
        cands[os.path.basename(f).split("_")[0]] = json.load(open(f))
def url(ref):
    vid, lbl = ref.split(":")
    n, k = map(int, lbl.split("-"))
    return cands[vid]["lines"][n - 1]["candidates"][k]["url"]
P = {
"n01": "n01:1-0 n01:1-3 n01:1-2 n01:6-5 n01:2-5 g01:2-3 n01:4-6 n01:4-2 n01:5-1 n01:5-0 n01:6-0 n01:7-7 n01:1-4",
"n02": "n02:7-2 n02:7-0 n02:7-3 n02:2-3 n02:2-4 g02:1-1 n02:2-1 n02:2-5 n02:7-7 n02:5-0 n02:6-4 n02:6-3 n02:7-4",
"n03": "n03:1-6 g03:1-5 g03:1-4 n03:2-1 g03:3-5 n03:3-0 n03:3-5 n03:4-3 n03:4-5 n03:3-1 n03:5-0 n03:6-6 n03:7-4",
"n04": "n04:2-3 n04:2-0 n04:2-7 n04:1-3 n04:1-2 n04:1-4 n04:1-1 n04:4-0 n04:4-7 n04:5-0 g04:2-6 g04:2-2 n04:6-7 n04:7-1",
"n05": "n05:1-1 n05:1-3 n05:1-0 g05:1-0 n05:2-0 g05:1-2 n05:3-1 n05:1-7 n05:4-2 n05:5-0 n05:6-2 n05:6-3 n05:7-3 n05:7-5",
"n06": "n04:4-5 n06:6-0 n06:2-1 n06:2-3 n06:3-7 n06:4-2 n06:4-3 n06:5-0 n06:6-2 n06:6-4 n06:7-3 n06:7-7",
"n07": "n07:1-7 n07:1-3 g07:1-3 n07:2-0 n07:2-1 n07:3-7 n07:3-1 n07:4-6 n07:4-2 n07:5-5 n07:5-6 n07:6-2 n07:7-4 n07:7-0 n07:7-5",
}
seen = set()
for f in glob.glob("jobs/2026-11-14*/render.json"):
    if "-c" in f: continue
    for v in json.load(open(f))["videos"]:
        if not v["id"].startswith("L"):  # long-02 clips may reappear (different video/format); Shorts never share
            seen.update(v.get("clips", []))
vids = []
for k, v in SHORTS.items():
    clips, drop = [], []
    for r in P[k].split():
        u = url(r)
        if u in seen: drop.append(r); continue
        clips.append(u); seen.add(u)
    if drop: print(k, "dropped (already used):", drop)
    vids.append({"id": k, "subject": v["subject"], "script": " ".join(t for t, _ in v["lines"]),
                 "hook_text": v["hook_text"], "cta_text": "Full video: tap the link below",
                 "fast_open": {"clips": 3, "seconds": 1.5}, "clips": clips})
json.dump({"videos": vids, "tighten": True}, open("jobs/2026-11-14-c/render.json", "w"), indent=1, ensure_ascii=False)
print([(v["id"], len(v["clips"])) for v in vids])
