import subprocess,sys
V='/home/claude/psyched-mind-pipeline/assets/voice/2026-11-28-longvoice2/'
ns=[int(x) for x in sys.argv[2:]];out=sys.argv[1]
open('vlist.txt','w').write(''.join(f"file 'scene_{n:02d}.mp4'\n" for n in ns))
# audio: each chapter + 0.4 s silence, 48 kHz stereo, loudness later
parts=[];fc=''
for i,n in enumerate(ns):
    parts+=['-i',V+f'ch{n:02d}.mp3']
fc=''.join(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad=pad_dur=0.4[a{i}];' for i in range(len(ns)))+''.join(f'[a{i}]' for i in range(len(ns)))+f'concat=n={len(ns)}:v=0:a=1[v];['+str(len(ns))+':a]aresample=48000,aformat=channel_layouts=stereo,volume=0.6[s];[v][s]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]'
subprocess.check_call(['python3','sfx_long.py']+[str(n) for n in ns]);parts+=['-i','sfx_track.wav']
subprocess.check_call(['ffmpeg','-y','-loglevel','error']+parts+['-filter_complex',fc,'-map','[a]','-ar','48000','audio_tmp.wav'])
subprocess.check_call(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','vlist.txt','-i','audio_tmp.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out])
print(out)
