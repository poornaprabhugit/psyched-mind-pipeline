from content import S
HELD = set()
L = []
L.append("# Upload sheet – batch 2026-11-21 · 14 Shorts (Mon 23 – Sun 29 Nov) + long video (Sun 22 Nov 18:00)\n")
L.append("_Scripts approved by the user on 20 Nov; built exactly as approved. Shorts part delivered first; the long-video part is at the end._\n")
L.append("**Upload:** manual in YouTube Studio this week (automatic upload stays off until the new YT_REFRESH_TOKEN with youtube.upload is confirmed; weekly compliance check 21 Nov = OK).\n")
L.append("## Schedule at a glance (Amsterdam time)\n\n| Day | 12:00 | 16:00 |\n|---|---|---|")
for i in range(0, 14, 2):
    a, b = S[i], S[i + 1]
    L.append(f"| {a['day']} | **{a['b']}** {a['short']} · {a['angle'].split(' & ')[1]} · card {a['arm']} | **{b['b']}** {b['short']} · {b['angle'].split(' & ')[1]} · card {b['arm']} |")
L.append("""
Angle mix (user, 17 Nov): 8 brain & memory · 4 brain & money · 2 brain & health. **P1 subscribe-card test (user, 20 Nov):** arm A (card "Subscribe for a new brain fact every day" in the last 2.5 s) = B01, B04, B05, B08, B09, B12, B13; arm B (no card) = the other 7. Balanced by angle (4/2/1 each) and slot.

**Same settings for every Short:**
- Playlist "Psychology that moves you" · Category Education · Not made for kids · Language: English (video + audio language).
- Altered/synthetic content: **No** (real stock footage and photos, standard AI narrator).
- Thumbnail frame ~0:01 with the yellow hook card visible.
- **"Full video" card:** all 14 go live after the long video (Sun 22 Nov 18:00), so all 14 carry it. **Related video = "Why Your Brain Forgets Things On Purpose"** (the new long video) – set it once the long video is uploaded (it can be added later in Studio).
- Tags field: plain phrases, no "#".
""")
L.append("---\n")
for s in S:
    if s['b'] in HELD:
        L.append(f"## {s['b']} · {s['day']} {s['slot']} · HELD BACK – not delivered\nFailed the independent review twice (robot shot did not read as a robot; source link opened a different paper). Per the rule (max 2 fix rounds, then drop) it is not in this delivery. The Sat 28 Nov 12:00 slot stays empty unless you want to fill it. P1 arm B now has 6 Shorts (3 memory, 2 money, 1 health) vs arm A 7.\n\n---\n")
        continue
    L.append(f"## {s['b']} · {s['day']} {s['slot']} · {s['angle']} · P1 arm {s['arm']} (follow_card {'yes' if s['arm']=='A' else 'no'}) · predicted: {s['pred']}")
    L.append(f"**File:** `{s['b']} – {s['day']} {s['slot'].replace(':','-')} – {s['short']}.mp4` · **Hook card:** {s['hook']} · **Hook variant:** result-first line 1 + contrast card · **Ending:** loop")
    L.append(f"**Title:** {s['title']}")
    L.append("**Description:**\n```\n" + s['desc'] + "\nSource: " + s['src'] + "\nFull video: Why Your Brain Forgets Things On Purpose (Related video link above)\nScience-backed psychology · Sources in description · Not medical or financial advice.\n" + s['hashtags'] + "\n```")
    L.append(f"**Tags:** {s['tags']}")
    L.append(f"**Pinned comment:** {s['pin']}")
    L.append(f"**Related video:** Why Your Brain Forgets Things On Purpose (new long video)\n\n---\n")
open('upload-sheet.md', 'w').write("\n".join(L))
C = ["# Instagram + Facebook Reels – captions for 23–29 Nov (14 Reels, 2 per day)\n",
     "Use the **IG-FB** files (no \"Full video\" card; arm-A Reels show \"Follow for a new brain fact every day\" at the end instead of \"Subscribe…\"). Schedule each Reel in **Meta Business Suite → Create reel** (NOT \"Create post\") with **Instagram + Facebook both ticked**, same day and time as on YouTube (Amsterdam), at least 20 min ahead.\n",
     "**For every Reel:** paste the caption block as it is · cover = a frame with the yellow hook card (~0:01) · Audio: the video's own sound · AI label: off (real footage/photos + standard narrator) · max 5 hashtags.\n", "---\n"]
for s in S:
    if s['b'] in HELD: continue
    C.append(f"## {s['day']} · {s['slot']} · {s['short']}  ({s['b']}, follow card {'yes' if s['arm']=='A' else 'no'})")
    C.append(f"**File:** `IG-FB – {s['day']} {s['slot'].replace(':','-')} – {s['short']}.mp4`")
    C.append("```\n" + s['ig_hook'] + "\n\n" + s['ig_body'] + "\n\nSource: " + s['ig_src'] + "\nFollow for one real psychology study a day 🧠\n" + s['ig_tags'] + "\n```\n")
open('igfb-captions.md', 'w').write("\n".join(C))
print('ok')
