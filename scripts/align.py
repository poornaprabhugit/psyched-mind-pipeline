"""Sentence-aligned video assembly (long videos).

MoneyPrinterTurbo lays clips end to end at a fixed clip length, so on a 90-second segment
clip N drifts away from the line it was picked for (long 02, 14 Nov: many off-topic frames).
This module rebuilds the picture from MPT's own narration (audio.mp3) and sentence subtitles
(subtitle.srt): every script line gets exactly the clips picked for it, cut to that line's
spoken duration, and the subtitles are burned as full sentences (not word by word).

render.json, per video:  "lines": [{"text": "<one sentence>", "clips": ["<url>", ...]}, ...]
(the script is the lines joined by spaces) and optionally "subtitle_style": {...} (ASS overrides).
"""
import json
import os
import re
import subprocess
import sys


def _dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout.strip())


def _t(s):
    h, m, rest = s.strip().replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def parse_srt(path):
    items = []
    for block in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
        rows = [r for r in block.splitlines() if r.strip()]
        tl = next((i for i, r in enumerate(rows) if "-->" in r), None)
        if tl is None:
            continue
        a, b = rows[tl].split("-->")
        items.append({"start": _t(a), "end": _t(b), "text": " ".join(rows[tl + 1:])})
    return items


def _words(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("'", ""))


def line_times(lines, srt, total):
    """Start/end time of each script line, by walking the subtitle entries word by word."""
    counts = [len(_words(l["text"])) for l in lines]
    starts, done, li, acc = [], 0, 0, 0
    for e in srt:
        if li < len(lines) and acc == 0:
            starts.append(e["start"])
        acc += len(_words(e["text"]))
        while li < len(lines) and acc >= counts[li] - 0.5:
            acc -= counts[li]
            li += 1
            if acc > 0 and li < len(lines):
                starts.append(e["start"])  # line began inside this entry (rare)
        done = e["end"]
    while len(starts) < len(lines):  # fallback: spread the rest evenly
        starts.append(starts[-1] + 1.0 if starts else 0.0)
    starts[0] = 0.0
    ends = starts[1:] + [total]
    return list(zip(starts, ends))


def _render_piece(src, seconds, w, h, out, is_image=False):
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30,format=yuv420p,setsar=1"
    if is_image:  # slow push-in on a still photo
        frames = max(int(seconds * 30), 1)
        vf = (f"scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
              f"zoompan=z='min(zoom+0.0008,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps=30,"
              "format=yuv420p,setsar=1")
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src, "-t", f"{seconds:.3f}", "-vf", vf]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", src, "-t", f"{seconds:.3f}", "-vf", vf]
    subprocess.run(cmd + ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out], check=True)


DEFAULT_STYLE = {  # sentence subtitles: white, bold, thin outline, bottom centre, ~2 lines max
    "Fontname": "Microsoft YaHei", "Bold": "1", "FontSize": "17", "PrimaryColour": "&H00FFFFFF",
    "OutlineColour": "&H00000000", "BackColour": "&H80000000", "BorderStyle": "1", "Outline": "1.4",
    "Shadow": "0.8", "Alignment": "2", "MarginV": "16", "MarginL": "40", "MarginR": "40", "WrapStyle": "0",
}


def build(task_dir, lines, clip_paths, out, aspect="16:9", fonts_dir=None, style=None, min_piece=2.5):
    """lines: [{"text"}], clip_paths: list (per line) of local clip files. Writes `out` (video + MPT audio + subtitles)."""
    w, h = (1920, 1080) if aspect == "16:9" else (1080, 1920)
    audio = os.path.join(task_dir, "audio.mp3")
    srt_path = os.path.join(task_dir, "subtitle.srt")
    total = _dur(audio)
    srt = parse_srt(srt_path)
    times = line_times(lines, srt, total)
    work = out + ".pieces"
    os.makedirs(work, exist_ok=True)
    pieces, log = [], []
    for i, ((a, b), clips) in enumerate(zip(times, clip_paths)):
        d = max(b - a, 0.2)
        k = max(1, min(len(clips), int(d // min_piece) or 1))
        for j in range(k):
            seg = d / k
            p = os.path.join(work, f"{i:03d}_{j}.mp4")
            src = clips[j]
            _render_piece(src, seg, w, h, p, is_image=src.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
            pieces.append(p)
        log.append({"line": i, "start": round(a, 2), "end": round(b, 2), "clips_used": k, "clips_given": len(clips),
                    "text": lines[i]["text"][:60]})
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pieces))
    silent = os.path.join(work, "silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent],
                   check=True)
    st = dict(DEFAULT_STYLE, **(style or {}))
    force = ",".join(f"{k}={v}" for k, v in st.items())
    sub = f"subtitles='{srt_path}':original_size={w}x{h}:force_style='{force}'"
    if fonts_dir:
        sub += f":fontsdir='{fonts_dir}'"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", audio, "-vf", sub, "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out], check=True)
    json.dump(log, open(out + ".align.json", "w"), indent=1)
    for p in pieces + [lst, silent]:
        os.remove(p)
    os.rmdir(work)
    return log


if __name__ == "__main__":  # python align.py <task_dir> <lines.json> <out.mp4>  (lines.json: [{"text","files":[...]}])
    t, lj, o = sys.argv[1:4]
    L = json.load(open(lj))
    print(json.dumps(build(t, L, [l["files"] for l in L], o), indent=1))
