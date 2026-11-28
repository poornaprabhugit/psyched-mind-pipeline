# Builds upload-sheet.md and igfb-captions.md for batch 2026-11-28 (animation test).
LONG = "8 Ways Your Brain Tricks You Into Wasting Money"
S = [
 dict(b="B01", q="Q01", day="Mon 30 Nov", slot="12:00", arm="A", short="Lost wallet", hook="Found a wallet with cash. Return it?",
  title="Would you return a lost wallet with money in it? 👛",
  desc="Researchers turned in more than 17,000 \"lost\" wallets in 355 cities across 40 countries, including India. Wallets with no money came back 40% of the time. With about $13 inside: 51%. Most people, even economists, predicted the opposite.",
  src="Cohn, Maréchal, Tannenbaum & Zünd (2019), Science – https://doi.org/10.1126/science.aau8712",
  tags="lost wallet experiment, honesty psychology, wallet study, psychology facts, behavioral science",
  hashtags="#psychology #honesty #brainfacts #shorts", pin="Would you return it? Be honest 👇",
  ig="Found a wallet with cash. Would you return it? 👛\n\nIn 17,000+ \"lost\" wallets across 40 countries, the ones WITH money came back more often: 51% vs 40%."),
 dict(b="B02", q="Q02", day="Mon 30 Nov", slot="16:00", arm="K", short="Healthy later junk now", hook="Snack for next week: fruit or chocolate?",
  title="Why you choose healthy food for later, but not now 🍎",
  desc="200 office workers picked a snack they would get a week later, and many chose an apple or a banana. When they could choose again at the moment of eating, far more took chips or a chocolate bar. Future you plans well; right-now you wants the treat.",
  src="Read & van Leeuwen (1998), Organizational Behavior and Human Decision Processes – https://doi.org/10.1006/obhd.1998.2803",
  tags="healthy eating psychology, present bias, snack choice study, self control, psychology facts",
  hashtags="#psychology #food #brainfacts #shorts", pin="What's your 'right-now' snack? 🍫",
  ig="Snack for next week: fruit or chocolate? 🍎\n\nWorkers chose fruit for next week… but when they chose again right then, far more took chips or chocolate."),
 dict(b="B03", q="Q03", day="Tue 1 Dec", slot="12:00", arm="K", short="Turning down free money", hook="They keep $90, you get $10. Deal?",
  title="Why you'd turn down free money 💵",
  desc="In the ultimatum game, one person splits a sum and the other can accept (both get paid) or reject (nobody gets anything). Across 37 papers, people offered about 40% on average, and low offers were often rejected – people give up free money to punish an unfair split.",
  src="Güth, Schmittberger & Schwarze (1982), Journal of Economic Behavior & Organization; Oosterbeek, Sloof & van de Kuilen (2004), Experimental Economics – https://doi.org/10.1023/B:EXEC.0000026978.14316.74",
  tags="ultimatum game, fairness psychology, behavioral economics, psychology facts, free money",
  hashtags="#psychology #money #fairness #shorts", pin="$10 out of $100 – would you take it? 👇",
  ig="They keep $90, you get $10. Deal? 💵\n\nIn the classic ultimatum game, low offers often get turned down – even though saying no means nobody gets anything."),
 dict(b="B04", q="Q04", day="Tue 1 Dec", slot="16:00", arm="A", short="Takes longer", hook="Your paper: done in 34 days, or 56?",
  title="Why everything takes longer than you planned ⏳",
  desc="Students guessed when they would finish their honors thesis. Average guess: about 34 days. Actual: about 56. Fewer than 1 in 3 finished by their guess, and about half missed even their worst-case date. Psychologists call it the planning fallacy.",
  src="Buehler, Griffin & Ross (1994), Journal of Personality and Social Psychology – https://doi.org/10.1037/0022-3514.67.3.366",
  tags="planning fallacy, procrastination psychology, time estimation, psychology facts, productivity",
  hashtags="#psychology #planning #brainfacts #shorts", pin="How late was your last 'quick' project? ⏳",
  ig="Your paper: done in 34 days, or 56? ⏳\n\nStudents guessed 34 days. It took 56. About half missed even their worst-case date."),
 dict(b="B05", q="Q06", day="Wed 2 Dec", slot="12:00", arm="A", short="Stranger", hook="Talk to the stranger, or sit alone?",
  title="Is talking to strangers on the train worth it? 🚆",
  desc="Train commuters were asked to start a chat with a stranger or keep to themselves. Other commuters predicted the quiet ride would be nicer – but the talkers reported the more pleasant trip. A bus study found the same.",
  src="Epley & Schroeder (2014), Journal of Experimental Psychology: General – https://doi.org/10.1037/a0037323",
  tags="talking to strangers, social psychology, commute study, psychology facts, happiness",
  hashtags="#psychology #social #brainfacts #shorts", pin="Do you talk to strangers on your commute? 🚆",
  ig="Talk to the stranger, or sit alone? 🚆\n\nCommuters expected the quiet ride to be nicer. The ones who chatted had the more pleasant trip."),
 dict(b="B06", q="Q05", day="Wed 2 Dec", slot="16:00", arm="K", short="Drive to save 5", hook="Drive 20 minutes to save $5?",
  title="Would you drive 20 minutes to save $5? 🧮",
  desc="People were asked if they would drive 20 minutes to another store to save $5 on a calculator. On a $15 calculator, 68% said yes. On a $125 calculator, only 29%. Same $5 – we judge savings relative to the price.",
  src="Tversky & Kahneman (1981), Science – https://doi.org/10.1126/science.7455683",
  tags="mental accounting, relative thinking, behavioral economics, psychology facts, saving money",
  hashtags="#psychology #money #brainfacts #shorts", pin="Would you make the drive? 🚗",
  ig="Drive 20 minutes to save $5? 🧮\n\n68% said yes on a $15 calculator. Only 29% on a $125 one. Same $5."),
 dict(b="B07", q="Q07", day="Thu 3 Dec", slot="12:00", arm="K", short="Pre-checked box", hook="Check to join, or uncheck to leave?",
  title="Why you stick with the box that's already checked ☑️",
  desc="In an online study, people chose whether to be organ donors. When they had to check a box to join, far fewer joined. When they were in unless they unchecked it, about twice as many stayed in. The default made the choice for them.",
  src="Johnson & Goldstein (2003), Science – https://doi.org/10.1126/science.1091721",
  tags="default effect, nudge, organ donation study, psychology facts, decision making",
  hashtags="#psychology #nudge #brainfacts #shorts", pin="Do you ever uncheck the box? ☑️",
  ig="Check to join, or uncheck to leave? ☑️\n\nWhen 'yes' was already checked, about twice as many people stayed in. The default chose for them."),
 dict(b="B08", q="Q08", day="Thu 3 Dec", slot="16:00", arm="A", short="Old friend", hook="Text an old friend after a long time?",
  title="Should you text an old friend after years? 📱",
  desc="Across 13 preregistered studies with about 5,900 people, senders of a short surprise note to someone they hadn't talked to in a while kept underestimating how much it would be appreciated.",
  src="Liu, Rim, Min & Min (2023), Journal of Personality and Social Psychology – https://doi.org/10.1037/pspi0000402",
  tags="reaching out, friendship psychology, social connection, psychology facts, texting",
  hashtags="#psychology #friendship #brainfacts #shorts", pin="Who are you going to text today? 📱",
  ig="Text an old friend after a long time? 📱\n\nIn 13 studies, people guessed too low how much their surprise message would be appreciated."),
 dict(b="B09", q="Q09", day="Fri 4 Dec", slot="12:00", arm="A", short="Experience vs thing", hook="Concert ticket vs new jacket?",
  title="Do experiences make you happier than things? 🎟️",
  desc="In a national survey, 1,263 Americans thought of one purchase made to own and one made to do. 57% said the experience made them happier; 34% said the thing. Later research found limits, for example with bad experiences.",
  src="Van Boven & Gilovich (2003), Journal of Personality and Social Psychology – https://doi.org/10.1037/0022-3514.85.6.1193",
  tags="experiences vs things, happiness psychology, spending, psychology facts, experiential purchases",
  hashtags="#psychology #happiness #brainfacts #shorts", pin="Best thing you ever spent money on? 🎟️",
  ig="Concert ticket vs new jacket? 🎟️\n\n57% said an experience made them happier than a thing. 34% said the thing."),
 dict(b="B10", q="Q10", day="Fri 4 Dec", slot="16:00", arm="K", short="Scarf vs coat", hook="$45 scarf vs $55 coat. More generous?",
  title="Why a cheaper gift can seem more generous 🎁",
  desc="Each person heard about one gift only: a $45 scarf from a store where scarves cost $5–$50, or a $55 coat from a store where coats cost $50–$500. The scarf giver was seen as more generous – we judge a price against its range. A preregistered replication was mostly successful.",
  src="Hsee (1998), Journal of Behavioral Decision Making 11(2) – https://doi.org/10.1002/(SICI)1099-0771(199806)11:2%3C107::AID-BDM292%3E3.0.CO;2-Y",
  tags="gift giving psychology, less is better effect, generosity, psychology facts, holiday gifts",
  hashtags="#psychology #gifts #brainfacts #shorts", pin="Scarf or coat – which would you rather get? 🎁",
  ig="$45 scarf vs $55 coat. Which giver seems more generous? 🎁\n\nThe scarf giver – because $45 is the top of the scarf range, and $55 is the bottom of the coat range."),
 dict(b="B11", q="Q11", day="Sat 5 Dec", slot="12:00", arm="K", short="Thank-you note", hook="Send the thank-you, or skip it?",
  title="Is it weird to send a thank-you note? ✉️",
  desc="People wrote thank-you letters and guessed how the reader would feel. They put the reader's surprise at about 6 out of 10; readers said almost 8. Writers expected some awkwardness; readers felt very little.",
  src="Kumar & Epley (2018), Psychological Science – https://doi.org/10.1177/0956797618772506",
  tags="gratitude letter, thank you note, gratitude psychology, psychology facts, kindness",
  hashtags="#psychology #gratitude #brainfacts #shorts", pin="Who deserves a thank-you from you? ✉️",
  ig="Send the thank-you, or skip it? ✉️\n\nWriters guessed the reader's surprise at 6/10. Readers said almost 8 – and felt very little awkwardness."),
 dict(b="B12", q="Q12", day="Sat 5 Dec", slot="16:00", arm="A", short="Ordering", hook="Friend orders your pick first. Switch?",
  title="Why you change your order when friends go first 🍽️",
  desc="At a bar offering free samples of four beers, some tables ordered out loud one by one, others chose in private. Out loud, people picked something different from their friends – and liked it less. 38% wished they had picked another, vs 12% of private orderers.",
  src="Ariely & Levav (2000), Journal of Consumer Research – https://doi.org/10.1086/317585",
  tags="ordering food psychology, group decisions, social influence, psychology facts, restaurants",
  hashtags="#psychology #social #brainfacts #shorts", pin="Do you switch when a friend orders 'your' dish? 🍽️",
  ig="Your friend orders your pick first. Do you switch? 🍽️\n\nPeople ordering out loud picked something different – and liked it less."),
 dict(b="B13", q="Q13", day="Sun 6 Dec", slot="12:00", arm="A", short="Best job", hook="Best job or good-enough job?",
  title="Why chasing the best option can feel worse 🔍",
  desc="548 American students were followed through their first job search. Those aiming for the very best started on about 20% more pay – but felt more stressed and less happy with the job. One correlational study; not career advice.",
  src="Iyengar, Wells & Schwartz (2006), Psychological Science – https://doi.org/10.1111/j.1467-9280.2006.01677.x",
  tags="maximizers vs satisficers, job search psychology, decision making, psychology facts, happiness",
  hashtags="#psychology #career #brainfacts #shorts", pin="Are you a 'best' chaser or a 'good enough' person? 🔍",
  ig="Best job or good-enough job? 🔍\n\nBest-seekers earned about 20% more – and felt more stressed and less happy with the job."),
 dict(b="B14", q="Q14", day="Sun 6 Dec", slot="16:00", arm="K", short="Coin flip", hook="Quit or stay? Flip a coin.",
  title="What happens if you let a coin flip decide? 🪙",
  desc="In more than 22,000 coin tosses, volunteers stuck on a big choice, like quitting a job, let a coin decide. Heads (make the change) made them far more likely to do it, and six months later the changers were happier on average. This is one study of volunteers – the author calls the results suggestive – not advice to quit anything.",
  src="Levitt (2021), Review of Economic Studies – https://doi.org/10.1093/restud/rdaa016",
  tags="coin flip study, decision making, big life decisions, psychology facts, change",
  hashtags="#psychology #decisions #brainfacts #shorts", pin="Would you let a coin decide? 🪙",
  ig="Quit or stay? Flip a coin. 🪙\n\nIn 22,000+ tosses, people who got heads were more likely to make the change – and were happier on average 6 months later. One study, not advice."),
]
L = [f"# Upload sheet – batch 2026-11-28 · 14 Shorts (Mon 30 Nov – Sun 6 Dec) · animation test\n",
 "_Scripts v2 approved by the user on 28 Nov; built exactly as approved._\n",
 "**Test:** A = animated (code-drawn characters), K = stock footage. Same voice, hook card, captions, pacing and end card (\"Like & subscribe for a new brain fact every day\") on all 14. Judge ~13 Dec: stayed-to-watch %, avg % viewed, likes + subscribers per 1,000 views, shares, day-7 views per arm.\n",
 "## Schedule at a glance (Amsterdam time)\n\n| Day | 12:00 | 16:00 |\n|---|---|---|"]
