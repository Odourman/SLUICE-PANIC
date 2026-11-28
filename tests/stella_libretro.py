#!/usr/bin/env python3
"""Frame-exact execution of an actual libretro Stella core, not a CPU model."""
import argparse,ctypes as C,hashlib,json,os,pathlib,random,struct,time,wave,zlib
# Generic callback harness adapted from user's MELLANRUM libretro test.
COMMIT=os.environ.get("GITHUB_SHA","SOURCE_SHA_NOT_PROVIDED")
ROM_SHA=os.environ.get("SLUICE_ROM_SHA","HASH_NOT_PROVIDED")
class Info(C.Structure):
 _fields_=[("library_name",C.c_char_p),("library_version",C.c_char_p),("valid_extensions",C.c_char_p),("need_fullpath",C.c_bool),("block_extract",C.c_bool)]
class Geometry(C.Structure):
 _fields_=[("base_width",C.c_uint),("base_height",C.c_uint),("max_width",C.c_uint),("max_height",C.c_uint),("aspect_ratio",C.c_float)]
class Timing(C.Structure):
 _fields_=[("fps",C.c_double),("sample_rate",C.c_double)]
class AV(C.Structure):
 _fields_=[("geometry",Geometry),("timing",Timing)]
class Game(C.Structure):
 _fields_=[("path",C.c_char_p),("data",C.c_void_p),("size",C.c_size_t),("meta",C.c_char_p)]
