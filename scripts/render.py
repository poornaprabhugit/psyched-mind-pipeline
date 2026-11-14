"""Render one video with a running MoneyPrinterTurbo API (http://127.0.0.1:8080).

Usage: python scripts/render.py jobs/<batch>/render.json <video_id> <mpt_dir> <outdir>

render.json:
{"videos": [{"id": "v01", "subject": "...", "script": "...", "clips": ["https://cdn.pixabay.com/...mp4", ...],
             optional: "hook_text", "cta_text", "title_card", "fast_open": {"clips": 3, "seconds": 1.5},
             "settings": {per-video overrides}}],
 "settings": {optional overrides of DEFAULTS}, optional "cta_text", "fast_open",
 optional "long": {"id": "long02", "segments": ["L0", ...]}  -> collect job joins the segments (scripts/join_long.py)}
"""
import json
import os
import shutil
import sys
import time
import urllib.request

DEFAULTS = {
    "video_aspect": "9:16", "video_concat_mode": "sequential", "video_clip_duration": 3, "video_count": 1,
    "voice_name": "en-US-ChristopherNeural-Male", "voice_rate": 1.1, "voice_volume": 1.4,
    "bgm_type": "random", "bgm_volume": 0.2,
    "subtitle_enabled": True, "subtitle_position": "center", "subtitle_display_mode": "word_by_word",
    "subtitle_animation": "pop_spring", "font_name": "MicrosoftYaHeiBold.ttc", "font_size": 80,
    "text_fore_color": "#FFE600", "stroke_color": "#000000", "stroke_width": 4,
}
API = "http://127.0.0.1:8080"


def http(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def download(url, target):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r, open(target, "wb") as f:
                shutil.copyfileobj(r, f)
            return
        except Exception as e:
            print(f"retry {i+1} {url}: {e}", flush=True)
            time.sleep(5)
    raise RuntimeError(f"download failed: {url}")


def _wrap_cards(text, width, max_lines=3):
    import textwrap
    return textwrap.wrap(text, width)[:max_lines]


def add_overlays(src, dst, mpt_dir, hook=None, cta=None, title=None, hook_seconds=2.5,
                 cta_seconds=2.5, title_seconds=4.0):
    """Burn text cards in one ffmpeg pass (black on #FFE600, brand style):
    hook  = big card near the top for the first seconds (Shorts; stops the scroll, works muted)
    cta   = small card near the bottom for the last seconds (points to the Related video link)
    title = item title card top-left for the first seconds (long-video segments)."""
    import subprocess
    font = os.path.join(mpt_dir, "resource", "fonts", "MicrosoftYaHeiBold.ttc")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True, check=True).stdout.strip())
    tmp, filters = [], []

    def card(text, size, x, y, enable, border):
        tf = os.path.join(os.path.dirname(os.path.abspath(dst)), f"card_{len(tmp)}.txt")
        open(tf, "w", encoding="utf-8").write(text)
        tmp.append(tf)
        filters.append(f"drawtext=fontfile='{font}':textfile='{tf}':fontsize={size}:fontcolor=black:"
                       f"box=1:boxcolor=0xFFE600:boxborderw={border}:x={x}:y={y}:enable='{enable}'")

    if hook:
        for i, line in enumerate(_wrap_cards(hook, 22)):
            card(line, 72, "(w-text_w)/2", f"h*0.14+{i}*96", f"lt(t,{hook_seconds})", 18)
    if cta:
        card(cta, 46, "(w-text_w)/2", "h*0.70", f"gt(t,{max(dur - cta_seconds, 0):.2f})", 14)
    if title:
        for i, line in enumerate(_wrap_cards(title, 34, 2)):
            card(line, 58, "60", f"60+{i}*84", f"lt(t,{title_seconds})", 16)
    if not filters:
        shutil.copy(src, dst)
        return
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", ",".join(filters),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", dst], check=True)
    for tf in tmp:
        os.remove(tf)


def add_hook(src, dst, text, mpt_dir, seconds=2.5):
    add_overlays(src, dst, mpt_dir, hook=text, hook_seconds=seconds)


def trim_clip(path, seconds):
    """Cut a clip to its first `seconds` (fast-open: quicker visual changes in the first seconds).
    MPT keeps clips shorter than video_clip_duration whole."""
    import subprocess
    tmp = path + ".trim.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-t", str(seconds), "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", tmp], check=True)
    os.replace(tmp, path)


def main(job_path, vid, mpt_dir, outdir):
    os.makedirs(outdir, exist_ok=True)
    job = json.load(open(job_path, encoding="utf-8"))
    video = next(v for v in job["videos"] if v["id"] == vid)
    local = os.path.join(mpt_dir, "storage", "local_videos")
    os.makedirs(local, exist_ok=True)
    names = []
    for i, url in enumerate(video["clips"], 1):
        name = f"{vid}_{i:02d}.mp4"
        download(url, os.path.join(local, name))
        names.append(name)
    print(f"downloaded {len(names)} clips", flush=True)
    fast = video.get("fast_open", job.get("fast_open", 0))  # e.g. {"clips": 3, "seconds": 1.5}
    if fast:
        for n in names[:fast.get("clips", 3)]:
            trim_clip(os.path.join(local, n), fast.get("seconds", 1.5))

    params = dict(DEFAULTS, **job.get("settings", {}), **video.get("settings", {}))
    params.update({
        "video_subject": video["subject"], "video_script": video["script"], "video_terms": ["psychology"],
        "video_source": "local",
        "video_materials": [{"provider": "local", "url": n, "duration": 0} for n in names],
    })
    for _ in range(60):  # wait for API
        try:
            http("GET", "/ping")
            break
        except Exception:
            time.sleep(5)
    task_id = http("POST", "/api/v1/videos", params)["data"]["task_id"]
    print("task", task_id, flush=True)
    start = time.time()
    while time.time() - start < 45 * 60:
        d = http("GET", f"/api/v1/tasks/{task_id}")["data"]
        print(f"state={d.get('state')} progress={d.get('progress')}", flush=True)
        if d.get("state") == 1:
            src = os.path.join(mpt_dir, "storage", "tasks", task_id, "final-1.mp4")
            dst = os.path.join(outdir, f"{vid}.mp4")
            add_overlays(src, dst, mpt_dir, hook=video.get("hook_text"),
                         cta=video.get("cta_text", job.get("cta_text")), title=video.get("title_card"))
            json.dump({"id": vid, "task_id": task_id, "seconds": int(time.time() - start)},
                      open(os.path.join(outdir, f"{vid}.json"), "w"))
            return
        if d.get("state") == -1:
            raise RuntimeError(f"render failed: {d.get('failed_stage')} {d.get('error')}")
        time.sleep(20)
    raise RuntimeError("render timed out")


if __name__ == "__main__":
    main(*sys.argv[1:5])