for i in range(0, 14, 2):
    a, b = S[i], S[i + 1]
    L.append(f"| {a['day']} | **{a['b']}** {a['short']} · {a['arm']} | **{b['b']}** {b['short']} · {b['arm']} |")
L.append(f"""
**Same settings for every Short:**
- Playlist "Psychology that moves you" · Category Education · Not made for kids · Language: English (video + audio language).
- Altered/synthetic content: **No** (stock: real footage and photos + standard AI narrator; animated: clearly cartoon characters, which YouTube does not require disclosing).
- Thumbnail frame ~0:01 with the yellow hook card visible.
- **Related video = "{LONG}"** (long 04, live Sat 28 Nov 18:00). All 14 go live after it.
- Tags field: plain phrases, no "#".

---
""")
for s in S:
    kind = "animated" if s['arm'] == "A" else "stock"
    L.append(f"## {s['b']} · {s['day']} {s['slot']} · {s['q']} · arm {s['arm']} ({kind})")
    L.append(f"**File:** `{s['b']}_{s['day'].replace(' ','')}_{s['slot'].replace(':','')}_*.mp4` · **Hook card:** {s['hook']}")
    L.append(f"**Title:** {s['title']}")
    L.append("**Description:**\n```\n" + s['desc'] + "\nSource: " + s['src'] + f"\nFull video: {LONG} (Related video link above)\nScience-backed psychology · Sources in description · Not medical or financial advice.\n" + s['hashtags'] + "\n```")
    L.append(f"**Tags:** {s['tags']}")
    L.append(f"**Pinned comment:** {s['pin']}")
    L.append(f"**Related video:** {LONG}\n\n---\n")
open('upload-sheet.md', 'w').write("\n".join(L))
C = ["# Instagram + Facebook Reels – captions for 30 Nov – 6 Dec (14 Reels, 2 per day)\n",
 "Use the **_igfb** files (no \"Full video\" card; end card says \"Follow for a new brain fact every day\"). Schedule each Reel in **Meta Business Suite → Create reel** with **Instagram + Facebook both ticked**, same day and time as on YouTube (Amsterdam), at least 20 min ahead.\n",
 "**For every Reel:** paste the caption block as it is · cover = a frame with the yellow hook card (~0:01) · Audio: the video's own sound · AI label: off · max 5 hashtags.\n", "---\n"]
for s in S:
    src = s['src'].split(' – ')[0]
    C.append(f"## {s['day']} · {s['slot']} · {s['short']}  ({s['b']}, {'animated' if s['arm']=='A' else 'stock'})")
    C.append("```\n" + s['ig'] + f"\n\nSource: {src}\nFollow for one real psychology study a day 🧠\n" + s['hashtags'].replace(' #shorts', '') + "\n```\n")
open('igfb-captions.md', 'w').write("\n".join(C))