class Descriptor(C.Structure):
 _fields_=[("port",C.c_uint),("device",C.c_uint),("index",C.c_uint),("id",C.c_uint),("description",C.c_char_p)]
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
POLL=C.CFUNCTYPE(None)
INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
def write_png(file,w,h,pitch,pixels,fmt):
 raw=bytearray()
 for y in range(h):
  raw.append(0);row=pixels[y*pitch:(y+1)*pitch]
  if fmt==1:raw.extend(b"".join(bytes((row[i+2],row[i+1],row[i])) for i in range(0,w*4,4)))
  else:
   for v in struct.unpack_from("<"+str(w)+"H",row):
    if fmt==2:r,g,b=((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31
    else:r,g,b=((v>>10)&31)*255//31,((v>>5)&31)*255//31,(v&31)*255//31
    raw.extend((r,g,b))
 def ck(k,v):return struct.pack(">I",len(v))+k+v+struct.pack(">I",zlib.crc32(k+v)&0xffffffff)
 pathlib.Path(file).write_bytes(b"\x89PNG\r\n\x1a\n"+ck(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+ck(b"IDAT",zlib.compress(raw,6))+ck(b"IEND",b""))
class Core:
 def __init__(self,so,rom,out,audio_frames):
  self.lib=C.CDLL(so);self.out=pathlib.Path(out);self.pixels=None;self.width=0;self.height=0;self.pitch=0;self.pixfmt=0
  self.pressed=set();self.desc=[];self.counters={"video":0,"audio_samples":0,"input_polls":0};self.frame=0;self.audio_frames=audio_frames
  for n,args,ret in [("retro_set_environment",[ENV],None),("retro_set_video_refresh",[VIDEO],None),("retro_set_audio_sample",[AUDIO],None),("retro_set_audio_sample_batch",[BATCH],None),("retro_set_input_poll",[POLL],None),("retro_set_input_state",[INPUT],None),("retro_init",[],None),("retro_deinit",[],None),("retro_get_system_info",[C.POINTER(Info)],None),("retro_get_system_av_info",[C.POINTER(AV)],None),("retro_load_game",[C.POINTER(Game)],C.c_bool),("retro_unload_game",[],None),("retro_run",[],None),("retro_set_controller_port_device",[C.c_uint,C.c_uint],None),("retro_get_memory_data",[C.c_uint],C.c_void_p),("retro_get_memory_size",[C.c_uint],C.c_size_t)]:
   f=getattr(self.lib,n);f.argtypes=args;f.restype=ret
  self.sd=C.create_string_buffer(os.fsencode(str(self.out.resolve())))
  @ENV
  def env(cmd,p):
   if cmd==10:self.pixfmt=C.cast(p,C.POINTER(C.c_int))[0];return True
   if cmd==3:C.cast(p,C.POINTER(C.c_bool))[0]=True;return True
   if cmd==11:
    d=C.cast(p,C.POINTER(Descriptor))
    for i in range(128):
     row=d[i]
     if not row.description:break
     self.desc.append({"port":row.port,"device":row.device,"id":row.id,"name":row.description.decode("utf-8","replace")})
    return True
   if cmd in (9,30,31):C.cast(p,C.POINTER(C.c_char_p))[0]=C.cast(self.sd,C.c_char_p);return True
   if cmd==39:C.cast(p,C.POINTER(C.c_uint))[0]=0;return True
   if cmd==17:C.cast(p,C.POINTER(C.c_bool))[0]=False;return True
   return False
  @VIDEO
  def video(ptr,w,h,pitch):
   self.counters["video"]+=1
   if ptr:self.width=w;self.height=h;self.pitch=pitch;self.pixels=C.string_at(ptr,pitch*h)
  @AUDIO
  def audio(l,r):
   self.counters["audio_samples"]+=1
   if self.wav and self.frame<self.audio_frames:self.wav.writeframesraw(struct.pack("<hh",l,r))
  @BATCH
  def batch(ptr,n):
   self.counters["audio_samples"]+=n
   if self.wav and self.frame<self.audio_frames:self.wav.writeframesraw(C.string_at(ptr,n*4))
   return n
  @POLL
  def poll():self.counters["input_polls"]+=1
  @INPUT
  def inp(port,device,index,id):return int(port==0 and device==1 and index==0 and id in self.pressed)
  self.refs=[env,video,audio,batch,poll,inp]
  self.lib.retro_set_environment(env);self.lib.retro_set_video_refresh(video);self.lib.retro_set_audio_sample(audio);self.lib.retro_set_audio_sample_batch(batch);self.lib.retro_set_input_poll(poll);self.lib.retro_set_input_state(inp)
  self.lib.retro_init();inf=Info();self.lib.retro_get_system_info(C.byref(inf))
  self.info={"name":inf.library_name.decode() if inf.library_name else "", "version":inf.library_version.decode() if inf.library_version else "","core_sha256":hashlib.sha256(pathlib.Path(so).read_bytes()).hexdigest(),"need_fullpath":bool(inf.need_fullpath)}
  self.lib.retro_set_controller_port_device(0,1)
  self.rombytes=pathlib.Path(rom).read_bytes();self.buf=C.create_string_buffer(self.rombytes);self.game=Game(os.fsencode(os.path.abspath(rom)),C.cast(self.buf,C.c_void_p),len(self.rombytes),None)
  if not self.lib.retro_load_game(C.byref(self.game)):raise RuntimeError("LIBRETRO_ROM_LOAD_FAILED")
  av=AV();self.lib.retro_get_system_av_info(C.byref(av))
  self.info.update({"fps":av.timing.fps,"sample_rate":av.timing.sample_rate,"geometry":[av.geometry.base_width,av.geometry.base_height],"pixel_format":self.pixfmt,"rom_sha256":hashlib.sha256(self.rombytes).hexdigest(),"reported_ram_bytes":self.lib.retro_get_memory_size(2)})
  self.wav=wave.open(str(self.out/"tia_audio.wav"),"wb") if audio_frames else None
  if self.wav:self.wav.setnchannels(2);self.wav.setsampwidth(2);self.wav.setframerate(round(av.timing.sample_rate))
 def memory(self):
  sz=self.lib.retro_get_memory_size(2);p=self.lib.retro_get_memory_data(2)
  return C.string_at(p,min(sz,8192)) if p and sz else None
 def run(self,buttons,frame):
  self.pressed=set(buttons);self.frame=frame;self.lib.retro_run()
 def snapshot(self,frame):
  if self.pixels is None:return None
  file=self.out/("frame_%07d.png"%frame);write_png(file,self.width,self.height,self.pitch,self.pixels,self.pixfmt);return file.name
 def close(self):
  if self.wav:self.wav.close()
  self.lib.retro_unload_game();self.lib.retro_deinit()
def mapping_for(desc):
 m={"Fire":0,"Select":2,"Reset":3,"Up":4,"Down":5,"Left":6,"Right":7}
 for d in desc:
  if d["port"]!=0 or d["device"]!=1:continue
  s=d["name"].lower().strip()
  for name in ["Fire","Select","Reset","Up","Down","Left","Right","Left Difficulty A","Left Difficulty B","Right Difficulty A","Right Difficulty B","Color","Black/White"]:
   if s==name.lower():m[name]=d["id"]
 return m

def main():
 p=argparse.ArgumentParser()
 for n in ("core","rom","sym","out"):p.add_argument("--"+n,required=True)
 p.add_argument('--stress-frames',type=int,default=3600)
 a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 sym={}
 for l in pathlib.Path(a.sym).read_text().splitlines():
  f=l.split()
  if len(f)>1:
   try:sym[f[0]]=int(f[1],16)
   except ValueError:pass
 c=Core(a.core,a.rom,out,900);m=mapping_for(c.desc)
 print("CORE",c.info,"INPUT",m,flush=True)
 from PIL import Image
 import subprocess
 video=None; seen=set(); samples=[]; events=[]; best=0; start=0; stop=a.stress_frames; died=False; restart=False; sessions=0; random_frames=0; classic_seen=False; expert_seen=False
 import random
 rng=random.Random(2600)
 def state():
  ram=c.memory();assert ram and len(ram)>=128, "RIOT RAM unavailable"
  def g(k,i=0):return ram[(sym[k]+i)&127]
  sc=sum(((g("score",i)>>4)*10+(g("score",i)&15))*100**i for i in range(3))
  return dict(variant=g("variant"),mode=g("mode"),lives=g("lives"),active=g("active"),keeper=g("keeper"),gates=g("gates"),level=g("level"),score=sc,kind=[g("kind",i) for i in range(4)],pos=[g("pos",i) for i in range(4)],fireHeld=g("fireHeld"),oldDir=g("oldDir"),bonus=g("bonusTimer"))
 def snap(tag,f):
  if tag in seen:return
  seen.add(tag);fn=c.snapshot(f)
  if fn:(out/fn).rename(out/(tag+".png"))
 for f in range(stop+3600):
  buttons=set()
  if f in (5,10):buttons={"Select"}
  elif f==15:buttons={"Fire"}
  elif f>20:
   s=state()
   if f<stop and s["mode"]!=1:
    if not s["fireHeld"]:buttons={"Fire"}
   elif f<stop and stop>20000 and f>=stop-10000:
    random_frames+=1
    if f%751==0:buttons={"Reset"}
    elif f%6==0:buttons={rng.choice(["Up","Down","Fire"])}
   elif f<stop and s["mode"]==1:
    candidates=[(s["pos"][j],j) for j in range(s["active"]) if s["kind"][j] in (1,2) and bool(s["gates"]&(1<<j))!=(s["kind"][j]==1)]
    if candidates:
     _,j=max(candidates);k=s["keeper"]
     if j==k and not s["fireHeld"]:buttons={"Fire"}
     elif j!=k:
      d=0x20 if j<k else 0x10
      if s["oldDir"]!=d:buttons={"Up" if j<k else "Down"}
   elif f>stop and s["mode"]==2 and not restart:
    died=True;buttons={"Fire"};restart=True
  before=state() if f else None
  c.run({m[x] for x in buttons},f)
  s=state();best=max(best,s["level"])
  assert 0<=s["keeper"]<s["active"]<=4 and 0<=s["lives"]<=3 and s["mode"] in (0,1,2) and all(k<=6 for k in s["kind"]),s
  if before and before["mode"]!=1 and s["mode"]==1:sessions+=1
  if before and before["mode"]==0 and before["variant"]==1:expert_seen=True;snap("expert_ready",f)
  if before and before["mode"]==0 and before["variant"]==0:classic_seen=True
  if before and before["mode"]==2 and restart:snap("game_over",f)
  if buttons:events.append([f,sorted(buttons)])
  if f==13:snap("ready",f)
  if s["mode"]==1:
   start+=1
   if f>40:snap("gameplay",f)
   if s["active"]==3:snap("three_lanes",f)
   if s["active"]==4:snap("four_lanes",f)
   if s["bonus"]:snap("bonus",f)
  if f%120==0:samples.append({"frame":f,**s})
  if f<900 and c.pixels:
   raw=c.pixels
   if c.pixfmt==1:im=Image.frombytes("RGB",(c.width,c.height),raw,"raw","BGRX",c.pitch,1)
   elif c.pixfmt==2:im=Image.frombytes("RGB",(c.width,c.height),raw,"raw","BGR;16",c.pitch,1)
   else:im=Image.frombytes("RGB",(c.width,c.height),raw,"raw","BGR;15",c.pitch,1)
   im=im.resize((640,480),Image.Resampling.NEAREST)
   if video is None:
    fps=50 if "PAL" in a.rom and "NTSC" not in a.rom else 60
    video=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","640x480","-r",str(fps),"-i","-","-an","-c:v","libx264","-pix_fmt","yuv420p",str(out/"silent.mp4")],stdin=subprocess.PIPE)
   video.stdin.write(im.tobytes())
  if restart and s["mode"]==1:
   f+=1;c.run(set(),f);s=state();snap("restart",f);break
  if f==stop-1:snap("late_gameplay",f)
 c.close()
 if video:
  video.stdin.close();assert video.wait()==0
  subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(out/"silent.mp4"),"-i",str(out/"tia_audio.wav"),"-c:v","copy","-c:a","aac","-shortest",str(out/"gameplay.mp4")],check=True)
  (out/"silent.mp4").unlink()
 with wave.open(str(out/"tia_audio.wav"),"rb") as w:
  pcm=w.readframes(w.getnframes());peak=max(abs(v[0]) for v in struct.iter_unpack("<h",pcm))
 result={"core":c.info,"frames":f+1,"video_callbacks":c.counters["video"],"audio_samples":c.counters["audio_samples"],"pcm_peak":peak,"max_level":best,"active_gameplay_frames":start,"game_over":died,"restart":restart and s["mode"]==1,"snapshots":sorted(seen),"last_state":s,"sessions":sessions,"random_gameplay_frames":random_frames,"classic_ready":classic_seen,"expert_ready":expert_seen}
 (out/"result.json").write_text(json.dumps(result,indent=2));(out/"samples.json").write_text(json.dumps(samples));(out/"inputs.json").write_text(json.dumps(events));print("RESULT",json.dumps(result),flush=True)
 assert start>100 and best>=3 and died and restart and s["mode"]==1 and peak>0 and classic_seen and expert_seen and c.counters["video"]==f+1 and f+1>=stop,result
if __name__=="__main__":main()
