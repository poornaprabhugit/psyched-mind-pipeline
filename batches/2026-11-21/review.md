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
