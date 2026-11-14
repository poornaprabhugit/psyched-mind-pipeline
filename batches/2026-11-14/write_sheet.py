import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SHORTS, SOURCES, LONG_TITLE, LONG_SOURCES
D = {
"s01": ("Lottery winners weren't happier than people who won nothing – and everyday pleasures felt smaller to them. Psychologists call it hedonic adaptation: your brain gets used to almost anything, even a fortune.", "#psychology #money #happiness #wealth #shorts", "Would you still work if you won the lottery? Yes or no.", "Won millions. Not happier."),
"s02": ("Why would you pick the holiday you'd enjoy less? In a classic study, more than half of people chose a $100 ski trip over a $50 one they expected to enjoy more – because it cost more. It's the sunk cost effect: the money is gone either way, but your brain hates 'wasting' it.", "#psychology #money #sunkcost #decisionmaking #shorts", "What's something you kept using just because you paid for it?", "$100 trip vs $50 trip?"),
"s03": ("Researchers secretly swapped the face people had picked as more attractive – and most didn't notice. They even explained why they 'chose' it, citing details that weren't in the face they actually picked. It's called choice blindness.", "#psychology #brain #choiceblindness #mindblown #shorts", "Would you notice the swap? Yes or no.", "You picked A. They gave you B."),
"s04": ("Why do loyalty cards start with free stamps? In a car-wash study, a 10-stamp card with 2 stamps already filled was completed almost twice as often as an 8-stamp card – the same 8 washes. It's the endowed progress effect, and you can use it on your own goals.", "#psychology #business #marketing #motivation #shorts", "What goal could you give a head start today?", "8 stamps vs 10 with 2 free"),
"s05": ("Why do you snap at people after a bad night? After a night and a day without sleep, the brain's alarm centre (the amygdala) reacted about 60% more to upsetting images, and was less connected to the area that normally calms it down.", "#psychology #sleep #brain #stress #shorts", "How many hours did you sleep last night? Just the number.", "No sleep = 60% more reactive"),
"s06": ("Why do you hear your own name in a noisy room? When people listened to a different voice in each ear and repeated only one, about a third still noticed their own name in the ignored ear. It's called the cocktail party effect.", "#psychology #brain #cocktailpartyeffect #facts #shorts", "Do you ever think you hear your name when no one said it? Yes or no.", "You're listening without knowing it"),
"s07": ("What's the happiest way to spend $40? Working adults felt happier on the day they spent $40 on a time-saving purchase (a cleaner, a delivery, a ride) than on a material one. Yet very few people say they'd spend extra money that way.", "#psychology #money #happiness #wealth #shorts", "What would you buy more time for: cooking, cleaning or commuting?", "$40 on stuff vs $40 on time"),
}
FILES = {k: f"{k} – {v['title'].split(' ')[0]}" for k, v in SHORTS.items()}
o = ["# Upload sheet – week of 16–22 Nov 2026 (batch 2026-11-14)", "",
"7 Shorts, one per day, **alternating 12:00 and 16:00 Amsterdam** (slot test) + long video 02 on **Sun 22 Nov 18:00**.", "",
"**Same settings for every Short:** Playlist \"Psychology that moves you\" · Category Education · Not made for kids · Altered/synthetic content: **No** (real stock footage + standard AI narrator, no realistic AI people) · Remixing on · Thumbnail frame ~0:01 (hook card visible).",
"**Related video (all 7):** \"Why Your Brain Is Bad With Money\" (long 01, live Sun 15 Nov). The last 2.5 s of every Short shows \"Full video: tap the link below\".",
"**Experiment this week:** add a **Poll sticker** to s03 (\"Would you notice the swap? Yes / No\") – the only Short with a sticker (playbook §5).", "", "---", ""]
for k, v in SHORTS.items():
    desc, tags, pin, card = D[k]
    o += [f"## {k} · {v['slot']} · angle: {v['angle']} · predicted: {v['predicted']}",
          f"**File:** `{k}.mp4` · **Hook card:** {card} · **Ending:** {v['ending']}",
          f"**Title:** {v['title']}", "**Description:**", "```",
          desc, f"Source: {SOURCES[k]}",
          "Science-backed psychology · Sources in description · " + ("Not financial advice." if v['angle']=='wealth' else "Not medical advice."),
          tags, "```", f"**Pinned comment:** {pin}", "", "---", ""]
o += [f"# Long video 02 – {LONG_TITLE}", "",
"**File:** `long02.mp4` (1920×1080, −14 LUFS) · **Upload from desktop Studio** (needed for Test & compare) · **Schedule: Sun 22 Nov 18:00 Amsterdam** · **Predicted:** medium (trend-aligned 'quiet luxury / looking rich' topic; channel still tiny).", "",
"**Title:** The Psychology of Looking Rich (7 Real Studies)", "Title alternatives (for a later re-package): \"Why Rich People Hide Their Logos (7 Studies)\" · \"Why Expensive Things Feel Better (7 Studies)\"", "",
"**Thumbnails – Test & compare (upload all 3):**", "- A `thumb_A_quiet_rich.jpg` – \"QUIET = RICH\"", "- B `thumb_B_wine.jpg` – \"$5 OR $45?\"", "- C `thumb_C_fake.jpg` – \"FAKE = CHEAT?\"", "",
"**Description:**", "```",
"The psychology of looking rich: why the most expensive bags have the smallest logos, why a price tag changes how wine tastes in your brain, and why half of people would take less money just to be richer than everyone around them. 7 real studies on status, luxury and money psychology – and one thing to try from each today.",
"", "CHAPTERS_PLACEHOLDER", "", "Studies:"] + [f"{i+1}. {s}" for i, (t, s) in enumerate(LONG_SOURCES)] + ["",
"This video explains psychology research about status, luxury and how the brain handles money. It is not financial advice.",
"Science-backed psychology · New Shorts every day.", "#psychology #moneypsychology #oldmoney", "```", "",
"**Settings:** Category Education · Not made for kids · Altered/synthetic: No · Playlist \"The Psyched Mind – Weekly Psychology\" · Chapters on (from description) · Automatic concepts on, check it.",
"**Tags:** psychology of looking rich, old money vs new money, quiet luxury psychology, status symbols psychology, luxury brands psychology, red sneakers effect, counterfeit self, scarcity effect, price placebo, money psychology",
"**End screen (last ~10 s):** video element → \"Why Your Brain Is Bad With Money\" + Subscribe.",
"**Cards:** at the logo item → Short s04 (\"Why your coffee card comes with free stamps\") once live.",
"**Pinned comment:** \"Old money or new money – which one are you? 👀\"", "",
"## After publishing (user)",
"1. Start Test & compare with the 3 thumbnails (desktop Studio). Don't change title/thumbnail during the test.",
"2. Set the Related video of the 23 Nov+ Shorts to this video (next batch will say so).",
"3. Once a month: re-package the worst-CTR long video – first check is 13 Dec (only 2 long videos so far).", ""]
open(os.path.join(os.path.dirname(__file__), "upload-sheet.md"), "w").write("\n".join(o))
print("ok")
