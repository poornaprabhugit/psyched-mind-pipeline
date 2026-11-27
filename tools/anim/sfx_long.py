import numpy as np,json,subprocess,wave
from playwright.sync_api import sync_playwright
from render_long import V,adur,GAP
SR=48000;rng=np.random.default_rng(7)
def env(n,att=0.005,rel=0.1):
    t=np.arange(n)/SR;return np.minimum(1,t/att)*np.exp(-t/rel)
def lp(x,k): return np.convolve(x,np.ones(k)/k,mode='same')
def sweep(f0,f1,d,vib=0,amp=0.35,rel=None):
    n=int(d*SR);t=np.arange(n)/SR;f=np.linspace(f0,f1,n)+vib*np.sin(2*np.pi*14*t)*f0*0.08
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.004,rel or d/2)*amp
def noise(d,k,amp,shape='hump'):
    n=int(d*SR);x=lp(rng.standard_normal(n),k);t=np.linspace(0,1,n)
    return x*(np.sin(np.pi*t)**2 if shape=='hump' else np.exp(-t*8))*amp
def add(a,b):
    n=max(len(a),len(b));o=np.zeros(n);o[:len(a)]+=a;o[:len(b)]+=b;return o
S={
 'thud':lambda: add(sweep(140,45,0.25,amp=0.9,rel=0.08),noise(0.12,60,0.6,'dec')),
 'whoosh':lambda: noise(0.7,25,0.55),
 'ding':lambda: (lambda t:(np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*2637*t))*np.exp(-t/0.3)*0.28)(np.arange(int(0.9*SR))/SR),
 'pop':lambda: sweep(900,220,0.07,amp=0.5,rel=0.03),
 'boing':lambda: sweep(220,520,0.4,vib=1,amp=0.3,rel=0.3),
 'slurp':lambda: noise(0.45,6,0.25)*np.sin(np.linspace(0,30,int(0.45*SR)))**2,
 'buzz':lambda: np.sign(np.sin(2*np.pi*90*np.arange(int(0.8*SR))/SR))*np.exp(-np.arange(int(0.8*SR))/SR/0.5)*0.08,
 'tweet':lambda: np.concatenate([sweep(2200,3000,0.08,amp=0.2,rel=0.05) for _ in range(4)]),
 'brr':lambda: np.concatenate([noise(0.03,3,0.35,'dec') for _ in range(18)]),
 'slide':lambda: sweep(1400,300,0.6,amp=0.25,rel=0.5),
 'screech':lambda: add(noise(0.5,4,0.35),sweep(1800,1500,0.5,amp=0.08)),
 'plink':lambda: sweep(1800,1700,0.15,amp=0.25,rel=0.06),
 'flutter':lambda: lp(rng.standard_normal(int(1.4*SR)),8)*(0.5+0.5*np.sign(np.sin(2*np.pi*22*np.arange(int(1.4*SR))/SR)))*np.sin(np.pi*np.arange(int(1.4*SR))/int(1.4*SR))*0.22,
 'bonk':lambda: sweep(500,300,0.12,amp=0.4,rel=0.05),
 'pat':lambda: noise(0.06,40,1.0,'dec'),
 'wah':lambda: sweep(420,180,0.7,vib=1,amp=0.3,rel=0.5),
}
def build(chapters):
    starts=[];acc=0
    for n in chapters: starts.append(acc);acc+=adur(n)+GAP
    total=np.zeros(int((acc+1)*SR))
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page(viewport={'width':1920,'height':1080})
        pg.goto('file:///home/claude/anim/long.html')
        for n,st in zip(chapters,starts):
            w=json.load(open(V+f'ch{n:02d}.words.json'));pg.evaluate(f"setChapter({n},{json.dumps(w)},{adur(n)+GAP})")
            for t,name in pg.evaluate("sfxList()"):
                if t>1e6: continue
                snd=S[name]();i=int((st+t)*SR);total[i:i+len(snd)]+=snd[:max(0,len(total)-i)]*0.5
    with wave.open('sfx_track.wav','wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(total,-1,1)*32767).astype(np.int16).tobytes())
    return acc
if __name__=='__main__':
    import sys;print(build([int(x) for x in sys.argv[1:]]))
