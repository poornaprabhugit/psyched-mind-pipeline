"""Join rendered long-video segments into one 1920x1080 video at -14 LUFS.

Usage: python scripts/join_long.py <render.json> <dir with segment mp4s> <out.mp4>

Reads "long": {"id": "long02", "segments": ["L0", "L1", ...]} from render.json.
Segments are re-encoded to a common format, concatenated without gaps, then
loudness-normalised (two-pass loudnorm, I=-14, TP=-1.5, LRA=11).
Writes <out>.chapters.txt with the start time of every segment.
"""
import json
import os
import subprocess
import sys


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
              capture_output=True, text=True).stdout.strip()
    return float(out)


def main(job_path, seg_dir, out):
    job = json.load(open(job_path, encoding="utf-8"))
    segs = job["long"]["segments"]
    titles = {v["id"]: v.get("chapter") or v.get("title_card") or v.get("subject", v["id"]) for v in job["videos"]}
    work = os.path.join(os.path.dirname(os.path.abspath(out)), "_join")
    os.makedirs(work, exist_ok=True)
    norm, t, chapters = [], 0.0, []
    for s in segs:
        src = os.path.join(seg_dir, f"{s}.mp4")
        dst = os.path.join(work, f"{s}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-i", src,
             "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p",
             "-af", "aresample=44100,aformat=channel_layouts=stereo",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k", dst])
        chapters.append((t, titles.get(s, s)))
        t += duration(dst)
        norm.append(dst)
    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        for p in norm:
            f.write(f"file '{p}'\n")
    joined = os.path.join(work, "joined.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
    # two-pass loudnorm to -14 LUFS
    meas = run(["ffmpeg", "-hide_banner", "-i", joined, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          "aresample=44100")
    run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", out])
    with open(out + ".chapters.txt", "w", encoding="utf-8") as f:
        for start, title in chapters:
            mm, ss = divmod(int(start), 60)
            f.write(f"{mm:02d}:{ss:02d} {title}\n")
    print(open(out + ".chapters.txt").read())
    print(f"total {t:.1f} s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
