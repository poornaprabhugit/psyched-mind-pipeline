# Proposals 2026-11-20 – subscriber & like conversion

**Status (user, 20 Nov): P1 APPROVED for the 21 Nov batch (Shorts 23–29 Nov); judge it, then decide how to continue. P2–P4 not approved (not run).**

Evidence: `memory/research-log.md` (2026-11-20). Our numbers: 9.0 likes per 1k views vs a median of 30.8 at 45 top psych/facts Shorts channels. ~1.2 subs per 1k views. 40 likes per 1k *engaged* views, so viewers who stay do convert. One variable per week. Measure likes/1k, subs/1k (Analytics) and stayed-to-watch per Short. Below ~1,000 views per arm, read the result as a direction only.

## P1 – On-screen follow card, 7 vs 7 (batch 28 Nov)
Evidence: weak (anecdote, ~1.6× vs no CTA). It is cheap, and the voice and loop stay unchanged, so retention should not suffer.
```diff
 render.json (7 of 14 Shorts, balanced: 2 brain-money, 4 brain-memory, 1 health; 4 at 12:00 / 3 at 16:00)
+ "cta_text": "Follow for a new brain fact every day"   # last 2.5 s, small, bottom; voice keeps looping
 (other 7 Shorts: no card)
```

## P2 – Spoken 3–4 word ask vs loop, 7 vs 7 (week after P1, only if the user wants it)
Evidence: weak (one 2015 long-form source: spoken ask 1 in 115 vs none 1 in 1,500). Risk: it breaks the loop ending, which is our default, so retention could drop. That is why it is a separate week.
```diff
- …That's why ↻ (loops into line 1)
+ …Follow for more brain facts.   # 7 of 14 Shorts, balanced as P1
```

## P3 – Make the Shorts → long bridge real (action, not a test)
Evidence: YouTube documents the Related video link as the Shorts → long path (playbook §2/§5). Galloway's data shows long videos convert more subscribers per view (weak). Long 02 has 1 view in 5.6 days.
```diff
+ User: check that Related video is set on every public Short since 14 Nov (it points to long 02 until the 22 Nov long video is live, then to the new one)
+ From the 22 Nov long video on: the "Full video: tap the link below" card on all Shorts that go live after it (already the rule; check it is applied)
```

## P4 – Watch 10 top Shorts for their CTAs before deciding P2 (research, ~15 min)
We don't know if top channels use spoken CTAs; the API has no transcripts. Pull captions/transcripts for the top 10 Shorts of 5 US/IN/GB channels from research/psych-shorts-2026-11-17.json and count CTA use (spoken/on-screen, timing).

Not proposed (no evidence): numbered series titles (0/45 top channels), pinned-comment changes, channel trailer, community posts.
