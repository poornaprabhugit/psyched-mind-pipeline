"""Shorts: order clips so each MPT slot (3 x 1.5 s fast-open, then 3 s each) shows a clip picked for the line
being spoken at that moment. Line times come from the first render's audio (pauses = sentence ends)."""
import json, re, subprocess, sys, math
sys.path.insert(0, 'tools'); import build_shorts_2026_11_21 as B
M = {
'p01': {1:['P ph1 1 0','P ph1 1 3'],2:['S p01 2 3','S p01 2 2'],3:['S p01 3 1','P ph1 1 7'],4:['P ph1 2 0','P ph1 2 7'],5:['S p01 5 0','S p01 5 7'],6:['S p01 6 4'],7:['S p01 7 5','S p01 1 0']},
'p02': {1:['P ph1 3 7','P ph1 3 0'],2:['P ph1 4 0','P ph1 4 2'],3:['P ph1 5 2','P ph1 5 7'],4:['P ph2 1 7'],5:['P ph2 2 4','P ph2 2 0'],6:['S p02 6 3','S p02 6 5'],7:['P ph2 3 2','P ph2 3 3']},
'p03': {1:['P ph2 4 3','P ph2 4 4'],2:['S p03 2 0','S p03 2 3'],3:['P ph2 4 1','P ph2 4 7'],4:['S p03 4 5','S p03 4 6'],5:['S p03 5 0'],6:['S p03 7 6'],7:['P ph2 4 0']},
'p04': {1:['P ph3 3 1','P ph2 5 2'],2:['P ph3 1 5','P ph3 1 2'],3:['P ph3 3 0','P ph3 3 3'],4:['P ph3 2 7','P ph3 2 6'],5:['P ph3 2 3','P ph3 3 4'],6:['P ph3 4 6','P ph3 3 2'],7:['P ph3 3 5']},
'p05': {1:['S p05 1 0','S p05 1 5'],2:['P ph3 5 2','P ph3 5 1','P ph3 5 0'],3:['S p05 3 0','S p05 3 4'],4:['S p05 4 1','S p05 4 7'],5:['S p05 5 0','S p05 5 1'],6:['S p05 6 2','S p05 6 6']},
'p06': {1:['G g01 5 2','G g01 5 4'],2:['S p06 2 1','S p06 2 2'],3:['S p06 2 7'],4:['P ph4 1 5','S p06 4 3'],5:['S p06 5 2','G g01 5 6'],6:['G g01 5 3']},
'p07': {1:['S p07 1 2','S p07 1 7'],2:['G g05 1 0','S p07 2 4','S p07 2 6'],3:['P ph1 3 2'],4:['P ph3 4 7'],5:['S p07 6 2'],6:['S p07 5 6','S p07 6 7'],7:['S p07 7 1','S p07 7 2']},
'p08': {1:['P ph4 2 5','P ph4 2 0'],2:['S p08 2 5','S p08 2 2'],3:['S p08 3 4','S p08 3 2'],4:['P ph4 2 4','P ph4 2 2'],5:['S p08 5 1'],6:['P ph4 2 1'],7:['S p08 7 6','S p08 7 3']},
'p09': {1:['S p09 1 0','S p09 1 4'],2:['S p09 2 0','S p09 2 2'],3:['S p09 3 7','S p09 3 4'],4:['S p09 4 2','S p09 4 4'],5:['S p09 5 0'],6:['S p09 6 6','S p09 6 0'],7:['S p09 7 6','S p09 7 0']},
'p10': {1:['P ph4 4 0','P ph4 4 4'],2:['P ph4 5 3','S p10 2 6'],3:['P ph4 5 5','P ph4 5 4'],4:['P ph4 5 6','S p10 4 5'],5:['S p10 5 0','S p10 5 1','S p10 5 6'],6:['S p10 6 4','S p10 6 0'],7:['P ph4 4 3']},
'p11': {1:['P ph5 1 0','P vd1 4 4'],2:['P ph5 1 2','S p11 2 1'],3:['S p11 3 1','S p11 3 3'],4:['S p11 4 0','S p11 4 6'],5:['P ph5 1 3','P ph5 2 6'],6:['P ph5 2 7','S p11 6 1']},
'p12': {1:['P ph5 3 2','P ph5 3 3'],2:['S p12 2 1','S p12 2 0'],3:['P ph5 3 7'],4:['S p12 4 0','S p12 4 1','S p12 4 2'],5:['S p12 5 5','S p12 5 1'],6:['S p12 6 0']},
'p13': {1:['P ph1 3 3','P ph1 3 6'],2:['S p13 2 5'],3:['P ph1 3 1'],4:['G g09 5 7'],5:['G g09 3 7','G g09 3 2'],6:['S p13 6 7'],7:['G g09 1 0']},
'p14': {1:['P ph6 1 2','P ph6 1 0'],2:['S p14 2 3','S p14 2 6'],3:['P ph6 1 6','S p14 3 3'],4:['S p14 4 5','S p14 4 6'],5:['S p14 5 3','S p14 5 1'],6:['S p14 6 5','S p14 6 2']},
}
def pauses(f):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=n=-33dB:d=0.35", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", e)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    return list(zip(st, en))
def line_times(lines, f):
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    ps = [(a, b) for a, b in pauses(f) if 0.3 < a and b < total - 0.3]
    # speech spans between pauses
    spans, t = [], 0.0
    for a, b in ps: spans.append((t, a)); t = b
    spans.append((t, total))
    speech = sum(b - a for a, b in spans)
    chars = [len(l) for l in lines]; tot = sum(chars)
    # map cumulative char fraction -> time through speech spans
    def at(frac):
        need = frac * speech
        for a, b in spans:
            if need <= b - a: return a + need
            need -= b - a
        return total
    starts, c = [], 0
    for n in chars: starts.append(at(c / tot)); c += n
    return starts, total
search = {v['id']: [l['text'] for l in v['lines']] for v in json.load(open('jobs/2026-11-21/search.json'))['videos']}
job = json.load(open('jobs/2026-11-21/render.json'))
allurls = {}
for v in job['videos']:
    vid = v['id']; lines = search[vid]
    starts, total = line_times(lines, f'/home/claude/out/shorts/{vid}.mp4')
    slots = [0, 1.5, 3.0] + [4.5 + 3 * k for k in range(math.ceil((total - 4.5) / 3) + 1)]
    used = {n: 0 for n in M[vid]}; order = []
    for s in slots:
        mid = s + (0.75 if s < 4.5 else 1.5)
        ln = max(i + 1 for i, st in enumerate(starts) if st <= mid)
        # next unused clip of this line, else of the nearest following/previous line with spares
        for cand in [ln] + [ln + d for d in (1, -1, 2, -2, 3, -3)]:
            if cand in M[vid] and used[cand] < len(M[vid][cand]):
                order.append(M[vid][cand][used[cand]]); used[cand] += 1; break
    v['clips'] = [B.url(r) for r in order]
    for u in v['clips']:
        assert u not in allurls, (vid, u, allurls.get(u)); allurls[u] = vid
    print(vid, f'{total:.1f}s', 'lines@', [round(x, 1) for x in starts], '->', len(order), 'clips:', ' | '.join(order))
json.dump(job, open('jobs/2026-11-21/render.json', 'w'), indent=1)
