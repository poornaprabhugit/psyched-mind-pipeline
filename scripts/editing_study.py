"""Editing study: measure how top videos are cut (fact base for the 'Alux-quality' decision).

Input: jobs/editing/<name>.json
  {"long_handles": [...], "short_handles": [...], "n_long": 3, "n_short": 2,
   "videos": [{"id": "...", "group": "ours"}], "max_seconds": 180, "scene_threshold": 0.3}
Output: research/editing/<name>/results.json plus, per video, <id>_open.jpg (first 3 s)
and <id>_sheet.jpg (one frame every ~10 s of the analysed part) to classify footage by eye.

Per video: length, analysed seconds, number of cuts (ffmpeg scene score > threshold),
seconds per shot (overall, first 15 s, first 60 s), and words per minute from YouTube's
auto captions over the analysed part when available.
Long videos are analysed over their first `max_seconds` only (to save Actions minutes).
"""
import glob, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from stats import access_token, get

API = "https://www.googleapis.com/youtube/v3/"


def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def pick(tok, handle, n, want_short, log):
    r = get(API + "channels", tok, {"part": "id,snippet,statistics,contentDetails", "forHandle": handle})
    if not r.get("items"):
        log.append({"handle": handle, "found": False, "error": r.get("error")})
        return []
    ch = r["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = []
    page = None
    while len(ids) < 100:
        p = {"part": "contentDetails", "playlistId": pl, "maxResults": 50}
        if page:
            p["pageToken"] = page
        rr = get(API + "playlistItems", tok, p)
        ids += [it["contentDetails"]["videoId"] for it in rr.get("items", [])]
        page = rr.get("nextPageToken")
        if not page:
            break
    vids = []
    for i in range(0, len(ids), 50):
        rr = get(API + "videos", tok, {"part": "contentDetails,statistics,snippet", "id": ",".join(ids[i:i + 50])})
        for it in rr.get("items", []):
            d = dur(it["contentDetails"]["duration"])
            vids.append({"id": it["id"], "title": it["snippet"]["title"], "dur": d,
                         "published": it["snippet"]["publishedAt"],
                         "views": int(it["statistics"].get("viewCount", 0) or 0)})
    vids = [v for v in vids if (v["dur"] <= 180) == want_short and (want_short or v["dur"] >= 240)]
    vids.sort(key=lambda v: -v["views"])
    meta = {"channel": ch["snippet"]["title"], "handle": handle,
            "subs": int(ch["statistics"].get("subscriberCount", 0) or 0), "pool": len(vids)}
    return [dict(v, **meta) for v in vids[:n]]


def run(cmd, timeout=600):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def captions_wpm(base, secs):
    files = glob.glob(base + "*.json3")
    if not files:
        return None
    try:
        d = json.load(open(files[0]))
    except Exception:
        return None
    words = 0
    for ev in d.get("events", []):
        if ev.get("tStartMs", 0) / 1000 > secs:
            break
        for s in ev.get("segs", []) or []:
            words += len(s.get("utf8", "").split())
    return round(words / (secs / 60), 1) if secs else None


def analyse(v, outdir, max_s, thr, cookies):
    vid = v["id"]
    base = f"/tmp/v_{vid}"
    secs = min(v.get("dur") or max_s, max_s)
    core = ["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=480]/b[height<=480]/b",
            "--download-sections", f"*0-{secs}", "-o", base + ".%(ext)s"]
    if cookies:
        core += ["--cookies", cookies]
    url = f"https://www.youtube.com/watch?v={vid}"
    subs = ["--write-auto-subs", "--sub-langs", "en.*,en", "--sub-format", "json3"]
    t0 = time.time()
    r = run(core + subs + [url], timeout=900)
    files = [f for f in glob.glob(base + ".*") if not f.endswith(".json3")]
    if not files:
        # captions may have failed the run; retry video only
        r2 = run(core + [url], timeout=900)
        files = [f for f in glob.glob(base + ".*") if not f.endswith(".json3")]
        if not files:
            v["error"] = (r.stderr + r2.stderr)[-600:]
            return v
    src = files[0]
    v["download_s"] = round(time.time() - t0, 1)
    probe = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src])
    try:
        got = float(probe.stdout.strip())
    except ValueError:
        got = secs
    v["analysed_s"] = round(got, 1)
    sc = run(["ffmpeg", "-hide_banner", "-i", src, "-vf",
              f"scale=320:-2,select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"], timeout=900)
    cuts = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", sc.stderr)]
    # ignore cuts closer than 0.3 s (flashes / transitions counted twice)
    clean = []
    for c in cuts:
        if not clean or c - clean[-1] >= 0.3:
            clean.append(c)
    v["cuts"] = [round(c, 2) for c in clean]

    def sps(limit):
        span = min(limit, got)
        n = len([c for c in clean if c < span])
        return round(span / (n + 1), 2)
    v["sec_per_shot"] = sps(1e9)
    v["sec_per_shot_first15"] = sps(15)
    v["sec_per_shot_first60"] = sps(60)
    v["first_cut_s"] = round(clean[0], 2) if clean else None
    v["wpm"] = captions_wpm(base, got)
    # frames: opening (0, 0.5, 1, 2 s) and a sheet every ~10 s (shorts: every 3 s)
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
         "select='eq(n,0)+eq(n,15)+eq(n,30)+eq(n,60)',scale=240:-2,tile=4x1", "-vsync", "0", "-frames:v", "1",
         f"{outdir}/{vid}_open.jpg"])
    step = 3 if got <= 70 else 10
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
         f"fps=1/{step},scale=200:-2,tile=6x3", "-frames:v", "1", f"{outdir}/{vid}_sheet.jpg"])
    for f in glob.glob(base + "*"):
        os.remove(f)
    return v


def main(job, outdir):
    cfg = json.load(open(job))
    os.makedirs(outdir, exist_ok=True)
    tok = access_token()
    log, todo = [], []
    for h in cfg.get("long_handles", []):
        todo += [dict(v, group="long") for v in pick(tok, h, cfg.get("n_long", 3), False, log)]
    for h in cfg.get("short_handles", []):
        todo += [dict(v, group="short") for v in pick(tok, h, cfg.get("n_short", 2), True, log)]
    extra = cfg.get("videos", [])
    if extra:
        r = get(API + "videos", tok, {"part": "contentDetails,statistics,snippet", "id": ",".join(x["id"] for x in extra)})
        info = {it["id"]: it for it in r.get("items", [])}
        for x in extra:
            it = info.get(x["id"])
            if it:
                todo.append({"id": x["id"], "group": x.get("group", "extra"), "title": it["snippet"]["title"],
                             "channel": it["snippet"]["channelTitle"], "dur": dur(it["contentDetails"]["duration"]),
                             "views": int(it["statistics"].get("viewCount", 0) or 0)})
    cookies = None
    if os.environ.get("YT_COOKIES"):
        cookies = "/tmp/cookies.txt"
        open(cookies, "w").write(os.environ["YT_COOKIES"])
    res = []
    for v in todo:
        print("analysing", v["group"], v.get("channel"), v["id"], flush=True)
        try:
            res.append(analyse(v, outdir, cfg.get("max_seconds", 180), cfg.get("scene_threshold", 0.3), cookies))
        except Exception as e:
            v["error"] = repr(e)[-400:]
            res.append(v)
        print("  ->", {k: res[-1].get(k) for k in ("sec_per_shot", "wpm", "error")}, flush=True)
        json.dump({"job": cfg, "log": log, "videos": res}, open(f"{outdir}/results.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
