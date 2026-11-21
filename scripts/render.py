"""Render one video with a running MoneyPrinterTurbo API (http://127.0.0.1:8080).

Usage: python scripts/render.py jobs/<batch>/render.json <video_id> <mpt_dir> <outdir>

render.json:
{"videos": [{"id": "v01", "subject": "...", "script": "...", "clips": ["https://cdn.pixabay.com/...mp4", ...],
             optional: "hook_text", "cta_text", "follow_text" (+ "follow_text_clean" for IG/FB), "title_card", "fast_open": {"clips": 3, "seconds": 1.5},
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
    if url.startswith("repo:"):  # a file committed in this repo (e.g. code-drawn diagrams for long videos)
        shutil.copy(url[5:], target)
        return
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
                 cta_seconds=2.5, title_seconds=4.0, follow=None):
    """Burn text cards in one ffmpeg pass (black on #FFE600, brand style):
    hook  = big card near the top for the first seconds (Shorts; stops the scroll, works muted)
    cta   = small card near the bottom for the last seconds (points to the Related video link)
    title = item title card top-left for the first seconds (long-video segments)
    follow = small subscribe/follow card above the cta for the same last seconds (P1 conversion test, 20 Nov)."""
    import subprocess
    font = os.path.join(mpt_dir, "resource", "fonts", "MicrosoftYaHeiBold.ttc")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True, check=True).stdout.strip())
    tmp, filters = [], []

    def card(text, size, x, y, enable, border):
        tf = os.path.join(os.path.dirname(os.path.abspath(dst)), f"card_{len(tmp)}.txt")
        open(tf, "w", encoding="utf-8").write(text)
        tmp.append(tf)
        filters.append(f"drawtext=fontfile='{font}':textfile='{tf}':expansion=none:fontsize={size}:fontcolor=black:"
                       f"box=1:boxcolor=0xFFE600:boxborderw={border}:x={x}:y={y}:enable='{enable}'")

    if hook:
        for i, line in enumerate(_wrap_cards(hook, 22)):
            card(line, 72, "(w-text_w)/2", f"h*0.14+{i}*96", f"lt(t,{hook_seconds})", 18)
    if follow:
        card(follow, 40, "(w-text_w)/2", "h*0.62", f"gt(t,{max(dur - cta_seconds, 0):.2f})", 14)
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


def tighten(src, dst, max_gap=0.35, noise="-33dB", min_detect=0.4, tail=0.25):
    """Shorten pauses between sentences to `max_gap` s and cut dead air at the end (keep `tail` s).
    Cuts video and audio together, so captions stay in sync."""
    import re, subprocess
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"silencedetect=n={noise}:d={min_detect}",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    cuts = []
    for i, st in enumerate(starts):
        en = ends[i] if i < len(ends) else dur
        if st < 0.3:
            continue  # never touch the opening
        if en >= dur - 0.05:  # trailing silence
            cuts.append((st + tail, dur)); continue
        keep_a, keep_b = st + max_gap / 2, en - max_gap / 2
        if keep_b - keep_a > 0.05:
            cuts.append((keep_a, keep_b))
    if not cuts:
        shutil.copy(src, dst); return 0.0
    expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in cuts)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                    "-vf", f"select='not({expr})',setpts=N/FRAME_RATE/TB",
                    "-af", f"aselect='not({expr})',asetpts=N/SR/TB",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k", dst], check=True)
    return sum(b - a for a, b in cuts)


def trim_clip(path, seconds):
    """Cut a clip to its first `seconds` (fast-open: quicker visual changes in the first seconds).
    MPT keeps clips shorter than video_clip_duration whole."""
    import subprocess
    tmp = path + ".trim.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-t", str(seconds), "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", tmp], check=True)
    os.replace(tmp, path)


def pad_to_audio(path):
    """MPT often ends the video track up to ~2.7 s before the audio; hold the last frame so both end together."""
    import subprocess
    def d(kind):
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", kind, "-show_entries", "stream=duration",
                            "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        try:
            return float(o.split()[0])
        except (ValueError, IndexError):
            return None
    v, a = d("v:0"), d("a:0")
    if v is None or a is None or a - v <= 0.05:
        return 0.0
    tmp = path + ".pad.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", f"tpad=stop_mode=clone:stop_duration={a - v:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", tmp], check=True)
    os.replace(tmp, path)
    return a - v


def params_aspect(job, video):
    return video.get("settings", {}).get("video_aspect") or job.get("settings", {}).get("video_aspect") \
        or DEFAULTS["video_aspect"]


def photo_to_clip(path, aspect="9:16", seconds=4.0):
    """A Pixabay photo (search line option "photos": true) becomes a slow push-in clip, so MPT can use it.
    Detects JPEG/PNG/WebP by magic bytes; leaves real videos untouched."""
    import subprocess
    head = open(path, "rb").read(12)
    if not (head[:3] == b"\xff\xd8\xff" or head[:8] == b"\x89PNG\r\n\x1a\n" or head[8:12] == b"WEBP"):
        return False
    w, h = (1080, 1920) if aspect == "9:16" else (1920, 1080)
    frames = int(seconds * 30)
    img = path + ".img"
    os.replace(path, img)
    vf = (f"scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
          f"zoompan=z='min(zoom+0.0010,1.15)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps=30,"
          "format=yuv420p,setsar=1")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", img, "-t", f"{seconds:.2f}", "-vf", vf,
                    "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", path], check=True)
    os.remove(img)
    return True


def main(job_path, vid, mpt_dir, outdir):
    os.makedirs(outdir, exist_ok=True)
    job = json.load(open(job_path, encoding="utf-8"))
    video = next(v for v in job["videos"] if v["id"] == vid)
    local = os.path.join(mpt_dir, "storage", "local_videos")
    os.makedirs(local, exist_ok=True)
    names = []
    lines = video.get("lines")  # sentence-aligned mode (long videos): [{"text", "clips": [urls]}]
    line_files = []
    if lines:
        video["script"] = video.get("script") or " ".join(l["text"] for l in lines)
        seen = {}
        for li, l in enumerate(lines):
            files = []
            for url in l["clips"]:
                if url not in seen:
                    ext = os.path.splitext(url.split("?")[0])[1].lower() or ".mp4"
                    name = f"{vid}_{len(seen) + 1:03d}{ext}"
                    download(url, os.path.join(local, name))
                    seen[url] = name
                    names.append(name)
                files.append(os.path.join(local, seen[url]))
            line_files.append(files)
        names = [n for n in names if n.endswith(".mp4")] or names
    else:
        for i, url in enumerate(video["clips"], 1):
            name = f"{vid}_{i:02d}.mp4"
            download(url, os.path.join(local, name))
            photo_to_clip(os.path.join(local, name), params_aspect(job, video))
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
            if lines:
                import align
                aligned = os.path.join(outdir, f"{vid}_aligned.mp4")
                log = align.build(os.path.join(mpt_dir, "storage", "tasks", task_id), lines, line_files, aligned,
                                  aspect=params.get("video_aspect", "16:9"),
                                  fonts_dir=os.path.join(mpt_dir, "resource", "fonts"),
                                  style=video.get("subtitle_style", job.get("subtitle_style")))
                print(f"aligned {len(log)} lines to their own clips", flush=True)
                src = aligned
            if video.get("tighten", job.get("tighten", False)):
                tight = os.path.join(outdir, f"{vid}_tight.mp4")
                cut = tighten(src, tight, max_gap=float(video.get("tighten_gap", job.get("tighten_gap", 0.35))))
                print(f"tightened: removed {cut:.2f} s of pauses", flush=True)
                src = tight
            cta = video.get("cta_text", job.get("cta_text"))
            follow = video.get("follow_text")
            add_overlays(src, dst, mpt_dir, hook=video.get("hook_text"), cta=cta, title=video.get("title_card"),
                         follow=follow)
            print(f"padded video by {pad_to_audio(dst):.2f} s", flush=True)
            if (cta or follow) and job.get("clean_variant"):
                # Instagram/Facebook version from the same render: no "Full video" card (saves a second render job)
                clean = os.path.join(outdir, f"{vid}_clean.mp4")
                add_overlays(src, clean, mpt_dir, hook=video.get("hook_text"), cta=None, title=video.get("title_card"),
                             follow=video.get("follow_text_clean", follow))
                pad_to_audio(clean)
            for tmpname in (f"{vid}_tight.mp4", f"{vid}_aligned.mp4"):
                if os.path.exists(os.path.join(outdir, tmpname)):
                    os.remove(os.path.join(outdir, tmpname))
            json.dump({"id": vid, "task_id": task_id, "seconds": int(time.time() - start)},
                      open(os.path.join(outdir, f"{vid}.json"), "w"))
            return
        if d.get("state") == -1:
            raise RuntimeError(f"render failed: {d.get('failed_stage')} {d.get('error')}")
        time.sleep(20)
    raise RuntimeError("render timed out")


if __name__ == "__main__":
    main(*sys.argv[1:5])
