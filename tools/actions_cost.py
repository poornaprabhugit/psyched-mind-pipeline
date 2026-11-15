"""Sum GitHub Actions billable minutes per day and workflow (fact base for cost per job, playbook #30).
Usage: python tools/actions_cost.py [since YYYY-MM-DD]  -> prints CSV rows: date,workflow,runs,billable_min,wall_min
Needs the gh CLI (session) – uses /actions/runs and /runs/{id}/timing."""
import json, subprocess, sys, collections, datetime as dt
since = sys.argv[1] if len(sys.argv) > 1 else "2026-11-01"
R = "repos/poornaprabhugit/psyched-mind-pipeline"
runs = json.loads(subprocess.run(["gh", "api", f"{R}/actions/runs?per_page=100&created=>={since}"], capture_output=True, text=True).stdout)["workflow_runs"]
agg = collections.defaultdict(lambda: [0, 0.0, 0.0])
for r in runs:
    t = json.loads(subprocess.run(["gh", "api", f"{R}/actions/runs/{r['id']}/timing"], capture_output=True, text=True).stdout or "{}")
    bill = sum(v.get("total_ms", 0) for v in (t.get("billable") or {}).values()) / 60000
    wall = (t.get("run_duration_ms") or 0) / 60000
    jobs = json.loads(subprocess.run(["gh", "api", f"{R}/actions/runs/{r['id']}/jobs?per_page=100"], capture_output=True, text=True).stdout or "{}").get("jobs", [])
    jm = 0.0
    for j in jobs:
        if j.get("started_at") and j.get("completed_at"):
            a = dt.datetime.fromisoformat(j["started_at"].replace("Z", "+00:00")); b = dt.datetime.fromisoformat(j["completed_at"].replace("Z", "+00:00"))
            jm += max(1, -(-(b - a).total_seconds() // 60))  # GitHub rounds each job up to the whole minute
    bill = bill or jm
    k = (r["created_at"][:10], r["name"])
    agg[k][0] += 1; agg[k][1] += bill; agg[k][2] += wall
print("date,workflow,runs,billable_min,wall_min")
for (d, w), (n, b, wl) in sorted(agg.items()):
    print(f"{d},{w},{n},{b:.1f},{wl:.1f}")
