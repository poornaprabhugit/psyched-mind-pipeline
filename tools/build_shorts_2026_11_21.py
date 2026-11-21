import json,re,glob
R='/home/claude/res/'
SRC={'S':R+'2026-11-21-search/{v}_candidates.json','G':R+'gap/{v}_candidates.json','P':R+'gap2/{v}_candidates.json'}
def url(spec):
    src,v,ln,k=spec.split(); ln=int(ln);k=int(k)
    d=json.load(open(SRC[src].format(v=v)))
    line=next(l for l in d['lines'] if l['n']==ln)
    return line['candidates'][k]['url']
def S(v,*refs): return [f"S {v} {r.replace('-',' ')}" for r in refs]
picks={
'p01':['P ph1 1 0','P ph1 1 3','S p01 2 3','S p01 2 2','S p01 3 1','P ph1 1 7','P ph1 2 0','P ph1 2 7','S p01 5 0','S p01 5 7','S p01 6 4','S p01 7 5','S p01 1 0'],
'p02':['P ph1 3 7','P ph1 4 0','P ph1 4 2','P ph1 5 2','P ph1 5 7','P ph2 1 7','P ph2 2 4','P ph2 2 0','S p02 6 3','S p02 6 5','P ph2 3 2','P ph2 3 3'],
'p03':['P ph2 4 3','S p03 2 0','S p03 2 3','P ph2 4 4','S p03 4 5','S p03 4 6','S p03 5 0','S p03 7 6','P ph2 4 7','P ph2 4 1'],
'p04':['P ph3 3 1','P ph2 5 2','P ph3 1 5','P ph3 1 6','P ph3 3 0','P ph3 3 3','P ph3 2 7','P ph3 2 6','P ph3 2 3','P ph3 3 4','P ph3 4 6','P ph3 3 2'],
'p05':['S p05 1 0','P ph3 5 2','P ph3 5 1','P ph3 5 0','S p05 3 0','S p05 3 4','S p05 4 1','S p05 4 7','S p05 5 0','S p05 5 1','S p05 6 2','S p05 6 6'],
'p06':['G g01 5 2','G g01 5 4','S p06 2 1','S p06 2 2','S p06 2 7','P ph4 1 5','S p06 4 3','S p06 5 2','G g01 5 3','G g01 5 6'],
'p07':['S p07 1 2','S p07 1 7','G g05 1 0','S p07 2 4','S p07 2 6','P ph1 3 2','P ph3 4 7','S p07 6 2','S p07 5 6','S p07 6 7','S p07 7 1','S p07 7 2'],
'p08':['P ph4 2 5','P ph4 2 0','S p08 2 5','S p08 2 2','S p08 3 4','S p08 3 2','P ph4 2 4','P ph4 2 2','S p08 5 1','S p08 6 0','S p08 7 6','S p08 7 3'],
'p09':['S p09 1 0','S p09 1 4','S p09 2 0','S p09 2 2','S p09 3 7','S p09 3 4','S p09 4 2','S p09 4 4','S p09 5 1','S p09 6 6','S p09 6 0','S p09 7 6','S p09 7 0'],
'p10':['P ph4 4 0','P ph4 4 4','P ph4 5 3','S p10 2 6','P ph4 5 5','P ph4 5 4','G g06 5 0','S p10 4 5','S p10 5 0','S p10 5 1','S p10 5 6','S p10 6 4','S p10 6 0','P ph4 4 3'],
'p11':['P ph5 1 0','P vd1 4 4','S p11 2 0','S p11 2 1','S p11 3 1','S p11 3 3','S p11 4 0','S p11 4 6','P ph5 2 6','P ph5 1 3','P ph5 2 7','S p11 6 1'],
'p12':['P ph5 3 2','P ph5 3 3','S p12 2 1','S p12 2 0','P ph5 3 7','S p12 4 0','S p12 4 1','S p12 4 2','S p12 5 5','S p12 5 1','S p12 6 0'],
'p13':['P ph1 3 3','S p13 2 5','P ph1 3 6','G g09 5 7','G g09 3 7','G g09 3 2','P ph1 3 1','S p13 7 1','P ph1 3 4'],
'p14':['P ph6 1 2','P ph6 1 0','S p14 2 3','S p14 2 6','P ph6 1 6','S p14 3 3','S p14 4 5','S p14 4 6','S p14 5 3','S p14 5 1','S p14 6 5','S p14 6 2'],
}
# scripts from approved file
txt=open('batches/2026-11-21/scripts.md').read()
meta={}
for m in re.finditer(r'## (P\d\d) ·[^\n]*\n\*\*Hook card:\*\* ([^\n]+)\n\*\*Title:\*\* ([^\n]+)\n\*\*Script[^\n]*\n([^\n]+)',txt):
    meta[m.group(1).lower()]=(m.group(2).strip(),m.group(3).strip(),m.group(4).replace('↻','').strip())
A={'p01','p04','p05','p08','p09','p12','p13'}
# earlier Shorts clips
old=set()
for f in glob.glob('jobs/*/render.json'):
    if '2026-11-21' in f: continue
    for v in json.load(open(f))['videos']:
        old.update(v.get('clips',[]))
seen={};vids=[]
for vid,refs in picks.items():
    urls=[url(r) for r in refs]
    for u,r in zip(urls,refs):
        if u in seen: print('DUP',vid,r,'also',seen[u])
        if u in old: print('OLDUSE',vid,r)
        seen[u]=(vid,r)
    hook,title,script=meta[vid]
    v={"id":vid,"subject":title,"script":script,"hook_text":hook,"cta_text":"Full video: tap the link below",
       "fast_open":{"clips":3,"seconds":1.5},"clips":urls}
    if vid in A:
        v["follow_text"]="Subscribe for a new brain fact every day"; v["follow_text_clean"]="Follow for a new brain fact every day"
    vids.append(v)
json.dump({"videos":vids,"tighten":True,"clean_variant":True},open('jobs/2026-11-21/render.json','w'),indent=1)
print(len(vids),'videos', sum(len(v['clips']) for v in vids),'clips'); 
for v in vids: print(v['id'],len(v['clips']),v['hook_text'],'|',v['script'][-25:], 'A' if 'follow_text' in v else 'B')

# list free candidates for lines of each short
if __name__=='__main__':
    import sys
    used=set(seen)
    for v in sorted({r.split()[1] for refs in picks.values() for r in refs if r.startswith('S')}):
        d=json.load(open(SRC['S'].format(v=v)))
        out=[]
        for l in d['lines']:
            free=[f"{l['n']}-{k}" for k,c in enumerate(l['candidates']) if c['url'] not in old and c['url'] not in used]
            out.append(f"L{l['n']}:{','.join(free)}")
        print(v,' '.join(out))
