# Batch 2026-11-21 – independent final review (14 Shorts, YT + IG-FB)

_Reviewed 21 Nov 2026 against: "Would Psych2Go / Zack D. Films / The School of Life post this as it is?" Read: facts.md, voice.md, playbook §0–1, scripts.md, upload-sheet.md, igfb-captions.md. Opened all 14 frame grids (out/shorts2/pXX_grid.jpg, which match the delivered files byte for byte) plus end frames of all 14 IG-FB files._

**Tech (all 28 files):** 1080×1920 · video and audio end within 0.031 s · −16.2 to −17.4 LUFS · no black frames · no silences > 0.5 s · no flat frames (flat.py min sd ≥ 12.5). Card checks: the "Full video: tap the link below" card is in the last ~2.5 s of all 14 YT files and in none of the IG-FB files. Subscribe card (YT) and Follow card (IG-FB) appear on exactly B01, B04, B05, B08, B09, B12 and B13. They sit fully inside the frame, below the captions and not covering them. The other 7 have no card.

**Facts:** every number in voiceover, hook card, title, description and caption traces to facts.md. Two descriptions have no source link (B03, B11).

| Video | Verdict | Reasons | Exact fix |
|---|---|---|---|
| B01 Phantom buzz | PASS | Hook clip shows a phone in a hand; the shirt clip lands on "shirt moves"; clean loop | – |
| B02 Lost ticket | PASS | $10 bill on line 1, then ticket, theater and empty pocket; strong match | – |
| B03 Contagious yawns | **FIX** | (1) The dad-and-child clip (~12.0–16.5 s, "Your brain copies…") is also used in B11, and it is a weak match. (2) No source link in the description (rule §1.5) | Swap 12.0–16.5 s for a person yawning back at someone, or another yawn. Description: add the DOI for Provine (1986), likely https://doi.org/10.1111/j.1439-0310.1986.tb00611.x (check it resolves) |
| B04 FREE chocolate | PASS (note) | No shot shows candy on a check. The chef-with-bread clip (~12–13.5 s, "turned back") is a loose match | Optional: swap 0–1.5 s for mints or chocolate on a check tray |
| B05 Photo forget | PASS (note) | Frame 0–1.4 s is heavily out of focus. "Sony Lens G" text shows at ~7.5–10.5 s | Optional: start the clip ~1 s later; use a lens shot with no brand |
| B06 Alone/shock | PASS (note) | The masked woman (~10.5–13 s) reads as COVID, not "women pressed it" | Optional: swap for a woman alone in a room |
| B07 Old stuff | PASS (note) | Brazilian "centavos" coins on "under three" (~10.5–12 s). Rule: US dollars | Swap for US coins or $1 bills |
| B08 Stuck song | PASS | Gum on line 1, key-press and finger-tap clips match | – |
| B09 Nature | PASS (note) | A "TOPMAN" store sign is visible ~3–4.5 s | Optional: crop or swap the city clip |
| B10 Smell | PASS (note) | An adult couple is on screen during "Smells brought back early childhood" (~10.5–12 s); the toddlers come ~1.5 s late | Optional: move the carousel clip forward 1.5 s |
| B11 Tickle | **FIX** | (1) The dad-and-child clip at ~1.5–3.0 s is the same footage as in B03, at hook time. (2) The robot shot (~9–10.5 s) is mostly an empty gray wall with the toy at the edge. (3) No source link in the description | Swap 1.5–3.0 s for a tickling clip (a parent tickling a child's feet or belly). Swap 9–10.5 s for a centered robot or robot-arm clip. Description: add https://doi.org/10.1162/089892999563607 (check it resolves) |
| B12 Word | PASS (note) | Extreme teeth close-ups (~3–6 s) are unappealing. The IG caption drops "Scientists think" ("Your brain's response simply gets tired") | Optional: swap for a talking mouth. Caption: "Scientists think your brain's response simply gets tired." |
| B13 Losses | PASS (note) | The title has no "you". The coin-flip clip sits at the end (15–17 s), not on "Flip a coin" (~4.5 s) | Title: "Why losing money hurts you twice as much 💸". Optional: move the coin clip to ~4.5 s |
| B14 Wandering | PASS | Window-gazer on line 1; phone pings; reader on "even reading this" | – |

**Sameness (batch):** no footage is reused except B03/B11 (fixed above). Five of 14 end with "That's why ↻" (B01, B03, B04, B07, B13), and all 14 use the same hook variant (result-first line + contrast card). The scripts are approved, so this is not a FIX. Next batch: vary the loop words and at least 3 hook structures, because YPP's "templated" rule (§1.1) is aimed at this.

## Round 2 (independent re-review, 21 Nov 2026)

_Same bar. Opened p03/p07/p10/p11 grids, extra frames at B03 10–14 s and B11 6.5–10.5 s, the check.py grids for the 4 IG-FB re-renders, and the end frames of IG-FB B07/B10. Read upload-sheet.md (B03, B11, B13) and igfb-captions.md (B12). Ran check.py and flat.py on the 8 re-rendered files. Ran a frame-hash check across all 14 YT files for reused footage, and a card-position scan on all 28 files._

**Tech (8 re-renders):** 1080×1920 · A/V end within 0.027 s · −16.5 to −16.8 LUFS · no black frames, no silences · flat.py min sd 12.5 (B03) / ≥ 34.8 (others) · no logos or letterbox seen. **Cards (all 28):** the "Full video" card starts exactly 2.4–2.5 s before the end in all 14 YT files and is in none of the 14 IG-FB files. B03, B07, B10 and B11 have no subscribe or follow card. **Reuse:** the dad-and-child clip is gone from both files. The frame-hash check found no footage shared between any two Shorts (the one hit, B05/B06, was a false match between two dark frames).

| Item | Verdict | Notes |
|---|---|---|
| B03 shared clip | PASS | The dad-and-child clip is replaced with a woman stretching awake in bed (~12–13.5 s), then a yawning cat. It is not used in any other Short. It's a stretch, not a yawn, so it's an OK match, not a strong one. Note: the white cat stays on screen for ~5.5 s (≈12–17.5 s), which is long for a Short. |
| B03 source link | PASS (note) | The link is present: `cir.nii.ac.jp/crid/1360292621459430784`. The page loaded empty here, so I could not confirm it shows Provine (1986). The DOI could not be checked either: the proxy blocked it. Better: use the DOI `https://doi.org/10.1111/j.1439-0310.1986.tb00611.x` once someone opens it in a browser and confirms it is Provine 1986. |
| B11 shared clip | PASS | The hook is now a baby being tickled on the belly (0–1.5 s), then a smiling baby. No shared footage. |
| B11 robot shot (~7.5–10.5 s) | **FIX** | The new shot is factory or lab machinery, with no robot or robot arm visible. On "tickled themselves through a robot" it doesn't read as a robot. Swap it for a clear robot arm or robot hand. |
| B11 source link | **FIX** | The link `wolpertlab…/BlaWolFri99.pdf` opens a **different paper**: Blakemore, Wolpert & Frith (1999), *NeuroImage* 10, 448–459, an fMRI study. It only mentions the robot-delay study in its introduction. The description cites J Cogn Neurosci 11(5). Replace it with `https://doi.org/10.1162/089892999563607` (J Cogn Neurosci 11(5):551–559), after someone opens it in a browser to confirm. The proxy blocked it here. |
| B07 foreign coins | PASS | No coins left. A US $1 bill is on screen at ~7.5–10 s, and a mug is on "under three". |
| B10 early childhood | PASS | Toddlers on a carousel land on "childhood" (~12 s). No adult couple. |
| B13 title | PASS | "Why losing money hurts you twice as much 💸" |
| B12 IG caption | PASS | "Scientists think your brain's response simply gets tired." |

**Round 2 result:** B11 is still **FIX**: wrong-paper source link and robot shot. Everything else passes. B03's link is a note, not a blocker.

## Long video

_Independent final review, 21 Nov 2026. File: `C – Sun 22 Nov 18-00 – Why Your Brain Forgets Things On Purpose.mp4` (delivered, patched version). Bar: "Would a top psychology/facts channel (Veritasium-lite, The School of Life, Psych2Go) post this as it is?" Read: scripts.md (LONG VIDEO), upload-sheet.md §C, facts.md, voice.md, playbook §1 and §6, playbook-diff.md (new §6). Opened sheet_1–4 plus ~35 new frames (chapter starts, cold open, 10:22–10:30, 11:35.4, end). Ran ffprobe, ebur128 and silencedetect (−35 dB, 0.5 s), plus peak levels at the 5 joins._

**Tech:** 1920×1080, 30 fps · 11:46.0 (video 705.97 s, audio 706.04 s) · **−14.0 LUFS**, LRA 2.3, true peak −1.4 dBFS · no silence longer than 0.62 s anywhere (all are the normal sentence pauses) · 11:35.4 now shows a held frame (child drawing). No black frame.

**One story or stitched Shorts?** **One story.** One question ("If your brain is so powerful, why does it keep dropping things?") is asked at ~0:24 and answered at ~10:00. The spine is one day, morning to night. Each chapter ends with a clue ("This is the first clue…") and a bridge into the next chapter ("But the next part of your day…", "Not so fast", "the strangest part…"). The practical takeaway is held back for the end. It is not a compilation.

| Item | Verdict | Reason | Exact fix |
|---|---|---|---|
| Structure (one story, one open question) | PASS | See above. The blueprint is followed: 5 chapters, a bridge per chapter, teases at ~2:48 and ~6:42 | – |
| Facts – numbers (voice, diagrams, description) | PASS | All numbers trace to facts.md: ~9 in 10 (87%), about half / 2/3 / almost all (53/68/96%), 60 s + 30 s ~1° warmer, 69%, 40.8 / 34.0 / 31.8 mph, 14% / 32%, 83/71 → 40/61%. Diagram bars and labels match | – |
| Facts – details not in facts.md | **FIX** | These spoken details are not in facts.md: "more than a hundred years ago" (Ebbinghaus); "a young student", "seventy-five days" (Murre & Dros); "students sat around a table" (Brenner); "high-school students", "English and German words" (Gais); "short science text" (Roediger). Rule: every claim must trace there | Open each paper and add a dated line to facts.md for each detail. If "seventy-five days" or "young student" can't be confirmed in Murre & Dros (2015), re-voice ~5:20–5:28 as "spent about seventy hours learning and relearning lists" |
| Voice rule – year in voiceover | PASS (note) | "In 2015" (~5:17) breaks voice.md ("no years in the voiceover"). The wording is user-approved | Optional: "Recently, two researchers repeated…" |
| First 30 s deliver the title's promise | PASS (note) | The lines are strong: kitchen moment → question at ~0:24 → "A lot of this forgetting is on purpose" at ~0:30. The footage is weak: 0:00–0:06 is hands rolling dough. Nobody walks in or stops. 0:06 knife, 0:07.5 steaming pot | **Fix with the footage below**: 0:00–0:06 needs a person walking through a doorway into a kitchen, stopping, looking around (this is the hook shot) |
| Footage matches lines | **FIX** | About 20 clips are mood B-roll with no link to their line. A top channel would not post this. Worst: 0:00–0:06 dough rolling ("You walk into the kitchen… You stop"); ~1:04–1:06 man in a respirator at an industrial machine ("put it down at another table"); 2:12 garden fence ("files the old scene away"); 2:36 pancake, 2:42 knife on a carrot ("first clue", "fits the moment"); 3:12 woman on a cliff; 4:36 seagulls, 4:42 tree; 5:24 empty chair ("seventy hours"); 6:00 dandelion, 6:06 ocean aerial; ~6:51 cat ("best or worst moment"); 7:48–7:50 aerial desert ("In a classic study… films of car crashes"); 8:36–8:42 apartment blocks ("This is what memory really is"); 9:30 wind turbine ("learned them in the morning"); 10:18 fish shoal ("weakens old connections"); 10:36 hooded figure in a garage ("exact words of every conversation"); 10:42 old doors ("The name fades") | Swap each one for a literal clip: 0:00 person entering a kitchen and freezing · 1:04 person setting an object on a table · 2:12 person closing a door behind them · 2:36–2:46 person standing in a new room, focused · 3:12 meeting-table introductions · 4:36–4:46 handshake / name said · 5:24 student at a desk with lists · 6:00–6:10 person scrolling past things / a crowd passing · 6:51 person telling a friend about their day · 7:48 dashcam / traffic · 8:36–8:42 person looking back, remembering · 9:30 student studying in the morning, then working all day · 10:18 neuron or brain animation · 10:36 people talking · 10:42 a name tag / person in the meeting |
| Logos / brand text | **FIX** | Apple logo on a MacBook at ~0:17–0:20 and ~2:52–2:56 (the chapter-2 opening frame, with a Google page on the second laptop). "SAVOCA" brand label on the mattress at ~0:42–0:45. "OLYMPUS" on the camera at ~7:46–7:48. A Spanish printed page fills the frame at ~10:48–10:52 (foreign text, distracts) | Swap or crop: 0:17–0:20 (crop out the lid or use a laptop with no logo), 2:52–2:56 (other meeting clip), 0:42–0:45 (crop the bottom ~25% or use another bedroom clip), 7:46–7:48 (other photo clip), 10:48–10:52 (English or blank notebook) |
| Flat / white frames | **FIX** | ~10:22–10:30 is ink drops on an almost blank white frame. The patched held frame at 10:26.6 is ~95% white with a small pink blob. On a dark-mode phone it reads as a flash/empty screen | Replace 10:22–10:30 with one clip that has content (e.g. a blurred photo coming into focus for "keeps the pattern and drops the noise") |
| AI faces, cartoons, letterbox | PASS | None seen. All people are real stock. Diagrams are clean code-drawn graphics | – |
| Code-drawn diagrams | PASS | Doorway, rooms, next-in-line, forgetting curve, cold water, Loftus speed + glass, reread vs test. Source tags are small, top-right. Numbers are correct | – |
| Chapter labels | PASS | Yellow tag top-left at 0:39.5, 2:52.5, 4:51.5, 6:48.5, 9:16.5. Readable. Never on a diagram, so no clash with the centered diagram titles | – |
| Captions | PASS | White with a dark outline, bottom center, sentence-aligned, readable at 1080p. On phones they are on the small side | Optional next time: +15% caption size |
| Segment joins (00:39, 02:52, 04:51, 06:48, 09:16) | PASS | Each join is a normal 0.51–0.60 s pause with a smooth fade out and in. No gap, click or level jump | – |
| Ending | PASS (note) | Answers the question → "try this today" (retrieval practice) → "watch this one next". The end screen goes to the choice-blindness Short, which is public. The last shot is a tulip, which doesn't relate to the pointer | Optional: 11:40–11:46 a person choosing between two photos (choice-blindness tease) |
| Description chapters | PASS | 00:00 · 00:39 · 02:52 · 04:51 · 06:48 · 09:16 match the labels in the file (±0.5 s). All 9 studies cited, 7 with DOI links | – |
| Title | PASS (note) | "Why Your Brain Forgets Things On Purpose" is 40 characters, has "your" and a clear promise. No emoji (voice.md asks for one; fine for a long-video title) | – |
| Thumb A "FORGOT WHY?" | PASS | 2 big words, readable at phone size, adds the doorway moment to title A. Real face, brand yellow | – |
| Thumb B "WHAT WAS HIS NAME?" | PASS (note) | 4 words, readable, adds the name moment to title B. The photo is soft/upscaled | Optional: a sharper source frame |
| Thumb C "YOUR BRAIN FORGETS / ON PURPOSE" | **FIX** | 5 words, and it repeats title A word for word. Playbook: max 4 words that *add* to the title | Keep only "ON PURPOSE" (big, yellow box), as in the original concept. Optionally add a trash-can or brain icon |
| Length vs 13–15 min target | PASS (note, target missed) | 11:46, about 1:15–3:15 under the brief. The approved script (~2,000 words) reads faster than estimated. Don't pad it; a tight 11:46 is better than filler | Note for the playbook: estimate ~170 words/min after pause trimming, so 13 min ≈ 2,250 words |

**Long video result: FIX.** It is one story, the numbers are correct and the tech is clean. It does not pass the bar yet because of (1) ~20 mood clips that don't match their lines, including the hook shot, (2) logos/brand text at 0:17, 0:42, 2:52, 7:46 and foreign text at 10:48, (3) a near-white flat stretch at 10:22–10:30, (4) Thumb C's text, and (5) the facts.md lines for the spoken study details. The script and audio don't need to change (unless "seventy-five days" can't be confirmed).
