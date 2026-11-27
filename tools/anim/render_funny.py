import base64,subprocess,os,json,numpy as np,wave
from playwright.sync_api import sync_playwright
V='/home/claude/psyched-mind-pipeline/assets/voice/2026-11-27-voice/p02_lost_ticket'
SR=24000
raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',V+'.mp3','-ac','1','-ar',str(SR),'-f','s16le','-'])
a=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
words=json.load(open(V+'.words.json'))
pauses=[]  # comedy beats
for at,d in sorted(pauses,reverse=True):
    i=int(at*SR);a=np.concatenate([a[:i],np.zeros(int(d*SR),np.float32),a[i:]])
    for w in words:
        if w['start']>=at: w['start']+=d;w['end']+=d
adur=len(a)/SR;dur=round(adur+0.3,2)
# ---------- SFX synth ----------
rng=np.random.default_rng(1)
def env(n,att=0.005,rel=0.1):
    t=np.arange(n)/SR;e=np.minimum(1,t/att)*np.exp(-t/rel);return e
def lp(x,k):  # simple moving-average lowpass
    return np.convolve(x,np.ones(k)/k,mode='same')
def whoosh(d=0.6):
    n=int(d*SR);x=rng.standard_normal(n);t=np.linspace(0,1,n)
    out=np.zeros(n)
    for k,w in [(30,1),(12,0.6)]: out+=lp(x,k)*w
    return out*np.sin(np.pi*t)**2*0.5
def sweep(f0,f1,d,vib=0,amp=0.35,rel=None):
    n=int(d*SR);t=np.arange(n)/SR;f=np.linspace(f0,f1,n)+vib*np.sin(2*np.pi*14*t)*f0*0.08
    ph=2*np.pi*np.cumsum(f)/SR;e=env(n,0.004,rel or d/2)
    return np.sin(ph)*e*amp
def ding():
    n=int(0.9*SR);t=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*2637*t))*np.exp(-t/0.25)*0.25
def pop(): return sweep(900,220,0.07,amp=0.45,rel=0.03)
def pat():
    n=int(0.06*SR);return lp(rng.standard_normal(n),40)*env(n,0.002,0.015)*1.2
def puff():
    n=int(0.4*SR);return lp(rng.standard_normal(n),60)*np.sin(np.pi*np.linspace(0,1,n))*0.5
def kaching():
    n=int(0.7*SR);t=np.arange(n)/SR
    clk=lp(rng.standard_normal(n),3)*np.exp(-t/0.02)*0.4
    bell=(np.sin(2*np.pi*2093*t)+np.sin(2*np.pi*2637*t))*np.exp(-t/0.3)*0.18
    return clk+np.concatenate([np.zeros(int(0.05*SR)),bell[:-int(0.05*SR)]])
def flutter(d):
    n=int(d*SR);t=np.arange(n)/SR;x=lp(rng.standard_normal(n),8)
    return x*(0.5+0.5*np.sign(np.sin(2*np.pi*22*t)))*np.sin(np.pi*t/d)*0.25
def wah(): return sweep(420,180,0.7,vib=1,amp=0.3,rel=0.5)
def boing(): return sweep(220,520,0.35,vib=1,amp=0.3,rel=0.25)
# events in ANIMATION time
ev=[(0.05,whoosh(0.7)),(1.0,sweep(600,600,0.08,amp=0.0)),(1.5,sweep(330,260,0.18,amp=0.3,rel=0.1)),(2.5,ding()),
    (3.32,whoosh(0.45)*0.7),(3.68,pat()),(3.8,pat()),(3.92,pat()),(4.04,pat()),(4.12,pop()),(4.22,pop()),(4.3,puff()),
    (8.8,boing()),(13.4,wah()),(17.55,kaching()),(18.05,flutter(1.6))]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/anim/anim.html')
    pg.evaluate(f"setupSync('V1',{json.dumps(words)},{adur})")
    m=pg.evaluate("SYNC.map")
    def a2v(ta):
        for i in range(len(m)-1):
            (v0,a0),(v1,a1)=m[i],m[i+1]
            if a0<=ta<a1: return v0+(ta-a0)/(a1-a0)*(v1-v0)
        return m[-1][0]
    mix=np.concatenate([a,np.zeros(int(0.3*SR)+10,np.float32)]).astype(np.float64)
    for ta,snd in ev:
        i=int(a2v(ta)*SR);snd=snd[:max(0,len(mix)-i)];mix[i:i+len(snd)]+=snd*0.55
    mix=np.clip(mix,-1,1)
    with wave.open('funny_audio.wav','wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes())
    n=int(dur*30);name='psyched_lost_ticket_funny_v3.mp4';tmp='tmp_'+name
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i','funny_audio.wav',
      '-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',tmp],stdin=subprocess.PIPE)
    for i in range(n):
        d=pg.evaluate(f"grabSync('V1',{i/30})");ff.stdin.write(base64.b64decode(d.split(',')[1]))
    ff.stdin.close()
    if ff.wait()==0: os.rename(tmp,name); print(name,n,dur)
