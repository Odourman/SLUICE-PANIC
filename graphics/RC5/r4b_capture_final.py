import sys,pathlib,json,hashlib,struct,os
sys.path.insert(0,str(pathlib.Path('tests').resolve()))
from stella_libretro import Core,mapping_for
from PIL import Image,ImageStat
tv=sys.argv[1]; root=pathlib.Path(sys.argv[2]); out=root/'emulator'/tv;out.mkdir(parents=True,exist_ok=True)
c=Core('/tmp/stella-core/stella_libretro.so',str(root/'build'/f'SLUICE_RC5_GRAPHICS_DIAGNOSTIC_{tv}.bin'),out,0)
m=mapping_for(c.desc); samples=[];seen=set();frames=[]; prev=None
for f in range(4200):
 c.run({m['Fire']} if f in (1020,2040,3060) else set(),f)
 ram=c.memory();stage,tick,mode=ram[1],ram[0],ram[13]
 if c.pixels and f>3:
  fmt='BGRX' if c.pixfmt==1 else 'BGR;16' if c.pixfmt==2 else 'BGR;15'
  im=Image.frombytes('RGB',(c.width,c.height),c.pixels,'raw',fmt,c.pitch,1)
  key=(stage,tick//8,mode)
  if key not in seen:
   seen.add(key); im.save(out/f's{stage}_t{tick:03d}_m{mode}.png')
   samples.append({'frame':f,'stage':stage,'tick':tick,'mode':mode,'width':c.width,'height':c.height,'pitch':c.pitch,'pixel_format':c.pixfmt,'colors':len(im.getcolors(100000) or []),'mean':ImageStat.Stat(im).mean,'raw_sha256':hashlib.sha256(c.pixels).hexdigest(),'audio_samples':c.counters['audio_samples']})
  if f%4==0 and f<1180:frames.append(im.resize((320,240),Image.Resampling.NEAREST))
if frames:frames[0].save(out/'diagnostic.gif',save_all=True,append_images=frames[1:],duration=67 if tv=='NTSC' else 80,loop=0)
# Compare independent PNG conversion against original manual writer at identical raw buffer.
from stella_libretro import write_png
write_png(out/'manual_final.png',c.width,c.height,c.pitch,c.pixels,c.pixfmt)
im.save(out/'pillow_final.png')
assert Image.open(out/'manual_final.png').convert('RGB').tobytes()==im.tobytes()
r={'core':c.info,'callbacks':c.counters,'samples':samples,'pid':os.getpid(),'manual_vs_pillow_equal':True}; c.close();(out/'result.json').write_text(json.dumps(r,indent=2))
print(tv,r['core'],r['callbacks'],flush=True)
assert r['callbacks']['video']==4200 and len({x['stage'] for x in samples})==8
