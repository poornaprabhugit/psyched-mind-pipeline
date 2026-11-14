"""Search Pixabay for candidate clips for every script line and build contact sheets.

Usage: python scripts/search.py jobs/<batch>/search.json <outdir>

search.json:
{"videos": [{"id": "v01", "aspect": "9:16" (default) or "16:9", "lines": [{"n": 1, "text": "...", "queries": ["shy", "awkward man"]}, ...]}]}

Writes <outdir>/<video>_candidates.json and <outdir>/<video>_sheet_<k>.jpg
(each sheet shows up to 5 lines x 8 candidates, labelled L<line>-<candidate>,
thumbnails cropped to 9:16 the way MoneyPrinterTurbo will crop them).
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

KEY = os.environ.get("PIXABAY_API_KEY", "")
BAD = ("ai generated", "ai-generated", "cartoon", "animation", "animated", "3d", "render",
       "green screen", "greenscreen", "chroma", "illustration", "vector", "loop video")
PER_LINE = 8
TW, TH = 180, 320  # 9:16 thumbnail cell


def get(url, binary=False, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "psyched-mind-pipeline"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:  # retry transient 5xx / timeouts
            print(f"  retry {i+1} {url[:80]}: {e}", flush=True)
            time.sleep(3 * (i + 1))
    return None


def search(q):
    params = urllib.parse.urlencode({"key": KEY, "q": q[:100], "video_type": "film",
                                     "per_page": 30, "safesearch": "true"})
    data = get(f"https://pixabay.com/api/videos/?{params}")
    return (data or {}).get("hits", [])


def ok(hit):
    text = (hit.get("tags", "") + " " + hit.get("pageURL", "")).lower()
    return hit.get("duration", 0) >= 3 and not any(b in text for b in BAD)


def pick_url(v):
    large = v.get("large") or {}
    if large.get("url") and (large.get("size") or 0) < 40_000_000 and large.get("width", 0) >= 1280:
        return large["url"]
    return (v.get("medium") or {}).get("url") or large.get("url")


def thumb(v):
    for k in ("small", "medium", "large", "tiny"):
        t = (v.get(k) or {}).get("thumbnail")
        if t:
            return t
    return None


def crop916(img, landscape=False):
    w, h = img.size
    if landscape:  # 16:9 cell for long videos
        th = int(w * 9 / 16)
        if th < h:
            y = (h - th) // 2
            img = img.crop((0, y, w, y + th))
        return img.resize((TH, TW))
    tw = int(h * 9 / 16)
    if tw < w:
        x = (w - tw) // 2
        img = img.crop((x, 0, x + tw, h))
    return img.resize((TW, TH))


def main(job_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    job = json.load(open(job_path, encoding="utf-8"))
    used = set()
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    for video in job["videos"]:
        vid = video["id"]
        result = {"id": vid, "lines": []}
        for line in video["lines"]:
            cands = []
            for q in line["queries"]:
                for hit in search(q):
                    if hit["id"] in used or any(c["pixabay_id"] == hit["id"] for c in cands) or not ok(hit):
                        continue
                    url, th = pick_url(hit["videos"]), thumb(hit["videos"])
                    if url and th:
                        cands.append({"pixabay_id": hit["id"], "url": url, "thumb": th,
                                      "page": hit.get("pageURL"), "tags": hit.get("tags"),
                                      "duration": hit.get("duration"), "query": q})
                    if len(cands) >= PER_LINE:
                        break
                if len(cands) >= PER_LINE:
                    break
            result["lines"].append({"n": line["n"], "text": line["text"], "candidates": cands})
            print(f"{vid} L{line['n']}: {len(cands)} candidates", flush=True)
        json.dump(result, open(f"{outdir}/{vid}_candidates.json", "w"), indent=1)
        # contact sheets, 5 lines per sheet
        lines = result["lines"]
        land = video.get("aspect") == "16:9"
        cw, ch = (TH, TW) if land else (TW, TH)
        for s in range(0, len(lines), 5):
            chunk = lines[s:s + 5]
            sheet = Image.new("RGB", (PER_LINE * (cw + 6) + 6, len(chunk) * (ch + 36) + 6), (17, 17, 20))
            d = ImageDraw.Draw(sheet)
            for r, line in enumerate(chunk):
                y = 6 + r * (ch + 36)
                d.text((8, y), f"L{line['n']}: {line['text'][:110]}", fill=(255, 230, 0), font=font)
                for c, cand in enumerate(line["candidates"]):
                    data = get(cand["thumb"], binary=True)
                    if not data:
                        continue
                    try:
                        img = crop916(Image.open(io.BytesIO(data)).convert("RGB"), land)
                    except Exception:
                        continue
                    x = 6 + c * (cw + 6)
                    sheet.paste(img, (x, y + 30))
                    d.rectangle((x, y + 30, x + 64, y + 58), fill=(0, 0, 0))
                    d.text((x + 4, y + 32), f"{line['n']}-{c}", fill=(255, 255, 255), font=font)
            sheet.save(f"{outdir}/{vid}_sheet_{s // 5 + 1}.jpg", quality=80)


if __name__ == "__main__":
    if not KEY:
        sys.exit("PIXABAY_API_KEY secret is missing")
    main(sys.argv[1], sys.argv[2])
