"""Collect YouTube stats for the channel and save them to memory/stats/<date>.json.

Needs secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (OAuth with scopes
youtube.readonly + yt-analytics.readonly, authorised on the channel's account).
"""
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request


def post_form(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def get(url, token, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": e.read().decode()[:500]}


def access_token():
    return post_form("https://oauth2.googleapis.com/token", {
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"})["access_token"]


def report(token, start, end, metrics, dimensions=None, filters=None, sort=None):
    p = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": metrics}
    if dimensions:
        p["dimensions"] = dimensions
    if filters:
        p["filters"] = filters
    if sort:
        p["sort"] = sort
    r = get("https://youtubeanalytics.googleapis.com/v2/reports", token, p)
    if "error" in r:
        return r
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]


def main(outdir):
    token = access_token()
    today = dt.date.today()
    start = "2026-11-01"
    end = today.isoformat()
    data = {"collected_at": dt.datetime.now(dt.timezone.utc).isoformat(), "note": "Analytics data lags 1-3 days"}

    ch = get("https://www.googleapis.com/youtube/v3/channels", token,
             {"part": "snippet,statistics,contentDetails", "mine": "true"})
    item = (ch.get("items") or [{}])[0]
    data["channel"] = {"title": item.get("snippet", {}).get("title"), "statistics": item.get("statistics")}
    uploads = item.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")

    videos = []
    if uploads:
        pl = get("https://www.googleapis.com/youtube/v3/playlistItems", token,
                 {"part": "contentDetails", "playlistId": uploads, "maxResults": 50})
        ids = [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        if ids:
            v = get("https://www.googleapis.com/youtube/v3/videos", token,
                    {"part": "snippet,statistics,contentDetails,status", "id": ",".join(ids)})
            for it in v.get("items", []):
                videos.append({"id": it["id"], "title": it["snippet"]["title"],
                               "published": it["snippet"]["publishedAt"],
                               "privacy": it["status"]["privacyStatus"],
                               "duration": it["contentDetails"]["duration"],
                               "statistics": it.get("statistics", {})})
    data["videos"] = videos

    if videos:
        f = "video==" + ",".join(v["id"] for v in videos)
        data["per_video"] = report(token, start, end,
                                   "views,engagedViews,estimatedMinutesWatched,averageViewDuration,"
                                   "averageViewPercentage,likes,comments,shares,subscribersGained",
                                   dimensions="video", filters=f, sort="-views")
        if isinstance(data["per_video"], dict):  # fall back if a metric is not available
            data["per_video"] = report(token, start, end,
                                       "views,estimatedMinutesWatched,averageViewDuration,"
                                       "averageViewPercentage,likes,comments,shares,subscribersGained",
                                       dimensions="video", filters=f, sort="-views")
    data["daily"] = report(token, start, end, "views,subscribersGained,estimatedMinutesWatched", dimensions="day")
    data["traffic_sources"] = report(token, start, end, "views,averageViewDuration",
                                     dimensions="insightTrafficSourceType", sort="-views")
    data["countries"] = report(token, start, end, "views", dimensions="country", sort="-views")

    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{today.isoformat()}.json")
    json.dump(data, open(path, "w"), indent=1)
    json.dump(data, open(os.path.join(outdir, "latest.json"), "w"), indent=1)
    print("saved", path, "videos:", len(videos))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "memory/stats")
