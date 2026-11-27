"""Execute actual DASM ROM bytes with py65, an approximate RIOT/WSYNC bus.
Not a TIA pixel, Stella, or hardware verification. Direct RAM setups are explicit.
"""
import re, sys, random, json
from pathlib import Path
from py65.devices.mpu6502 import MPU
class Bus:
    def __init__(self, rom):
        self.rom=rom; self.ram=bytearray(128); self.tia=bytearray(64)
        self.c=0; self.timer=0; self.events=[]; self.frames=[]
        self.joy=255; self.fire=128; self.reset=255; self.visible_gaps=[]
        self.last_sync=None; self.last_visible=False
    def __getitem__(self,a):
        a &= 0x1fff
        if a&0x1000: return self.rom[a&4095]
        if a&0x80:
            if not a&0x200: return self.ram[a&127]
            if a==0x280: return self.joy
            if a==0x282: return self.reset
            if a==0x284:
                d=self.timer-self.c
                return (d//64 if d>=0 else d%256)&255
            return 0
        if a&15==12: return self.fire
        return 0
    def __setitem__(self,a,v):
        a&=0x1fff; v&=255
        if a&0x1000: return
        if a&0x80:
            if not a&0x200: self.ram[a&127]=v
            elif a==0x296: self.events.append(("timer",v))
        else: self.events.append((a&63,v))
    def after(self,cycles):
        self.c+=cycles
        for a,v in self.events:
            if a=="timer": self.timer=self.c+v*64
            else:
                if a==0 and v&2 and not self.tia[0]&2:
                    self.frames.append(self.c//76)
                if a==2:
                    visible=not self.tia[1]&2 and not self.tia[0]&2
                    self.c=(self.c//76+1)*76 if self.c%76 else self.c
                    if visible and self.last_visible:
                        self.visible_gaps.append((self.c-self.last_sync)//76)
                    self.last_visible=visible; self.last_sync=self.c
                self.tia[a]=v
        self.events.clear()
class Machine:
    def __init__(self,tv):
        self.tv=tv
        self.syms={m[1]:int(m[2],16) for l in Path(f"build/{tv}.sym").read_text().splitlines() if (m:=re.match(r"^\s*(\S+)\s+([0-9a-fA-F]{4})\b",l))}
        self.bus=Bus(Path(f"build/SLUICE_PANIC_{tv}.bin").read_bytes())
        self.cpu=MPU(memory=self.bus,pc=None)
        self.minsp=255
        self.frame()
    def get(self,k,i=0): return self.bus.ram[(self.syms[k]+i)&127]
    def set(self,k,v,i=0): self.bus.ram[(self.syms[k]+i)&127]=v
    def frame(self,joy=255,fire=False,reset=False):
        self.bus.joy=joy; self.bus.fire=0 if fire else 128; self.bus.reset=254 if reset else 255
        n=len(self.bus.frames)
        for _ in range(20000):
            old=self.cpu.processorCycles
            self.cpu.step()
            self.bus.after(self.cpu.processorCycles-old)
            # Ignore initial power-on SP before TXS.
            if n: self.minsp=min(self.minsp,self.cpu.sp)
            if len(self.bus.frames)>n: return
        raise AssertionError(("frame timeout",self.tv,hex(self.cpu.pc)))
    def ticks(self,n=1,**kw):
        for _ in range(n): self.frame(**kw)
    def score(self):
        return sum(((self.get("score",i)>>4)*10+(self.get("score",i)&15))*100**i for i in range(3))
    def clear(self):
        for i in range(4):
            self.set("kind",0,i); self.set("delay",200,i); self.set("pos",8,i)
    def setup(self,kind,gate,score=None,lives=3):
        self.clear()
        for k,v in dict(mode=1,gates=gate,lives=lives,phase=0,roundN=8,dirty=0,active=2,level=1,speed=1,keeper=0).items(): self.set(k,v)
        self.set("kind",kind,0); self.set("pos",111,0)
        if score is not None:
            for i in range(3):
                n=score//100**i%100; self.set("score",(n//10)*16+n%10,i)
def check(tv):
    m=Machine(tv); checks=[]
    def ok(name,cond):
        assert cond,(tv,name,m.score(),m.get("lives"),m.get("mode"))
        checks.append(name)
    m.ticks(3)
    ok("power-on ready",m.get("mode")==0 and m.get("lives")==3 and m.score()==0)
    m.frame(fire=True); ok("fire starts",m.get("mode")==1)
    m.ticks(4,fire=True); ok("held start does not toggle",m.get("gates")==0)
    m.frame(); m.frame(fire=True); ok("toggle once",m.get("gates")==1)
    m.ticks(4,fire=True); ok("held fire",m.get("gates")==1)
    m.frame(); m.frame(joy=0xdf); ok("down",m.get("keeper")==1)
    m.ticks(20,joy=0xdf); ok("inactive lane cannot select",m.get("keeper")==1)
    m.frame(); m.frame(joy=0xef); ok("up",m.get("keeper")==0)
    m.frame()
    for kind,gate,points,remaining in [(1,1,100,3),(2,0,25,3),(1,0,0,2),(2,1,0,2)]:
        m.setup(kind,gate,0); m.frame()
        ok(f"collision {kind}/{gate}",m.score()==points and m.get("lives")==remaining)
        m.ticks(8); ok(f"no duplicate {kind}/{gate}",m.score()==points and m.get("lives")==remaining)
    m.setup(1,1,999950); m.frame(); ok("score saturation",m.score()==999999)
    m.setup(1,1,0); m.set("roundN",1); m.frame()
    ok("round bonus and third lane",m.score()==600 and m.get("active")==3 and m.get("level")==2)
    m.setup(2,0,0); m.set("roundN",1); m.set("dirty",1); m.set("active",3); m.set("level",2); m.frame()
    ok("dirty round and fourth lane",m.score()==25 and m.get("active")==4 and m.get("level")==3)
    m.setup(1,0,250,lives=1); m.frame(); ok("game over",m.get("mode")==2 and m.get("lives")==0 and m.score()==250)
    m.frame(fire=True); ok("restart",m.get("mode")==1 and m.score()==0 and m.get("lives")==3)
    m.frame(); m.frame(reset=True); ok("console reset",m.get("mode")==1 and m.score()==0)
    # Unmodified game, adversarial inputs.
    rng=random.Random(2600)
    for i in range(1200):
        m.frame(joy=rng.choice([255,0xef,0xdf,0xcf]),fire=rng.randrange(5)==0,reset=i%301==0)
        assert 0<=m.get("keeper")<m.get("active")<=4 and m.get("lives")<=3
        assert all(m.get("kind",j)<=4 for j in range(4))
        assert 0<=m.score()<=999999
    expected=262 if tv=="NTSC" else 312
    gaps=[b-a for a,b in zip(m.bus.frames,m.bus.frames[1:])]
    hist={x:gaps.count(x) for x in sorted(set(gaps))}
    print(tv,"checks",checks,"frame histogram",hist,"visible WSYNC gaps",sorted(set(m.bus.visible_gaps)),"minSP",hex(m.minsp), "ramEnd",hex(m.syms["ramEnd"]),flush=True)
    ok("frame model",set(gaps)=={expected})
    ok("visible WSYNC model",max(m.bus.visible_gaps)==1)
    ok("stack model",m.minsp>=m.syms["ramEnd"])
    return {"format":tv,"checks":checks,"frames":hist,"stack_min":m.minsp,"ram_end":m.syms["ramEnd"],"scope":"actual ROM CPU/approximate RIOT bus; not TIA"}
result=[check(tv) for tv in ("NTSC","PAL")]
Path("build/cpu-tests.json").write_text(json.dumps(result,indent=2))
