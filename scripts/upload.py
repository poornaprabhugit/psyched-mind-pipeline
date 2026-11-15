"""Upload finished videos to the channel as PRIVATE (optionally scheduled with publishAt).

Usage: python scripts/upload.py jobs/<batch>/upload.json <video_dir> uploads/<batch>.json

upload.json:
{
  "videos": [
    {"key": "B01", "file": "n01.mp4", "title": "...", "description": "...", "tags": ["..."],
     "publish_at": "2026-11-23T11:00:00Z",      # optional; omit = stays private until the user acts
     "category_id": "27",                       # optional, 27 = Education
     "synthetic": false,                        # status.containsSyntheticMedia (altered/synthetic disclosure)
     "thumbnail": "thumb_a.png",                # optional (long videos), file in video_dir
     "playlist_id": "PL..."}                    # optional
  ]
}

Safety rules built in:
- privacyStatus is ALWAYS "private". Nothing goes public unless publish_at is set (YouTube then
  publishes at that time) or the user publishes it in Studio.
- Every video is made-for-kids = false.
- A key already in the results file is skipped, so re-running a job never creates duplicates.
Needs YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN with the youtube.upload scope.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from stats import access_token  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"


def call(method, url, token, body=None, headers=None, raw=None):
    h = {"Authorization": f"Bearer {token}"}
    h.update(headers or {})
    data = raw
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json; charset=UTF-8"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            text = r.read().decode() or "{}"
            return r.status, dict(r.headers), json.loads(text)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), {"error": e.read().decode()[:800]}


def upload_one(token, v, video_dir):
    path = os.path.join(video_dir, v["file"])
    size = os.path.getsize(path)
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": bool(v.get("synthetic", False))}
    if v.get("publish_at"):
        status["publishAt"] = v["publish_at"]
    meta = {"snippet": {"title": v["title"][:100], "description": v.get("description", "")[:5000],
                        "tags": v.get("tags", []), "categoryId": v.get("category_id", "27"),
                        "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": status}
    url = f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status&notifySubscribers=true"
    code, hdrs, resp = call("POST", url, token, body=meta, headers={
        "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = hdrs.get("Location") or hdrs.get("location")
    if code != 200 or not loc:
        return {"ok": False, "step": "start", "code": code, "resp": resp}
    with open(path, "rb") as f:
        code, _, resp = call("PUT", loc, token, raw=f.read(), headers={"Content-Type": "video/mp4"})
    if code not in (200, 201) or "id" not in resp:
        return {"ok": False, "step": "upload", "code": code, "resp": resp}
    out = {"ok": True, "id": resp["id"], "url": f"https://youtube.com/shorts/{resp['id']}",
           "privacy": resp.get("status", {}).get("privacyStatus"),
           "publish_at": resp.get("status", {}).get("publishAt")}
    if v.get("thumbnail"):
        with open(os.path.join(video_dir, v["thumbnail"]), "rb") as f:
            c, _, r = call("POST", f"{UPLOAD}/thumbnails/set?videoId={resp['id']}", token,
                           raw=f.read(), headers={"Content-Type": "image/png"})
        out["thumbnail"] = "ok" if c == 200 else f"failed {c}: {r}"
    if v.get("playlist_id"):
        c, _, r = call("POST", f"{API}/playlistItems?part=snippet", token, body={"snippet": {
            "playlistId": v["playlist_id"], "resourceId": {"kind": "youtube#video", "videoId": resp["id"]}}})
        out["playlist"] = "ok" if c == 200 else f"failed {c}: {r}"
    return out


def main(job_path, video_dir, results_path):
    job = json.load(open(job_path))
    results = json.load(open(results_path)) if os.path.exists(results_path) else {}
    token = access_token()
    for v in job["videos"]:
        key = v["key"]
        if results.get(key, {}).get("ok"):
            print(f"{key}: already uploaded ({results[key]['id']}), skipped", flush=True)
            continue
        r = upload_one(token, v, video_dir)
        r["title"] = v["title"]
        results[key] = r
        print(f"{key}: {json.dumps(r)}", flush=True)
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        json.dump(results, open(results_path, "w"), indent=2)
    bad = [k for k, r in results.items() if not r.get("ok")]
    print(f"done: {len(results) - len(bad)} ok, {len(bad)} failed {bad}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
