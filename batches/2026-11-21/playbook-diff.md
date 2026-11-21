# Proposed playbook change – batch 2026-11-21 (waiting for the user's approval; NOT applied)

## 1. Replace §6 "Long video" with the long-video blueprint (user decision 19 Nov, research doc https://claude.ai/artifact/Sp66xbnDZhxp2X3w3Cv6Nv)
Why: the user decided on 19 Nov that long videos are ONE story with one open question in the same brain theme as the Shorts, never a list/compilation. The current §6 still describes a numbered-list (Alux-style) structure. The 22 Nov long video ("Why Your Brain Forgets Things On Purpose") is the first one built this way.

```diff
-## 6. Long video (10–15 min) — script & edit
+## 6. Long video (13–15 min) — one story, one open question (blueprint, user 19 Nov 2026)
 
 **Packaging first [Pro].** Write title + thumbnail concept *before* the script. The video must deliver exactly what they promise (mismatch = early drop-off).
 - Title: one clear promise, curiosity gap, "you", ≤ 60 characters.
 - Thumbnail: 1280×720, max 4 big words that *add* to the title (don't repeat it), one strong visual, brand colours #111114/#FFE600, readable at phone size.
 - Upload 2–3 variants to **Test & compare** (desktop Studio, long videos only, winner chosen by watch time, can take up to 2 weeks; don't edit title/thumbnail during a test; make variants clearly different) [YT].
 
-**Script structure** (MrBeast memo + George Blackman) [Pro]:
-- **0:00–0:30 — the most important part.** Open on the payoff/problem immediately; no "welcome to the channel", no logo sting. Confirm the title's promise in the first 5–10 s (critical for viewers arriving from a Short) [YT].
-- **Per item = setup → tension → payoff.** Setup gives the next 30–60 s stakes ("this is why you…"), tension reveals info gradually, payoff is a clear "aha", then go straight into the next setup.
-- **Re-engagement beats** around ~3 min and ~6 min: the most surprising study or a "number 1 changes how you…" tease.
-- **Back half stays strong:** don't put weak items last. Strongest item last.
-- **Don't signal the ending.** No "to wrap up"; end quickly after the final payoff with a 5–10 s pointer to one specific next video.
+**Script structure – one story, not a list:**
+- **Same brain theme as the Shorts** (so Shorts viewers who tap "Full video" get what they came for).
+- **One open question asked at 0:00** ("If your brain is so powerful, why does it keep dropping things?") and answered only at the end; every chapter adds one clue to it. No numbered items, no "number 5…".
+- **A spine the viewer lives through** (e.g. one ordinary day, morning → night); 4–6 chapters, each = moment the viewer knows → the study (setup → tension → payoff) → what it says about the open question → a bridge into the next chapter.
+- **0:00–0:30:** open inside the moment, state the question, promise the answer; confirm the title's promise in the first 5–10 s [YT].
+- **Re-engagement:** a forward tease at ~3 min and ~6 min ("the strangest part isn't what you forget…"); hold back the one practical takeaway for the last chapter.
+- **Ending:** answer the question, give one "try this today", then a 5–10 s pointer to one already-public video; no "to wrap up".
+- ~1,950 words at voice rate 0.92 ≈ 13–14 min after pause trimming (0.6 s).
 
-**Edit.** Show, don't tell: stock clips matched to every line, scene change every 3–6 s, title card per item, chapters (00:00 + one per item), loudness −14 LUFS, no black gaps at segment joins.
+**Edit.** Sentence-aligned clips (each line gets its own literal clips, scripts/align.py); a recurring person/setting where stock footage allows; **simple animated diagrams of each experiment rendered in code** (Python/Pillow → ffmpeg, numbers only from memory/facts.md, source name small on screen); small on-screen chapter labels (no flow-resetting title cards); YouTube chapters (00:00 + one per chapter); loudness −14 LUFS; no black gaps at joins; never reuse a Short's footage or hook card.
 
 **Upload.** Description with keywords in the first 2 lines + chapters + citations; end screen to a related video/playlist; add to playlist "The Psyched Mind – Weekly Psychology"; post Sunday 18:00 Amsterdam, then set the Related video link on that week's Shorts.
```

## 2. No other playbook changes proposed this week
The weekly research check (memory/research-log.md, 21 Nov) found no platform change and no decision-grade signal in the new top-Shorts pull.
