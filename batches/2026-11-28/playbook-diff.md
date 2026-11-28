# Proposed changes – batch 2026-11-28 (waiting for the user; NOT applied)

## 1. Playbook: no change proposed this week
This week's research check (memory/research-log.md, 28 Nov) found nothing new for 21–28 Nov that touches Shorts, YPP, AI/originality, or Instagram/Facebook. The 25 Nov test design is already logged (playbook lines 159–162).

## 2. Tooling fix (not a strategy change; apply only after the user OKs it)
Since 16 Nov 2026 the YouTube Data API no longer defaults `paidProductPlacementDetails.hasPaidProductPlacement` to false (https://developers.google.com/youtube/v3/revision_history). Our uploads have no paid placement, so the field should say so explicitly:

```diff
--- a/scripts/upload.py
+++ b/scripts/upload.py
@@ (body built for videos.insert)
-    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
-              "containsSyntheticMedia": bool(v.get("synthetic", False))}
+    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
+              "containsSyntheticMedia": bool(v.get("synthetic", False))}
+    body["paidProductPlacementDetails"] = {"hasPaidProductPlacement": False}
+    # and request part "snippet,status,paidProductPlacementDetails"
```
Manual Studio uploads are not affected: Studio asks the question itself (answer "No").

## 3. Timing note for the share test (for the user to confirm)
The 25 Nov decision says "verdict ~7 Dec". By 7 Dec every Short has day-1 numbers, but only the Monday pair has day-7 numbers (the Sunday pair reaches day 7 on 13 Dec). The proposal is a day-1 read on 7 Dec and the day-7 verdict on 13 Dec.
