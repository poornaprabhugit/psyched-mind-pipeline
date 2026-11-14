---
name: psyched-mind-shorts
description: Run, review or improve the automated YouTube pipeline for the channel The Psyched Mind (psychology Shorts + weekly long video, MoneyPrinterTurbo, Pixabay, GitHub-driven weekly batches).
---

# The Psyched Mind – video pipeline

English YouTube channel **The Psyched Mind**, handle **@ThePsychedMindHQ**. Owner is in Europe/Amsterdam and uploads manually from YouTube Studio. Claude project: "ThePsychedMindHQ" (status doc `claude/channel-status.md`, deck "The Psyched Mind – Project Overview" – keep both current). Claude decides, writes, picks clips, renders, reviews and delivers; ask the user only for what only they can do (accounts, secrets, approvals, uploads, Studio numbers).

**Read first, every run:** `memory/playbook.md` (researched growth playbook – wins over this skill on growth practice), `memory/scoreboard.md` (our data; beats [Pro] rules once a video has ≥1,000 views), `memory/lessons.md`, `memory/topics_log.md`, `memory/performance.csv`, `memory/stats/latest.json`.

**Keep this skill current:** when a decision, setting or lesson changes, propose an updated complete SKILL.md and tell the user.

## Weekly format (user decisions 11 + 14 Nov 2026)
- **7 Shorts + 1 original long video per week**, AI voice. Batch runs **Saturday ~08:00 Amsterdam** (scheduled task).
- **Angle mix:** 4/7 Shorts wealth & success psychology (money, wealth, business, luxury/status, spending – always a real study, never get-rich promises or financial advice), 1 health & mind (behaviour, never medical advice), 2 everyday psychology (control). Log the angle per video; compare in scoreboard.md.
- **Slots:** Shorts one per day alternating **12:00 / 16:00 Amsterdam** (slot test; split the wealth Shorts evenly across slots). Long video **Sunday 18:00**.
- **Long video:** 10–15 min, 16:9, Alux-style numbered list, packaging first (title + 2–3 thumbnails before script), promise confirmed in the first 30 s, setup → tension → payoff + "try this today" per item, re-engagement ~3 and ~6 min, strongest item last, no ending signal, 5–10 s pointer to one next video. Leans wealth/success; every 3rd week a contrast angle (health/everyday). Write ~1,800 words (pauses get cut). 1/week until 2 are live; 2/week only if CTR ≥ ~4% and avg % viewed ≥ 35–40%.
- **Never:** mass-produced/templated content, stitched-Shorts long videos, narrator posing as psychologist/coach/adviser, made-up facts, real people's likeness, movie/TV clips, AI-generated realistic people. Tick "altered or synthetic" only for photorealistic AI visuals, AI music or a real-person voice. Every claim sourced.

