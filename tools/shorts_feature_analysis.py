import json,re,math,statistics as st,collections,sys
d=json.load(open('research/psych-shorts-2026-11-17.json'))
CORE=['The Alpha Mind','Roar Within','MindZenX','Brain Related','Abhasa','Unlock The Mind','B.A Wardrobe','Silent Satyam','Zerox Mind','The Real Facts','Legacy Mindset','JD Inspiration','Mark on Earth','RID','Atharv Explains Why','ZIVROXY']
emo=re.compile('[\U0001F300-\U0001FAFF☀-➿]')
TOP={'love/attraction':r'\b(love|crush|attract\w*|girlfriend|boyfriend|relationship|partner|dating|likes you|ex)\b',
 'money/success':r'(\$|\bmoney\b|\brich\b|wealth|million|billion|business|success|poor|salary|broke)',
 'dark/power':r'\b(dark|manipulat\w*|power\w*|control|respect|aura|alpha|dominan\w*|psychopath\w*)\b',
 'brain/memory':r'\b(brain|memory|remember|forget|mind)\b',
 'body/health/sleep':r'\b(sleep|health\w*|body|eat|food|depress\w*|anxiety|stress)\b',
 'self-help rules':r'\b(rules?|habits?|ways|lessons?|tips?|steps?)\b',
 'signs/traits':r'\b(signs?|traits?|people who|if you)\b'}
def feats(t,dur):
    tl=t.lower(); f={}
    f['question ?']='?' in t
    f['starts Why']=tl.startswith('why')
    f['you/your']=bool(re.search(r'\byou(r|\'re)?\b',tl))
    f['starts with number']=bool(re.match(r'\s*\d',t))
    f['ALL-CAPS word']=bool(re.search(r'\b[A-Z]{3,}\b',re.sub(r'#\w+','',t)))
    f['emoji']=bool(emo.search(t))
    f['hashtag in title']='#' in t
    f['"psychology"']='psycholog' in tl
    f['"truth"/"secret"']=bool(re.search(r'\b(truth|secrets?|hidden)\b',tl))
    f['short title (<=7 words)']=len(re.sub(r'#\w+','',t).split())<=7
    for k,p in TOP.items(): f['topic: '+k]=bool(re.search(p,tl))
    for lo,hi in [(0,25),(26,40),(41,60),(61,180)]: f[f'length {lo}-{hi}s']=lo<=dur<=hi
    return f
rows=[]
for c in d['channels']:
    if not any(c['title'].startswith(x) for x in CORE): continue
    sh=[u for u in c['uploads'] if u['dur'] and u['dur']<=180 and (u['lang'] or 'en').startswith('en') and '2026-05-17'<=u['published']<='2026-11-10']
    if len(sh)<25: continue
    med=st.median(u['views'] for u in sh)
    for u in sh: rows.append(dict(ch=c['title'],subs=c['subs'],s=math.log2(max(u['views'],1)/med),v=u['views'],dur=u['dur'],t=u['title'],**{'f_'+k:v for k,v in feats(u['title'],u['dur']).items()}))
chs=sorted(set(r['ch'] for r in rows))
print('channels',len(chs),'shorts',len(rows))
for ch in chs:
    rr=[r for r in rows if r['ch']==ch]; print(f"  {ch[:22]:22} n={len(rr)} subs={rr[0]['subs']} med_dur={st.median(r['dur'] for r in rr)}")
fk=[k for k in rows[0] if k.startswith('f_')]
out=[]
for k in fk:
    diffs=[];nwith=0
    for ch in chs:
        rr=[r for r in rows if r['ch']==ch]
        a=[r['s'] for r in rr if r[k]]; b=[r['s'] for r in rr if not r[k]]
        if len(a)>=5 and len(b)>=5:
            diffs.append(st.median(a)-st.median(b)); nwith+=len(a)
    if len(diffs)>=4:
        m=st.mean(diffs); pos=sum(x>0 for x in diffs)
        out.append((k[2:],len(diffs),nwith,round(2**m,2),pos))
out.sort(key=lambda x:-x[3])
print(f"{'feature':32} chans  n_with  views_x  chans_up")
for o in out: print(f"{o[0]:32} {o[1]:5} {o[2]:7} {o[3]:8} {o[4]:3}/{o[1]}")
json.dump(rows,open(sys.argv[1],'w'))
