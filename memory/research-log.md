# Research log

## 2026-11-20 – Turning viewers into subscribers and likes (user request, 19 Nov)

**Question:** Why do our viewers rarely like or subscribe, and which tested changes could raise that conversion? This feeds the 28 Nov batch (proposals in `batches/proposals-2026-11-20-conversion.md`, waiting for the user's decision).

**Short answer:** Our like rate is about a third of the rate at top psychology/facts Shorts channels. Our subscriber rate is too small to measure (3 subs in Analytics, all from doorway). YouTube does not say that likes or subscriber counts push a video by themselves. Instead it describes per-viewer satisfaction signals: watch time, likes, shares and surveys. Subscribers skip ~90% of uploads. The best-supported lever is still the one we already know: most viewers swipe away in the first seconds (~80%), so very few are left to like or subscribe. The only measured comparison of subscribe CTAs we could find is old, long-form and weak. It shows a spoken ask far ahead of on-screen text, and on-screen text ahead of nothing. There is no evidence for series titles, pinned comments, trailers or community posts.

### (a) What YouTube says (opened pages)
- Likes, dislikes, subscriptions and surveys are used **per viewer**. Likes "predict the likelihood that you will be interested in similar videos". Surveys help the system "understand satisfaction, not just watch time". [YT] https://support.google.com/youtube/answer/16089387
- "People are more likely to be satisfied by videos that they share or like." Only 4–5-star survey answers count as "valued watchtime". How much each signal weighs differs per viewer. [YT, Cristos Goodrow, 15 Sep 2021] https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
- Shorts: a view should "encode for your intent of watching". "The audience is the algorithm." Analytics shows viewed vs swiped away. [YT staff Todd Sherman, via SEJ, 28 Aug 2023] https://searchenginejournal.com/youtube-explains-how-shorts-algorithm-works/494953
- Subscribers don't guarantee views. "90% of the time, your subscribed audience isn't deciding to watch." Subscriber click-through is "10% or less". "No metric on its own is a good indicator of value." [YT staff Todd Beaupré, Creator Insider via PPC Land, 1 Sep 2026] https://ppc.land/subscribers-skip-90-of-uploads-in-their-feed-youtube-director-says/
- **Not on record:** we found no YouTube statement that a video's like total or the channel's subscriber count is a direct ranking factor. We also found none saying they are not. Don't claim either.

### (b) Our conversion vs benchmarks (stats 2026-11-20 07:35 UTC)
| Video | Views | Likes | Likes/1k | Subs (Analytics) |
|---|---|---|---|---|
| Free chocolate (n04) | 748 | 8 | 10.7 | – (lag) |
| Doorway (r1) | 724 | 11 | 15.2 | 3 (4.1/1k) |
| Because (n02) | 242 | 0 | 0 | 0 |
| Choice blindness (s03) | 182 | 1 | 5.5 | – |
| Can't-sleep | 113 | 0 | 0 | 0 |
| Sunk cost (s02) | 89 | 0 | 0 | 0 |
| **Channel** | 2,441 | 22 | **9.0** | 3 in Analytics (6 total, 3 on launch day 10 Nov) → **~1.2/1k** |
- **Per engaged view** (Analytics, all videos to ~17 Nov): 12 likes / 299 engaged views = 40 per 1k engaged views. Doorway is 11/160 = 69 per 1k engaged. Read: the viewers who stay do like at a normal rate. The problem is that ~80% leave before they could.
- **Top channels, our own pull** (research/psych-shorts-2026-11-17.json): 45 psychology/facts Shorts channels (US/IN/GB search, ≥50K subs). For Shorts ≤180 s with ≥1,000 views, the median **likes per 1k views is 30.8** (IQR 21.6–41.0; this includes a few channels with hidden likes = 0). Lifetime subs per 1k channel views has a median of 3.3. That figure mixes in long videos and is survivor-biased. Some views in the sample predate the 24 Aug 2026 view-count change, which may inflate their like rates a little.
- Shorts get **1.4× more likes per view** than regular videos [study, Violot et al., WebSci '24, N = 9.88M Shorts + 6.86M videos from 70,712 channels] https://arxiv.org/html/2403.00454v1
- Engagement rate ((likes + comments + shares) ÷ views): Shorts 3.6%, long 2.9% [vendor, Dash Social, 630 brand channels, H1 2025] https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/youtube.pdf
- Long videos convert more subscribers per view than Shorts, except on channels with more than 1M subscribers [anecdote/small sample, Paddy Galloway, 33 channels/5,400 Shorts, Apr 2023] https://threadreaderapp.com/thread/1646898356419981315.html
- **Gap:** no large published study of subscribers per 1,000 Shorts views.

### (c) Tactics and how strong the evidence is
| Tactic | Evidence | Strength |
|---|---|---|
| Keep more viewers past the first seconds (hook) | Likes, shares and surveys can only come from viewers who stay. YouTube: viewed vs swiped. Our data: 40 likes per 1k engaged views vs 9 per 1k views | YT + Ours – strongest |
| Spoken subscribe ask | No CTA 1 in 1,500 · on-screen text 1 in 950 · voiceover 1 in 115 (2015, long-form, unnamed channels, no N) https://castfromclay.co.uk/how-to/increase-youtube-subscription-rates-by-200x | anecdote – weak |
| On-screen subscribe/follow text | same source (~1.6× vs none) | anecdote – weak |
| Related video link + spoken CTA (Shorts → long) | YouTube says the link is "designed to … encourage viewers to watch more of your content" https://support.google.com/youtube/answer/14075157 . AIR: ~0.5% click-through with link + verbal CTA vs 0.04% without (method not stated) https://air.io/en/audience-growth/do-youtube-shorts-help-your-long-form-videos-grow-data-from-18000-channels | YT (mechanism) + vendor |
| Deliver on the promise of the title/hook | Rene Ritchie (YouTube liaison), advice, not data https://www.searchenginejournal.com/youtube-algorithm-insights-from-creator-liaison-renee-ritchie/493901/ | YT advice |
| Series / numbered formats | None of the 45 top channels uses numbered-series titles on ≥20% of its Shorts (our pull). No study found | not supported |
| Pinned comment, trailer, community posts, watermark, end-screen subscribe | No measured effect found | not supported |

### (d) What top US/IN/GB psychology/facts Shorts channels do (our data)
- Lengths are mostly 35–60 s (17 Nov research). Numbered series in titles are rare: 0 of 45 channels at ≥20%.
- **Spoken/on-screen CTAs: unknown.** The API pull has titles and counts only, with no transcripts or frames, so we can't tell whether they say "follow for more". This needs a manual watch of ~10 top Shorts or a transcript pull. Treat it as an open question, not a pattern.

### Not supported by evidence
1. "Likes and subscriber count push a video into recommendations" (YouTube describes per-viewer satisfaction signals; no metric works alone).
2. "Subscribers see every upload" (they skip ~90%).
3. "Shorts are a strong subscriber engine for small channels" (the only data says long videos convert better per view).
