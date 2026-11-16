# Lessons

- Hand-pick clips visually; auto-search returns cartoons/AI clips.
- Render max 2 at a time locally; cloud renders in parallel runners.
- Supply ~12 clips per video; 10 clips for a 32 s voiceover made MPT loop back to clip 1 at the end.
- Cloud render: ~4-7 min per video after ~5 min setup.
- Hook card (yellow, first 2.5 s) added after YouTube Studio advice: stayed ~44% on early Shorts.
- Thumbnails: custom uploads for Shorts are YPP-only (since Jul 2026); until then pick the frame in the YouTube app. Choose a frame at ~0:01 that shows the yellow hook card + an expressive face (YT's auto frames show random caption words like "to"/"one"). Plan clip 1 so that frame works, and note the timestamp in the upload sheet. Thumbnails matter on the channel page/home, not in the Shorts feed.
- 2026-11-12: YouTube Analytics API returns empty reports for the first ~2–3 days of a new channel (not an error); "stayed to watch / viewed vs swiped" is not in the API at all — get it from Studio. Scheduled videos show as "private" in the Data API until they go live (collector now records publish_at).
- 2026-11-12: First 3 Shorts each got a day-1 test burst (34–51 views) and then stalled (+0/+12 next day) → the Shorts feed did not widen distribution; hook/first 3 s is the main lever. No public Short has had the hook card yet.
- 2026-11-12 (Studio screenshot): 102 views but only 0.1 watch hours in 28 days → roughly 3–5 s watched per view on ~30 s Shorts. Most viewers leave in the first seconds = hook problem, not body. Favor trick: 15 views in first 7 h; fresh start: 4 views in 25 h (posted 6 h after IKEA, no hook card).
- 2026-11-12: Fresh start Short: no copyright claim; 5 views in 48 h = 3 Shorts feed, 1 search, 1 other. It DID get a (tiny) Shorts-feed test and was swiped → not a technical/distribution fault. "Viewed vs swiped" is not shown in Studio at this volume.
- 2026-11-12 (long video 01): built as 8 MPT segments (16:9, clip_duration 4) rendered in parallel, then ffmpeg concat + loudnorm −14 LUFS. MPT holds each clip ~5–7 s when clips are short, so fewer clips are used than supplied and visuals drift behind the voice – supply clips per line but expect drift; ~1,270 words ≈ 7:17. Some Pixabay clips open with a 0.2 s black frame → patch with a still overlay after render. Pixabay CDN is blocked from the Claude sandbox; thumbnail backgrounds come from rendered frames (crop out the burned-in captions).
- Don't push two render.json commits back to back: both runs start and burn minutes; cancel the stale run.
- 2026-11-13: Re-uploads replaced the 4 old scheduled Shorts (new IDs). First Analytics rows arrived after ~3 days (mere exposure: 34 views, 8 engaged views = 24%, 27 s AVD only for the minority who watched; Shorts feed avg 7 s vs channel page 31 s). Engaged-views/views is our best API proxy for "stayed to watch" until Studio shows it.
- 2026-11-14: Peak-end Short (6z_Euar4Wrg, public since 12 Nov 22:00) has 1 view after 34 h while siblings got 11–49 on day 1 → a Short with ~0 views after 24 h is a distribution problem (restriction/claim/not classed as Short), not a hook problem; check Studio before drawing creative conclusions.
- 2026-11-14: Shorts-feed avg view duration rose from 7 s to 13 s as more videos entered Analytics (79 feed views) – early single-video numbers swing a lot.
- 2026-11-14: The GitHub MCP Actions tools work from the cloud session (list runs, cancel a run) – use them to cancel a stale render instead of burning minutes.
- 2026-11-14: search.py never filled its `used` set, so the same clip was offered for several lines/videos; a batch shared ~30 clips between Shorts and the long video. Fixed (dedupe per job); build_render also drops repeats.
- 2026-11-14: Pixabay's API is weak on specific objects (handbag, lottery ticket, earrings → wheat 'ears', stamps, MRI, red sneakers). Write queries for what can be filmed generically (money, shop, hands, faces) and plan lines around visuals that exist; run one targeted gap search per batch.
- 2026-11-14: Studio advice on a 27 s Short: 81% swiped, avg 11 s, payoff at 13–22 s → put the result in the first 4–5 s.
- 2026-11-14: Long-video pipeline is now in the render workflow: `"long": {"id", "segments"}` in render.json → collect job joins segments (scripts/join_long.py, −14 LUFS, chapters file); title cards are burned per segment (`title_card`); contact sheets are 16:9 for `"aspect": "16:9"` videos.
- 2026-11-14: The `tighten` step (render.py) did not visibly run on the runner for v2 (pauses still ~0.8 s); it was applied in the session instead. Check the render step log next batch before relying on it.
- 2026-11-14: drawtext treats `%` as an expansion char – hook cards need `expansion=none` (fixed). Pixabay clips can start with a single black frame or a near-black second (r1) – check frames at 0.0/0.6 s and run blackdetect with d=0.01.
- 2026-11-14: Cutting long-video pauses to 0.45 s removed 76 s (11:00 → 9:43, below the 10-min target); 0.65 s removed 47 s (→ 10:12). Write long scripts at ~1,800 words if pauses get cut.
- 2026-11-14: Long video 01's final file is not in the repo (its v2 render was cancelled; the uploaded file was joined in an earlier session) – keep final long videos' segment lists in the repo so they can be re-edited.
- 2026-11-14: Long 02's outro named "why your brain is bad with money" (long 01), which was then not released → user trims the last ~8 s in Studio (cut from 10:04.5). Outros may only name videos that are already public; otherwise point to "the next video on screen" and use an end screen ("1 video, 1 subscribe", Best for viewer).
- 2026-11-14: Test & compare shows "Ineligible – not public" while a video is scheduled; it can only start once the video is public.
- 2026-11-14: Description hashtags: 3–5, strongest first (first 3 show above the title; >15 = all ignored). Tags field: ~10–15 plain relevant phrases, no "#".
- 2026-11-14 (Studio workflow, long 02): the Editor is not in the upload window – finish the upload (schedule it), then Content → click the video → Editor → Trim & cut → drag the right edge of the blue box to the cut point → Preview → Save (reprocessing takes minutes to an hour; a scheduled video still goes live, the trimmed version replaces it). Set end screens only AFTER a trim so their timing matches. End screen = "1 video, 1 subscribe", Best for viewer, last 6–7 s only.
- 2026-11-14: Prevention > repair: before delivery, re-read the last 15 s of every long script and check every video it names is already public; deliver the exact end-screen start time in the upload sheet.
- 2026-11-14 (batch c): the runner's `tighten` step again did not shorten pauses (0.8–0.9 s gaps remained). In-session `tighten(..., noise="-33dB", min_detect=0.4)` works; the default -38dB misses breathy pauses. Cut 1.0–2.7 s per Short.
- 2026-11-14 (batch c): many Pixabay picks were already used by the same week's Shorts/long video – build_render now seeds `seen` from earlier jobs and drops repeats with Shorts (long-video overlap allowed). Pick 2–3 spare clips per line.
- 2026-11-14 (batch c): candidate `tags` in *_candidates.json tell you what a clip is (e.g. "waffles", "nutella") – check them alongside the sheet; thumbnails at sheet size misled two picks. White/black-background product clips often open on a flat frame for 0.5–1 s → scan with a flatness check and hold a later frame (ffmpeg freezeframes with split).
- 2026-11-14: Pixabay has no treadmill, queue or "person in gorilla suit" footage; plan lines around what exists (walking, copy machines, real gorillas).
- 2026-11-14 19:00: first breakout signal = doorway remake (395 views in 3 h vs previous best 51 on day 1). Score new topics on "has the viewer lived this moment?" + "is the title the question they'd type?" before the study's wow-factor; the new style (result first, ≤20 s, loop) is the base, the relatable moment seems to be the multiplier.
- 2026-11-14: 7 private uploads carried the description footer ("Science-backed psychology · Sources in description · Not medical advice.") as their title and had no publish time – the daily summary should keep flagging private videos with that title.
- 2026-11-14: MPT renders often have a video track 0.3–2.7 s shorter than the audio (s04 clean: 16.4 vs 17.9 s) – the player then freezes the last frame while the voice finishes. Pad with `tpad=stop_mode=clone:stop_duration=<gap>` after tightening; check `ffprobe stream=duration` per stream in review.
- 2026-11-14: Clean (no CTA card) versions for Instagram/Facebook = same render.json with `cta_text` removed (job 2026-11-14-clean); flat-frame fixes must be re-applied after each re-render.
- 2026-11-14: Meta Business Suite only schedules Reels at least ~20 min ahead – schedule the week in one go, never last-minute.

## 15 Nov 2026 – automatic YouTube upload
- Built scripts/upload.py + workflow upload-videos (push jobs/<batch>/upload.json). Always uploads PRIVATE, optional publishAt; never re-uploads a key already in uploads/<batch>.json.
- Facts (checked 15 Nov): since 2 Nov 2026 unverified API projects are no longer forced to private (Data API revision history); videos.insert has its own 100 calls/day bucket (since 1 Jun 2026); publishAt and containsSyntheticMedia are settable.
- USER RULE: check upload compliance every week (API revision history, API Services Terms + Developer Policies). Any conflict or doubt → no automatic upload, deliver for manual upload and tell the user.
- Token status: WAITING – user must replace YT_REFRESH_TOKEN with one that has youtube.upload + youtube.force-ssl (plus the two readonly scopes). Until the user confirms, upload manually.
- First run: upload ONE Short without publish_at; user checks it in Studio before the rest.
- Still manual in Studio: Related video, pinning the comment, Test & compare.

## 15 Nov 2026 – Meta auto-posting plan (user agreed)
- Order: 1) YouTube auto-upload test in the 21 Nov batch; 2) once that works, send the user a Meta setup guide (Meta developer app, IG account must likely be Business not Creator, Page token, secrets); 3) Facebook Reels first (API supports scheduled publish 10 min–29 days ahead, 30 API reels/Page/24 h); 4) then Instagram (no scheduling in the API → our own GitHub cron posts at each slot + a backup run 10 min later, ~120 Actions min/month).
- Add Meta Platform Terms / Developer Policies + IG/FB publishing docs to the weekly compliance check when Meta posting goes live. Any conflict → manual via Meta Business Suite.

