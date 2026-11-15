# Prediction log – how good is our judgment? (#36)

_Created 2026-11-15. Every batch writes a prediction (low/medium/high) per Short in predictions.csv **before** it goes live, with a one-line reason. The daily summary fills day-1 and day-7 views and stayed-to-watch % (when the user pastes Studio numbers)._

**Bands (set from our own data, revise monthly):** low < 50 day-1 views · medium 50–200 · high > 200. (Before 14 Nov every Short was under 70 on day 1; doorway did 607.)

**Scoring:** `actual_band` from day-1 views; `hit` = yes if predicted == actual. Weekly: hit rate overall and for "high" predictions. If the hit rate stays near chance (~33%) for 3 weeks, our idea-picking rules are not working → research what top channels' best Shorts have in common before changing them (playbook §00).
