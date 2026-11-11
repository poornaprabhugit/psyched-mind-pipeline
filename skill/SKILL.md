---
name: "psyched-mind-shorts"
description: "Run, review or improve the automated YouTube Shorts pipeline for the channel The Psyched Mind (psychology + motivation, MoneyPrinterTurbo, Pixabay, weekly batches)."
---

# The Psyched Mind – Shorts pipeline

English YouTube Shorts channel **The Psyched Mind**, handle **@ThePsychedMindHQ** (confirm with the user if unsure). Owner is in Europe/Amsterdam and uploads manually once a week from the YouTube app. Claude project: "ThePsychedMindHQ" (status doc `claude/channel-status.md` – keep it updated). The user has handed this over as a challenge: **make as many Shorts go viral as possible and reach monetization ASAP**; Claude decides what is best and asks the user only for things only they can do (accounts, secrets, approvals, uploads). Claude writes, picks clips, renders, reviews and delivers; the user listens once and uploads.

**Keep this skill current (standing order from the user, never wait to be reminded):** at the end of ANY session or scheduled run where a decision, setting, workflow, lesson or status changed, deliver the complete updated SKILL.md with SendUserFile and say in one line what changed. Do this unprompted, in the same turn as the change. The user has asked for this more than once.

## Status log
- 2026-11-10: Channel created. Week 1 (7 Shorts) rendered on the user's PC, passed review; first Short published 20:00 Amsterdam, rest scheduled daily. GitHub repo connected; cloud search + render pipeline built and a test Short (fresh start effect) rendered successfully in ~4 min on GitHub.
- First stats (13 views, too few to trust): Shorts feed 61.5% of views (avg 7 s), channel page 38.5% (avg 21 s); "stayed" ~44%, avg view duration ~60% on the mere-exposure Short. YouTube Studio's AI advice adopted below.
- 2026-11-10 late: YouTube stats connection live (workflow `youtube-stats`, scripts/stats.py, secrets YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN). Fresh start Short uploaded as the 8th video.
- 2026-11-11: Day 1 public (mere exposure): 29 views, 1 like, 3 subs. Pratfall title was wrongly set to the footer text, user fixed it. GitHub cron did not fire at all on its first day → daily summary now triggers collection itself (see Stats). Thumbnail-frame rule added.
- Next (was): YouTube stats connection (Google Cloud project, YouTube Data/Analytics API) → weekly self-improving scheduled task → 2 Shorts/day.