## 15 Nov 2026 – daily stats
- The Data API's channel viewCount lags hours behind per-video counts (14 Nov 18:06: channel 174 while videos summed ~690). Compute "change since yesterday" from per-video sums, not the channel total.
- A Short's day-1 burst on our channel is front-loaded: doorway got ~55% of its first-16 h views in the first 3 h. Judge day-1 at ~24 h but expect most of it by hour 6.
- 2026-11-16: Doorway's burst ended by ~hour 16 (720 → 723 over the next 24 h). A big day-1 test does not keep growing by itself – no second wave on our channel yet. Expect each Short's views to be ~final after ~16 h.
- 2026-11-16: Second near-zero public Short (spotlight remake, 2 views at 16.5 h; peak-end is at 0) – 2 of 13 public Shorts got no real feed test. Check Studio before judging the creative.
- 2026-11-16: When Bash is blocked, the GitHub MCP (create_or_update_file on jobs/stats-now, list_commits, push_files) runs the whole daily read.
- 2026-11-15: All Meta uploads so far (doorway 14 Nov, liking gap/spotlight 15 Nov, the 16–22 Nov week) went to Facebook only. Cause: scheduled via "Create post", whose Instagram check allows 4:5–16:9 only and rejects our 9:16 files ("Wrong aspect ratio"). Use "Create reel" in Business Suite, one Reel at a time – the bulk upload tool is what rejects 9:16 for Instagram (user, 15 Nov). Instagram has no data yet – the platform test effectively starts when IG Reels are posted.
