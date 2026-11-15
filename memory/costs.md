# Cost per job (#30)

_Created 2026-11-15. Fact base: GitHub Actions job minutes measured with `tools/actions_cost.py` (each job rounded up to a whole minute, as GitHub bills). The weekly batch appends its week to costs.csv._

## What we pay with
- **GitHub Actions:** the repo is private, so runs use the account's included minutes. GitHub Free includes 2,000 Actions minutes per month for private repos (docs.github.com, checked 2026-11-15). Overage, if allowed by the account's spending limit, is billed per minute.
- **Claude usage:** scripting, clip picking (looking at contact sheets) and reviews use the user's Claude plan. Not measurable from the repo; use the explain-usage skill in a session when needed.
- **Your time:** uploading and scheduling (YouTube Studio + Meta Business Suite).

## Measured so far (10–15 Nov 2026): 745 job-minutes
- 14 Nov alone (7 Shorts, long video 02, 3 remakes, 7 extra Shorts, re-renders, clean versions): 491 job-minutes.
- A full week at the new format (14 Shorts + long video + IG/FB versions + 1–2 fix rounds) is likely **500–700 job-minutes**, i.e. **about 2,000–3,000 per month – at or over the free 2,000.**

## Options (user decides)
1. Make the repo public: Actions minutes on standard runners are free for public repos (docs.github.com). Downside: scripts, scripts' content and memory files become visible to anyone. Secrets stay secret.
2. Cut minutes: render IG/FB versions from the same run (one render job writes both variants) instead of a second full render; fewer re-render rounds.
3. Pay for extra minutes: usage beyond the included amount is billed to the account (docs.github.com). Check GitHub → Settings → Billing for the account's current Actions usage and any spending limit/budget before the month ends.