## Agreed decisions
- **Niche/format:** "real psychology behind everyday moments" + motivation. ~75–85 words, 25–35 s.
- **Script rules (from Studio AI advice + our research):**
  - First line ≤ 10 words, uses "you", creates tension or a surprising claim; no warm-up.
  - Every video has a **hook_text** card (on screen 0–2.5 s, black on #FFE600, top of frame): ≤ 8 words, intriguing claim/question, e.g. "Your favorite song is an illusion".
  - Go straight from hook to the strange result: say "Scientists…" / "In one study…"; put years and researcher names in the description, not the voiceover.
  - One idea per video; end with either a **loop line** that flows back into the first line ("…and that's the real reason you think…") or a motivational "use it" line / comment question. Alternate the two and compare in the stats.
  - Titles and first lines always use "you"; frame studies as everyday dilemmas.
- **Volume:** 2 Shorts per day (14/week) once the weekly cloud loop runs; add a weekly 8–10 min long-form compilation for watch hours once Shorts run smoothly.
- **Never:** made-up or superstition "facts", named real people's likeness, medical/financial advice, copied scripts/footage from other creators, movie/TV clips, AI-generated realistic people.
- **Branding:** dark #111114, yellow #FFE600 accent, psi-with-lightning-bolt logo; profile (800×800) + banner (2560×1440, text in 1546×423 safe area) on the Design canvas "The Psyched Mind – Channel Branding".
- **Channel description:** "The psychology behind how you think, feel and act, and how to use it to your advantage. 🧠⚡ Every Short takes a real study (the spotlight effect, the liking gap, the pratfall effect…) and turns it into something you can use today: more confidence, less overthinking, better habits. Science-backed, no fluff. New Shorts daily, sources in every description." Upload footer: "Science-backed psychology · Sources in description · Not medical advice. #psychology #motivation #shorts". Category Education, not made for kids, playlist "Psychology that moves you".
- **Scheduling:** ~16:00 Amsterdam (US morning); with 2/day add ~22:00.
- **Monetization facts (verify, they change):** YPP now = 1,000 subs + 10M Shorts views/90 days (or 4,000 watch hours). From 1 Feb 2027 new applicants need 20M Shorts views/90 days or 8,000 watch hours; Shorts revenue then requires 10M views/90 days even for members. Lower tier: 500 subs + 3M Shorts views (fan funding only).
- **YouTube policy:** inauthentic/mass-produced content is demonetized; keep genuine research, varied structure, real footage. No AI disclosure for real stock footage.
- **Deferred:** Hermes-style multi-agent server (cost, maintenance, no quality gain) – revisit only for auto-uploading or multiple channels. MoneyPrinterTurbo stays the renderer.

## Cloud pipeline (GitHub, primary)
Repo `poornaprabhugit/psyched-mind-pipeline` (private), cloned at `/home/claude/psyched-mind-pipeline`; secret `PIXABAY_API_KEY`. The session proxy **blocks the GitHub Actions API** (no workflow_dispatch, no run status, no artifact download), so everything is driven by git:
1. Write `jobs/<batch>/search.json` `{"videos":[{"id","lines":[{"n","text","queries":[2–3 concrete queries]}]}]}` and push to main → workflow **search-clips** (Pixabay API, `video_type=film`, filters AI/cartoon/3D/green-screen tags) pushes branch `results/<batch>-search` with `<id>_candidates.json` and contact sheets `<id>_sheet_N.jpg` (5 lines × 8 candidates, labelled `<line>-<k>`, cropped 9:16). ~1 min.
2. Clone that branch, **look at every sheet**, pick clips (any candidate from any line), write `jobs/<batch>/render.json` `{"videos":[{"id","subject","script","hook_text","clips":[urls]}],"settings":{optional overrides}}` and push → workflow **render-videos** (matrix, up to 5 parallel runners, installs MoneyPrinterTurbo pinned at commit 53c4ca3d = v1.3.10, ffmpeg) pushes branch `results/<batch>-render` with `<id>.mp4`, `<id>.json`, `<id>_api.log`, `STATUS`. ~4–6 min render + ~5 min setup.
3. Wait with a background `git ls-remote` loop for the branch (or a new commit on it); re-trigger a job by changing its JSON (e.g. a `run` counter). Delete old results branches when delivered (`git push origin --delete results/...`).
- **Clip count:** supply ~12 clips per video (≈ audio length / 3 s + 2 spares, last ones suitable as an ending). Too few makes MPT loop back to clip 1 at the end.
- Memory files in the repo: `memory/topics_log.md`, `memory/performance.csv`, `memory/lessons.md` – read first every run, update at the end, commit.
- Free private-repo quota: 2,000 Actions minutes/month.

## Stats (daily)
- Workflow `youtube-stats` writes memory/stats/<date>.json + latest.json (channel stats, per video views/likes/comments/privacy, analytics arrays per_video/daily/traffic_sources/countries, which stay empty for the first 1–3 days because of the lag).
- **Do not rely on its cron** (`17 6 * * *` UTC, best-effort; it skipped day 1 entirely). Trigger it: write a UTC timestamp to `jobs/stats-now`, push to main, wait ~1 min for the `stats <date>` commit by pipeline-bot. If it fails, check the run via GitHub MCP `actions_list` (works even though the proxy blocks the Actions API from git/curl) and memory/stats/last_run_log.txt, which usually means an expired refresh token or missing secrets.
- Scheduled tasks: "Psyched Mind daily summary" (09:33 Amsterdam, triggers stats, reports insights; push notification only for user actions) and "Psyched Mind weekly batch" (Sat 13:04 Amsterdam).
- After each upload, check titles in latest.json against the upload sheet (a footer once ended up as a title).

## Thumbnails
- Custom thumbnail uploads for Shorts are YPP-only (since Jul 2026, desktop Studio, no A/B testing). Until monetized, the user picks a frame in the YouTube app (Edit → thumbnail).
- Thumbnails show on the channel page/home only, not in the Shorts feed, but early on ~⅓ of views came from the channel page.
- Rule: plan clip 1 so the frame at ~0:01 shows the yellow hook card + an expressive face; put "Thumbnail: frame at 0:01" in the upload sheet. YouTube's auto frames show random caption words ("to", "one"), which is weak. Once in YPP, design real 9:16 thumbnails (key text centred, it gets cropped to ~3:2 in some places).

## Fallback (user's Windows PC)
MPT at `C:\Prabhu\Projects\MoneyPrinterTurbo-Portable-Windows-1.3.10`; `shorts\start_pipeline.bat` starts the MPT API (127.0.0.1:8080) + `shorts\clip_fetcher.py` (downloads cdn.pixabay.com URLs from `shorts\jobs\*.json` into `MoneyPrinterTurbo\storage\local_videos`). Needs the PC on and the Claude desktop app open and not minimized.

## Render settings (MPT API POST /api/v1/videos, defaults in scripts/render.py)
`video_source:"local"`, `video_materials` in script order, `video_concat_mode:"sequential"`, `video_aspect:"9:16"`, `video_clip_duration:3` (test 2 as an experiment), `voice_name:"en-US-ChristopherNeural-Male"`, `voice_rate:1.1`, `voice_volume:1.4`, `bgm_type:"random"`, `bgm_volume:0.2`, `subtitle_position:"center"`, `subtitle_display_mode:"word_by_word"`, `subtitle_animation:"pop_spring"`, `font_name:"MicrosoftYaHeiBold.ttc"`, `font_size:80`, `text_fore_color:"#FFE600"`, `stroke_color:"#000000"`, `stroke_width:4`. Always pass our own `video_script`. The hook card is burned in afterwards by `add_hook()` in render.py (ffmpeg drawtext, MicrosoftYaHeiBold, 72 px, wraps at 22 chars).

## Clip picking (the step that makes or breaks quality)
- Pexels API keys are paused; use **Pixabay**. Never let MPT auto-search.
- **Always check thumbnails visually** (contact sheets). Choosing from slugs/text alone let cartoons and 3D renders in – never do that. Reject AI-looking faces, letterboxed, near-black, plain-colour, animation/green-screen clips, and clips whose action happens outside the first 3 s.
- Avoid reusing a clip across videos in a batch.

## Review checklist (every video, before delivery)
ffmpeg: duration 25–60 s, 1080×1920, frame grid (0, 0.6 s, then every 1.5 s) **plus the last 3 s**, `ebur128` (≈ -17 LUFS ok, no clipping), `silencedetect`, `blackdetect d=0.05 pix_th=0.1`. Check: hook card readable; each clip matches its line; no AI faces/cartoons/flat colour/black stretches; captions readable; ending does not loop back to clip 1. Claude cannot judge the voice – the user listens once. PASS or FIX (swap clips, re-render; max 2 rounds).

## Learning loop (weekly, before writing)
1. Get stats for recent videos (until the API connection exists, ask the user to paste YouTube Studio / "Ask Studio" analytics): views, stayed vs swiped, avg view duration/% viewed, traffic sources. Append to `memory/performance.csv`. Treat samples under ~1,000 views as noise.
2. Compare by topic, hook style, hook card, length, ending type (loop vs question), clip duration; update `memory/lessons.md`.
3. Scan currently trending psychology/motivation Shorts for proven topics/angles – recreate the angle in our format, never the content.
4. Write the batch: ~70% doubling down on winners, ~30% experiments, one main variable per experiment. Check `memory/topics_log.md`; fact-check each claim against a real source and keep the link for the description.

## Delivery
Send each passed video as soon as it passes (SendUserFile, proactive) plus an upload sheet (thumbnail frame timestamp, title <60 chars with "you" + emoji, description citing the study + 3–5 hashtags incl. #psychology #shorts, posting slot, pinned-comment question). Be honest about weak spots. Topics used: week 1 – spotlight effect, liking gap, doorway effect, pratfall effect, Ben Franklin effect, IKEA effect, mere exposure effect; test – fresh start effect.