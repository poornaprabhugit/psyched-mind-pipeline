import base64,subprocess,os,json,sys
from playwright.sync_api import sync_playwright
V='/home/claude/psyched-mind-pipeline/assets/voice/2026-11-28-longvoice2/'
GAP=0.4
def adur(n): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',V+f'ch{n:02d}.mp3']))
def page(p):
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page(viewport={'width':1920,'height':1080})
    msgs=[];pg.on('console',lambda m:msgs.append(m.text));pg.on('pageerror',lambda e:msgs.append('ERR '+str(e)))
    pg.goto('file:///home/claude/anim/long.html');return pg,msgs
def setup(pg,n):
    w=json.load(open(V+f'ch{n:02d}.words.json'));d=round(adur(n)+GAP,3)
    pg.evaluate(f"setChapter({n},{json.dumps(w)},{d})");return d
mode=sys.argv[1] if __name__=="__main__" else ""
if __name__=='__main__':
 with sync_playwright() as p:
     pg,msgs=page(p)
     if mode=='shots':
         n=int(sys.argv[2]);d=setup(pg,n)
         ts=[float(x) for x in sys.argv[3:]]
         for t in ts:
             data=pg.evaluate(f"frame({t})");open(f'L{n}_{t}.jpg','wb').write(base64.b64decode(data.split(',')[1]))
         print('dur',d);print('\n'.join(sorted(set(msgs))))
     elif mode=='render':
         for n in [int(x) for x in sys.argv[2:]]:
             d=setup(pg,n);N=int(round(d*30));name=f'scene_{n:02d}.mp4';tmp='tmp_'+name
             ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',
               '-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30',tmp],stdin=subprocess.PIPE)
             for i in range(N):
                 data=pg.evaluate(f"frame({i/30})");ff.stdin.write(base64.b64decode(data.split(',')[1]))
             ff.stdin.close()
             if ff.wait()==0: os.rename(tmp,name);print(name,N,d,flush=True)
         print('\n'.join(sorted(set(m for m in msgs if 'MISSING' in m or 'ERR' in m))))
