"""Render one video with a running MoneyPrinterTurbo API (http://127.0.0.1:8080).

Usage: python scripts/render.py jobs/<batch>/render.json <video_id> <mpt_dir> <outdir>

render.json:
{"videos": [{"id": "v01", "subject": "...", "script": "...", "clips": ["https://cdn.pixabay.com/...mp4", ...]}],
 "settings": {optional overrides of DEFAULTS}}
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


def add_hook(src, dst, text, mpt_dir, seconds=2.5):
    """Burn a bold yellow hook card near the top for the first seconds (stops the scroll, works muted)."""
    import subprocess
    import textwrap
    lines = textwrap.wrap(text, 22)[:3]
    font = os.path.join(mpt_dir, "resource", "fonts", "MicrosoftYaHeiBold.ttc")
    filters = []
    for i, line in enumerate(lines):
        tf = os.path.join(os.path.dirname(dst), f"hook_{i}.txt")
        open(tf, "w", encoding="utf-8").write(line)
        y = f"h*0.14+{i}*96"
        filters.append(
            f"drawtext=fontfile='{font}':textfile='{tf}':fontsize=72:fontcolor=black:"
            f"box=1:boxcolor=0xFFE600:boxborderw=18:x=(w-text_w)/2:y={y}:"
            f"enable='lt(t,{seconds})'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", ",".join(filters),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", dst], check=True)
    for i in range(len(lines)):
        os.remove(os.path.join(os.path.dirname(dst), f"hook_{i}.txt"))


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
            if video.get("hook_text"):
                add_hook(src, dst, video["hook_text"], mpt_dir)
            else:
                shutil.copy(src, dst)
            json.dump({"id": vid, "task_id": task_id, "seconds": int(time.time() - start)},
                      open(os.path.join(outdir, f"{vid}.json"), "w"))
            return
        if d.get("state") == -1:
            raise RuntimeError(f"render failed: {d.get('failed_stage')} {d.get('error')}")
        time.sleep(20)
    raise RuntimeError("render timed out")


if __name__ == "__main__":
    main(*sys.argv[1:5])
