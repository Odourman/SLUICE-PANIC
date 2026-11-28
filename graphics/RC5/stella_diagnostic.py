#!/usr/bin/env python3
import pathlib,sys,json,subprocess,hashlib
sys.path.insert(0,str(pathlib.Path('tests').resolve()))
from stella_libretro import Core,mapping_for
from PIL import Image
root=pathlib.Path('rc5-graphics-output')
for tv in ('NTSC','PAL'):
 out=root/'emulator'/tv;out.mkdir(parents=True,exist_ok=True)
 c=Core('/tmp/stella-core/stella_libretro.so',str(root/'build'/f'SLUICE_RC5_GRAPHICS_DIAGNOSTIC_{tv}.bin'),out,0)
 m=mapping_for(c.desc);samples=[];snaps=set();vid=None
 for f in range(1060):
  c.run({m['Fire']} if f==1020 else set(),f)
  ram=c.memory()
  stage=ram[1] if ram and len(ram)>=128 else -1
  tick=ram[0] if ram and len(ram)>=128 else -1
  if f%16==0:samples.append([f,stage,tick])
  if c.pixels:
   if (stage,tick//32) not in snaps:
    snaps.add((stage,tick//32));p=c.snapshot(f)
    (out/p).rename(out/f'stage_{stage}_tick_{tick:03d}.png')
   if f%4==0:
    fmt='BGRX' if c.pixfmt==1 else 'BGR;16' if c.pixfmt==2 else 'BGR;15'
    im=Image.frombytes('RGB',(c.width,c.height),c.pixels,'raw',fmt,c.pitch,1).resize((320,240),Image.Resampling.NEAREST)
    if vid is None:vid=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','320x240','-r','15' if tv=='NTSC' else '12.5','-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p',str(out/'diagnostic.mp4')],stdin=subprocess.PIPE)
    vid.stdin.write(im.tobytes())
 if vid:vid.stdin.close();assert vid.wait()==0
 report={'core':c.info,'callbacks':c.counters,'samples':samples,'stage_snapshots':sorted(snaps),'limitations':'Actual Stella libretro snapshots, not independent verification; video subsampled every fourth frame and rescaled.'}
 c.close();(out/'result.json').write_text(json.dumps(report,indent=2));print(tv,report['core'],report['callbacks'],flush=True)
 assert report['callbacks']['video']==1060 and len({i[0] for i in snaps})>=8,report
