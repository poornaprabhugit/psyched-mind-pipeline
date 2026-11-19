"""Checkpoint snapshots of every public Short at ~3 h, ~24 h and ~7 days after it went live.

User decision 19 Nov 2026: instead of hourly checks, take a few fixed snapshots so we can
tell an early spike from a slow climb and line them up with retention/likes/subs.

Runs twice a day (workflow snapshots.yml, ~15:10 and ~19:10 Amsterdam), which lands each
12:00 / 16:00 Short at ~3 h on its first day, ~23-27 h the next day and ~167-171 h on day 7.
Each checkpoint is written once per video to memory/stats/snapshots.csv.

Live counts (views, likes, comments) come from the Data API and are current.
Analytics metrics (avg % viewed, engaged views, subscribers gained, shares) lag 1-3 days in
the API, so they are only recorded at the 7-day checkpoint (empty at 3 h / 24 h).
YouTube Studio's "stayed to watch" % is not available in the API; engaged_views / views is
the closest API proxy, not the same number.
"""
import csv
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats import access_token, get, report  # noqa: E402

# checkpoint name -> (min age h, max age h)
CHECKPOINTS = {"3h": (2, 6), "24h": (20, 30), "7d": (160, 176)}
FIELDS = ["video_id", "title", "checkpoint", "published", "taken_at", "age_h", "views", "likes",
          "comments", "engaged_views", "avg_view_pct", "avg_view_s", "subs_gained", "shares"]


def iso_dur_s(d):
    # PT#M#S -> seconds (Shorts are < 3 min)
    d = d.replace("PT", "")
    s = 0
    for unit, mult in (("H", 3600), ("M", 60), ("S", 1)):
        if unit in d:
            n, d = d.split(unit, 1)
            s += int(n) * mult
    return s


def main(path):
    token = access_token()
    now = dt.datetime.now(dt.timezone.utc)
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            done = {(r["video_id"], r["checkpoint"]) for r in csv.DictReader(f)}

    ch = get("https://www.googleapis.com/youtube/v3/channels", token, {"part": "contentDetails", "mine": "true"})
    uploads = (ch.get("items") or [{}])[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if not uploads:
        print("no uploads playlist:", ch)
        return 1
    pl = get("https://www.googleapis.com/youtube/v3/playlistItems", token,
             {"part": "contentDetails", "playlistId": uploads, "maxResults": 50})
    ids = [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
    v = get("https://www.googleapis.com/youtube/v3/videos", token,
            {"part": "snippet,statistics,contentDetails,status", "id": ",".join(ids)}) if ids else {}

    rows = []
    for it in v.get("items", []):
        if it["status"]["privacyStatus"] != "public" or iso_dur_s(it["contentDetails"]["duration"]) > 180:
            continue
        pub = dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
        age = (now - pub).total_seconds() / 3600
        for cp, (lo, hi) in CHECKPOINTS.items():
            if lo <= age < hi and (it["id"], cp) not in done:
                st = it.get("statistics", {})
                row = {"video_id": it["id"], "title": it["snippet"]["title"], "checkpoint": cp,
                       "published": pub.isoformat(), "taken_at": now.isoformat(timespec="minutes"),
                       "age_h": round(age, 1), "views": st.get("viewCount", ""),
                       "likes": st.get("likeCount", ""), "comments": st.get("commentCount", "")}
                if cp == "7d":
                    a = report(token, pub.date().isoformat(), now.date().isoformat(),
                               "views,engagedViews,averageViewPercentage,averageViewDuration,subscribersGained,shares",
                               dimensions="video", filters="video==" + it["id"])
                    if isinstance(a, list) and a:
                        a = a[0]
                        row.update({"engaged_views": a.get("engagedViews", ""),
                                    "avg_view_pct": a.get("averageViewPercentage", ""),
                                    "avg_view_s": a.get("averageViewDuration", ""),
                                    "subs_gained": a.get("subscribersGained", ""),
                                    "shares": a.get("shares", "")})
                    elif isinstance(a, dict):
                        print("analytics error for", it["id"], a)
                rows.append(row)

    if rows:
        new = not os.path.exists(path)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerows(rows)
    for r in rows:
        print(f"{r['checkpoint']:>3}  {r['age_h']:>6}h  views {r['views']:>6}  likes {r['likes']:>4}  {r['title']}")
    print("snapshots written:", len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "memory/stats/snapshots.csv"))