## Shorts script rules (14 Nov, from Studio data: 7–24% stayed, payoff came too late)
- **15–22 s, ~45–55 words.** Line 1 (≤ ~12 words, "you") states the **study's result** – the payoff lands in the first 3–5 s. Setup squeezed into one or two lines after it ("Researchers tested it: …"). No researcher names, universities or years in the voiceover (description only).
- **Hook card** (black on #FFE600, top, 0–2.5 s), ≤ 8 words, a **contrast** where the study has numbers ("$100 trip vs $50 trip?").
- **Full loop ending (default):** the last line flows straight into line 1 ("…That's why" → line 1). No closing questions or "use it" lines (questions go in the pinned comment).
- **First clip must literally match the hook line.** If Pixabay has no video: simpler filmable query → matching Pixabay photo with slow zoom (to build) → rewrite the hook around a filmable scene. Visual change every ~1.5 s in the first 5 s (`fast_open`).
- **"Full video: tap the link below"** card (last 2.5 s) only on Shorts that go live after a long video is public; their Related video = that long video.
- Draft, then rewrite once for a sharper hook and tighter middle. Predict low/medium/high per video.

## Cloud pipeline (GitHub, all driven by git)
Repo `poornaprabhugit/psyched-mind-pipeline` (attach with add_repo if needed), clone at `/home/claude/psyched-mind-pipeline`. Secrets: `PIXABAY_API_KEY`, `YT_CLIENT_ID/SECRET/REFRESH_TOKEN`. The GitHub MCP Actions tools work (list runs/jobs, cancel a stale run).
1. **Search:** push `jobs/<batch>/search.json` `{"videos":[{"id","aspect":"16:9" (long only),"lines":[{"n","text","queries":[2–3]}]}]}` → workflow **search-clips** → branch `results/<batch>-search` with `<id>_candidates.json` + contact sheets (9:16 or 16:9 cells). Clips are de-duplicated across the whole job. Run one targeted gap search per batch for lines with no literal match (Pixabay is weak on specific objects).
2. **Pick:** look at **every** contact sheet (never pick from text). ~12 clips per Short, ~audio/4 s + 2 per long segment; each clip literally matches its line; reject AI faces, cartoons, 3D, letterboxed, near-black, flat colour, text/logos. Long-video sheets can be delegated to subagents (they must view the sheets).
3. **Render:** push `jobs/<batch>/render.json` `{"videos":[{"id","subject","script","clips",opt "hook_text","cta_text","title_card","fast_open":{"clips":3,"seconds":1.5},"settings":{}}],"settings":{},opt "tighten":true,opt "long":{"id":"long02","segments":["L0",…]}}` → workflow **render-videos** (MPT pinned 53c4ca3d = v1.3.10, ≤5 parallel) → branch `results/<batch>-render`. With `"long"`, the collect job joins the segments (`scripts/join_long.py`: −14 LUFS, chapters file; files > 95 MB are split into `.part-*`, rejoin with `cat`). Shorts ~5 min, long segments ~10–17 min, join ~12 min.
4. Never push two render.json commits back to back; cancel the stale run.
5. Post-render (in session if the runner skipped it): `render.tighten()` cuts pauses to ~0.35 s (Shorts) / ~0.65 s (long, keeps ≥10 min); patch single black frames with `freezeframes`.
- Long-video segments: settings `video_aspect 16:9, video_clip_duration 4, subtitle_position bottom, font_size 64, no bgm, voice_rate 1.0`; `title_card` per item segment; L0 has no card.

## Render defaults (scripts/render.py)
`video_aspect 9:16`, `video_concat_mode sequential`, `video_clip_duration 3`, `voice en-US-ChristopherNeural-Male`, `voice_rate 1.1`, `voice_volume 1.4`, `bgm random 0.2`, captions centre word-by-word pop_spring, MicrosoftYaHeiBold 80, #FFE600 with black stroke 4. Cards are ffmpeg drawtext with `expansion=none` (so `%` works).

## Review checklist (every video)
Duration (Shorts 15–25 s), 1080×1920 / 1920×1080, frame grid (0, 0.6 s, every 1.5 s, last 3 s), loudness (Shorts ≈ −17 LUFS, long −14), `blackdetect d=0.01 pix_th=0.1`, `silencedetect` (no pause > 0.5 s, no dead air at the end). Check: hook card readable and first clip matches line 1; each clip matches its line; no AI faces/cartoons/flat colour; captions readable; ending loops. Long: every segment join, title cards, audio continuity, first 30 s deliver the title's promise, last frames, re-read script for filler. FIX by swapping clips and re-rendering (max 2 rounds); drop a Short rather than ship a bad one. The user listens once (Claude can't judge the voice).

## Learning loop
Daily stats task (08:33) updates scoreboard.md with the YPP line. Weekly: update performance.csv, scoreboard.md (angle, slot, long-video trackers), lessons.md. <1,000 views/video = noise. ~80% close to what works, ~20% experiments, one variable at a time. Monthly (first Saturday): refresh the playbook research + re-package the worst-CTR long video. Ask the user for Studio "stayed to watch" (not in the API).

## Delivery
One clearly named set: A = replacements of scheduled uploads, B1–B7 = Shorts with day + slot in the name, C = long video + thumbnails, D = upload sheet. SendUserFile all together, then one SendUserMessage: what was made, what changed and why (cite scoreboard/playbook), open experiments, YPP line, what the user must do. Commit `batches/<batch>/scripts.md` + `upload-sheet.md` + thumbnails, append topics, push; delete results branches older than 2 weeks; update the project doc and deck.

## Monetization facts (verify, they change)
YPP until 31 Jan 2027: 1,000 subs + 4,000 public long-form watch hours/12 mo or 10M Shorts views/90 days; from 1 Feb 2027 new applicants 8,000 h or 20M. Fan-funding tier: 500 subs + 3,000 h or 3M Shorts views. Shorts-feed watch time never counts toward hours.

## Status log
- 10 Nov: channel created; week 1 (7 Shorts) published; cloud pipeline built.
- 11–13 Nov: playbook researched; stats workflow; long video 01 (money, 7:17) built.
- 14 Nov: batch 2026-11-14 – 7 Shorts (wealth-led), long 02 "The Psychology of Looking Rich" (10:12), remakes of doorway/liking gap/spotlight in the new style; loops default; long-video join in the workflow.
