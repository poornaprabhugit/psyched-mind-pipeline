import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SHORTS, SOURCES, LONG, LONG_TITLE, LONG_SOURCES
out = ["# Batch 2026-11-14 – scripts", "",
       "Ideas → titles → scripts (playbook §4–6). Shorts follow the 14 Nov hook-first decisions plus Studio's notes on the card Short (payoff in the first 4–5 s, contrast hook cards, no wind-down at the end).", ""]
for k, v in SHORTS.items():
    out += [f"## {k} · {v['angle']} · {v['slot']} · predicted {v['predicted']}",
            f"**Title:** {v['title']}  ", f"**Hook card:** {v['hook_text']}  ", f"**Ending:** {v['ending']}  ",
            f"**Source:** {SOURCES[k]}", "", " ".join(t for t, _ in v["lines"]), ""]
out += [f"# Long video 02 – {LONG_TITLE}", ""]
for k, (title, lines) in LONG.items():
    out += [f"## {k} · {title or 'Opening (0:00–0:45)'}", "", " ".join(t for t, _ in lines), ""]
out += ["## Sources", ""] + [f"{i+1}. {t}: {s}" for i, (t, s) in enumerate(LONG_SOURCES)]
open(os.path.join(os.path.dirname(__file__), "scripts.md"), "w").write("\n".join(out) + "\n")
print("ok")
