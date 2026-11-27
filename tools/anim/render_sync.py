import base64,subprocess,os,json
from playwright.sync_api import sync_playwright
V='/home/claude/psyched-mind-pipeline/assets/voice/2026-11-27-voice/'
jobs0={'V1':('p02_lost_ticket','psyched_lost_ticket_funny.mp4'),'V2':('n04_free_chocolate','psyched_free_chocolate_funny.mp4')}
import sys
jobs={k:v for k,v in jobs0.items() if k in sys.argv[1:]}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/anim/anim.html')
    for v,(vid,name) in jobs.items():
        words=json.load(open(V+vid+'.words.json'))
        adur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',V+vid+'.mp3']))
        dur=round(adur+0.25,2)
        pg.evaluate(f"setupSync('{v}',{json.dumps(words)},{adur})")
        if 'talk' in sys.argv:
         import numpy as np
         raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',V+vid+'.mp3','-ac','1','-ar','24000','-f','s16le','-'])
         a=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
         hop=800;env=[float(np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2))) if i*hop<len(a) else 0 for i in range(int(dur*30)+2)]
         mx=np.percentile([e for e in env if e>0] or [1],95);env=[min(1,e/mx) for e in env]
         sm=[];p=0
         for e in env: p=e if e>p else p*0.55+e*0.45; sm.append(round(p if p>0.12 else 0,3))
         pg.evaluate(f"SYNC.env={json.dumps(sm)}")
        n=int(dur*30);tmp='tmp_'+name
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',V+vid+'.mp3',
          '-filter_complex','[1:a]apad,atrim=0:%s[a]'%dur,'-map','0:v','-map','[a]','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',tmp],stdin=subprocess.PIPE)
        for i in range(n):
            d=pg.evaluate(f"grabSync('{v}',{i/30})");ff.stdin.write(base64.b64decode(d.split(',')[1]))
        ff.stdin.close()
        if ff.wait()==0: os.rename(tmp,name); print(name,n,dur)
