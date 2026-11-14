import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SHORTS, LONG
R = "/home/claude/"
cands = {}
for d, ids in (("res-search", list(SHORTS) + list(LONG)), ("res-sb", [k + "b" for k in ["s01", "s03", "s04", "s06", "s07"]])):
    for i in ids:
        cands[i] = json.load(open(f"{R}{d}/{i}_candidates.json"))
def url(ref):
    vid, lbl = ref.split(":")
    n, k = map(int, lbl.split("-"))
    return cands[vid]["lines"][n - 1]["candidates"][k]["url"]
P = {
"s01": "s01:7-6 s01:7-1 s01:3-0 s01b:4-0 s01:6-5 s01:4-4 s01:5-4 s01:5-1 s01:6-7 s01:7-3 s01:8-5 s01:8-7 s01:9-3",
"s02": "s02:2-5 s02:1-4 s02:1-2 s02:2-4 s02:3-4 s02:3-7 s02:4-5 s02:6-5 s02:7-0 s02:7-1 s02:8-5 s02:9-3 s02:1-0",
"s03": "s03:2-4 s03:2-3 s03b:1-4 s03:3-5 s03b:3-2 s03:2-1 s03:6-2 s03:9-5 s03:2-7 s03:8-5 s03:9-3 s03:9-6",
"s04": "s04:1-4 s04b:2-0 s04:1-1 s04:2-1 s04:2-5 s04b:2-4 s04:6-1 s04:7-3 s04:7-5 s04:8-1 s04:8-2 s04:8-4",
"s05": "s05:4-4 s05:5-2 s05:4-7 s05:1-7 s05:4-2 s05:3-5 s05:3-2 s05:5-1 s05:6-0 s05:7-0 s05:7-1 s05:8-5 s05:8-3",
"s06": "s06:6-2 s06b:1-1 s06:1-7 s06:2-7 s06:3-6 s06:3-5 s06:5-2 s06b:3-7 s06:2-1 s06b:3-3 s06:7-7 s06:1-0",
"s07": "s07:1-4 s07:1-3 s07:2-0 s07:3-4 s07:4-2 s07b:1-5 s07b:3-1 s07:6-4 s07:6-1 s07:7-3 s07:7-7 s07:8-6 s07:9-4 s07:9-3",
}
pl = json.load(open(R + "picks_long.json"))
vids, seen = [], set()
for k, v in SHORTS.items():
    clips = []
    for r in P[k].split():
        if url(r) not in seen:
            clips.append(url(r)); seen.add(url(r))
    vids.append({"id": k, "subject": v["subject"], "script": " ".join(t for t, _ in v["lines"]),
                 "hook_text": v["hook_text"], "cta_text": "Full video: tap the link below",
                 "fast_open": {"clips": 3, "seconds": 1.5}, "clips": clips})
LS = {"video_aspect": "16:9", "video_clip_duration": 4, "subtitle_position": "bottom", "font_size": 64,
      "bgm_type": "", "bgm_volume": 0.0, "voice_rate": 1.0}
for k, (title, lines) in LONG.items():
    clips = []
    for c in pl[k]:
        if c["url"] not in seen:
            clips.append(c["url"]); seen.add(c["url"])
    v = {"id": k, "subject": title or "The psychology of looking rich", "script": " ".join(t for t, _ in lines),
         "clips": clips, "settings": LS}
    if title: v["title_card"] = title
    else: v["chapter"] = "Why looking rich follows hidden rules"
    vids.append(v)
job = {"videos": vids, "long": {"id": "long02", "segments": list(LONG)}}
json.dump(job, open("jobs/2026-11-14/render.json", "w"), indent=1, ensure_ascii=False)
print(len(vids), [len(v["clips"]) for v in vids])
