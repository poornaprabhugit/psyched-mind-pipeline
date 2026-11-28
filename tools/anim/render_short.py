import base64,subprocess,os,json,sys,wave,numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0,'/home/claude/anim')
from sfx_long import S,SR
V='/home/claude/psyched-mind-pipeline/assets/voice/2026-11-28-avoice/'
TAIL=0.15
def find(id_):
    for f in os.listdir(V):
        if f.lower()==id_+'.mp3': return V+f
def adur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
MAXGAP=0.35
def tighten(mp3):
    w=json.load(open(mp3[:-4]+'.words.json'))
    a=np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',mp3,'-ac','1','-ar',str(SR),'-f','s16le','-']),dtype=np.int16).astype(np.float64)/32768
    out=[];shift=0.0;nw=[];prev_end=0.0;pos=0
    for i,x in enumerate(w):
        gap=x['start']-prev_end
        if i>0 and gap>MAXGAP:
            cut=gap-MAXGAP;c0=int((prev_end+MAXGAP/2)*SR);out.append(a[pos:c0]);pos=c0+int(cut*SR);shift+=cut
        nw.append({'w':x['w'],'start':round(x['start']-shift,3),'end':round(x['end']-shift,3)});prev_end=x['end']
    out.append(a[pos:]);return nw,np.concatenate(out)
def run(ids,mode,times=None):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page(viewport={'width':1080,'height':1920})
        errs=[];pg.on('console',lambda m:errs.append(m.text));pg.on('pageerror',lambda e:errs.append('ERR '+str(e)))
        pg.goto('file:///home/claude/anim/short.html')
        for id_ in ids:
            mp3=find(id_);w,a=tighten(mp3);d=round(w[-1]['end']+0.35,3)
            if mode=='shots':
                pg.evaluate(f"setShort('{id_}',{json.dumps(w)},{d},false)")
                for t in times:
                    data=pg.evaluate(f"frame({t})");open(f'S_{id_}_{t}.jpg','wb').write(base64.b64decode(data.split(',')[1]))
                continue
            for clean in [False,True]:
                pg.evaluate(f"setShort('{id_}',{json.dumps(w)},{d},{str(clean).lower()})")
                # sfx + voice mix
                mix=np.zeros(int((d+0.5)*SR));mix[:len(a)]+=a
                for t,name in pg.evaluate("sfxList()"):
                    if t>1e6:continue
                    snd=S[name]();i=int(t*SR);mix[i:i+len(snd)]+=snd[:max(0,len(mix)-i)]*0.45
                mix=mix[:int(d*SR)]
                with wave.open('tmp_mix.wav','wb') as f:
                    f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
                name=f"{id_}{'_clean' if clean else ''}.mp4";tmp='tmp_'+name;N=int(round(d*30))
                ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i','tmp_mix.wav',
                  '-af','loudnorm=I=-17:TP=-1.5:LRA=11','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',tmp],stdin=subprocess.PIPE)
                for i in range(N):
                    data=pg.evaluate(f"frame({i/30})");ff.stdin.write(base64.b64decode(data.split(',')[1]))
                ff.stdin.close()
                if ff.wait()==0: os.rename(tmp,name);print(name,N,d,flush=True)
        print(sorted(set(e for e in errs if 'MISSING' in e or 'ERR' in e)))
if __name__=='__main__':
    mode=sys.argv[1];ids=sys.argv[2].split(',');times=[float(x) for x in sys.argv[3:]]
    run(ids,mode,times)
