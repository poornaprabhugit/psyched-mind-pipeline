"""Collect public posting data for top channels (fact base for scheduling decisions).

Input: jobs/research/<name>.json {"queries":[...], "handles":[...], "per_query":10, "uploads":200}
Output: research/<name>.json with, per channel: id, title, country, subs, views, and its last N uploads
(publishedAt UTC, duration seconds, views, likes, comments, title).
Uses the same OAuth secrets as stats.py (youtube.readonly is enough for public data).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from stats import access_token, get

API = "https://www.googleapis.com/youtube/v3/"


def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m:
        return None
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def main(job, out):
    cfg = json.load(open(job))
    tok = access_token()
    ids, log = {}, []
    for q in cfg.get("queries", []):
        r = get(API + "search", tok, {"part": "snippet", "q": q, "type": "channel", "order": "relevance",
                                         "maxResults": cfg.get("per_query", 10), "relevanceLanguage": "en"})
        log.append({"query": q, "error": r.get("error")})
        for it in r.get("items", []):
            ids.setdefault(it["snippet"]["channelId"], f"search:{q}")
    for h in cfg.get("handles", []):
        r = get(API + "channels", tok, {"part": "id", "forHandle": h})
        for it in r.get("items", []):
            ids.setdefault(it["id"], f"handle:{h}")
        if not r.get("items"):
            log.append({"handle": h, "found": False, "error": r.get("error")})
    chans = []
    idl = list(ids)
    for i in range(0, len(idl), 50):
        r = get(API + "channels", tok, {"part": "snippet,statistics,contentDetails", "id": ",".join(idl[i:i + 50])})
        for it in r.get("items", []):
            st = it.get("statistics", {})
            chans.append({"id": it["id"], "found_by": ids[it["id"]], "title": it["snippet"]["title"],
                          "handle": it["snippet"].get("customUrl"), "country": it["snippet"].get("country"),
                          "subs": int(st.get("subscriberCount", 0) or 0), "views": int(st.get("viewCount", 0) or 0),
                          "videos": int(st.get("videoCount", 0) or 0),
                          "uploads_pl": it["contentDetails"]["relatedPlaylists"]["uploads"]})
    min_subs = cfg.get("min_subs", 100000)
    chans = [c for c in chans if c["subs"] >= min_subs or c["found_by"].startswith("handle:")]
    chans.sort(key=lambda c: -c["subs"])
    chans = chans[:cfg.get("max_channels", 40)]
    for c in chans:
        vids, page = [], None
        while len(vids) < cfg.get("uploads", 200):
            p = {"part": "contentDetails", "playlistId": c["uploads_pl"], "maxResults": 50}
            if page:
                p["pageToken"] = page
            r = get(API + "playlistItems", tok, p)
            vids += [it["contentDetails"]["videoId"] for it in r.get("items", [])]
            page = r.get("nextPageToken")
            if not page or "error" in r:
                break
        ups = []
        for i in range(0, len(vids), 50):
            r = get(API + "videos", tok, {"part": "snippet,contentDetails,statistics", "id": ",".join(vids[i:i + 50])})
            for it in r.get("items", []):
                st = it.get("statistics", {})
                ups.append({"id": it["id"], "published": it["snippet"]["publishedAt"],
                            "title": it["snippet"]["title"][:120], "dur": dur(it["contentDetails"].get("duration")),
                            "lang": it["snippet"].get("defaultAudioLanguage") or it["snippet"].get("defaultLanguage"),
                            "views": int(st.get("viewCount", 0) or 0), "likes": int(st.get("likeCount", 0) or 0),
                            "comments": int(st.get("commentCount", 0) or 0)})
        c["uploads"] = ups
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"channels": chans, "log": log}, open(out, "w"), indent=0, ensure_ascii=False)
    print(len(chans), "channels", sum(len(c.get("uploads", [])) for c in chans), "uploads")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
