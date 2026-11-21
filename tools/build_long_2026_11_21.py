"""Build jobs/2026-11-21-long/render.json from the approved script lines, the visual picks and the diagrams."""
import json, glob, sys
sys.path.insert(0, '/tmp/claude-0'); from long_lines import L
P = {}
for f in glob.glob('/home/claude/picks/long_*.json'): P.update(json.load(open(f)))
D = 'repo:assets/2026-11-21-long/'
DIAG = {('L1', 6): 'd01_doorway_setup', ('L1', 8): 'd02_doorway_result', ('L1', 12): 'd03_rooms',
        ('L2', 7): 'd04_nextinline_a', ('L2', 8): 'd05_nextinline_b', ('L3', 7): 'd06_curve_a', ('L3', 8): 'd07_curve_b',
        ('L4', 3): 'd08_cold_a', ('L4', 4): 'd09_cold_b', ('L4', 7): 'd10_cold_result', ('L4', 15): 'd11_speed',
        ('L4', 18): 'd12_glass', ('L5', 22): 'd13_retrieval'}
CH = {'L0': None, 'L1': 'Morning: the doorway', 'L2': 'Work: the name you lost', 'L3': 'Lunch: why rereading fails',
      'L4': "Evening: the day you remember", 'L5': 'Night: sleep, and the answer'}
CHAP = dict(CH, L0='Why does your brain drop things?')
shorts = set()
for f in glob.glob('jobs/*/render.json'):
    if '-long' in f: continue
    for v in json.load(open(f))['videos']: shorts.update(v.get('clips', []))
vids, used, dropped = [], set(), 0
for seg, lines in L.items():
    pk = {x['n']: x['clips'] for x in P[seg]}
    out = []
    for i, (text, _) in enumerate(lines, 1):
        if (seg, i) in DIAG:
            clips = [D + DIAG[(seg, i)] + '.mp4']
        else:
            clips = []
            for u in pk.get(i, []):
                if u in shorts or u in used: dropped += 1; continue
                clips.append(u); used.add(u)
            if not clips: print('EMPTY', seg, i, text[:50])
        out.append({'text': text, 'clips': clips})
    v = {'id': seg, 'subject': CHAP[seg], 'chapter': CHAP[seg], 'lines': out,
         'settings': {'video_aspect': '16:9', 'video_clip_duration': 4, 'subtitle_position': 'bottom', 'font_size': 64,
                      'bgm_type': '', 'bgm_volume': 0.0, 'voice_rate': 0.92, 'subtitle_display_mode': 'sentence',
                      'subtitle_animation': 'none'}}
    if CH[seg]: v['title_card'] = CH[seg]
    vids.append(v)
job = {'videos': vids, 'tighten': True, 'tighten_gap': 0.6, 'long': {'id': 'long03', 'segments': list(L)}}
json.dump(job, open('jobs/2026-11-21-long/render.json', 'w'), indent=1)
print('segments', len(vids), 'lines', sum(len(v['lines']) for v in vids), 'dropped (Shorts overlap/dup)', dropped)
