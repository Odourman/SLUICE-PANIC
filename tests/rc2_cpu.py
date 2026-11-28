"""Execute actual DASM ROM bytes with py65, an approximate RIOT/WSYNC bus.
Not a TIA pixel, Stella, or hardware verification. RIOT floor countdown calibrated against native Stella raster observation. Direct RAM setups are explicit.
"""
import re, sys, random, json
from pathlib import Path
from py65.devices.mpu6502 import MPU
class Bus:
    def __init__(self, rom):
        self.rom=rom; self.bank=0; self.visited=set(); self.switches=0; self.ram=bytearray(128); self.tia=bytearray(64)
        self.c=0; self.timer=0; self.events=[]; self.frames=[]
        self.joy=255; self.fire=128; self.reset=255; self.visible_gaps=[]
        self.last_sync=None; self.last_visible=False; self.visible_cycles=[]; self.timer_usage=[]; self.timer_start=None; self.timer_wait=False
    def __getitem__(self,a):
        a &= 0x1fff
        if a&0x1000:
            if 0x1ff6<=a<=0x1ff9:
                self.bank=a-0x1ff6;self.visited.add(self.bank);self.switches+=1
            return self.rom[self.bank*4096+(a&4095)]
        if a&0x80:
            if not a&0x200: return self.ram[a&127]
            if a==0x280: return self.joy
            if a==0x282: return self.reset
            if a==0x284:
                if not self.timer_wait and self.timer_start is not None:
                    self.timer_usage.append(self.c-self.timer_start); self.timer_wait=True
                d=self.timer-self.c
                return (d//64 if d>=0 else d%256)&255
            return 0
        if a&15==12: return self.fire
        return 0
    def __setitem__(self,a,v):
        a&=0x1fff; v&=255
        if a&0x1000:
            if 0x1ff6<=a<=0x1ff9:
                self.bank=a-0x1ff6;self.visited.add(self.bank);self.switches+=1
            return
        if a&0x80:
            if not a&0x200: self.ram[a&127]=v
            elif a==0x296: self.events.append(("timer",v))
        else: self.events.append((a&63,v))
    def after(self,cycles):
        self.c+=cycles
        for a,v in self.events:
            if a=="timer":
                self.timer=self.c+v*64; self.timer_start=self.c; self.timer_wait=False
            else:
                if a==0 and v&2 and not self.tia[0]&2:
                    self.frames.append(self.c//76)
                if a==2:
                    visible=not self.tia[1]&2 and not self.tia[0]&2
                    before=self.c
                    self.c=(self.c//76+1)*76 if self.c%76 else self.c
                    if self.frames and visible and self.last_visible:
                        self.visible_gaps.append((self.c-self.last_sync)//76)
                        self.visible_cycles.append(before-self.last_sync)
                    self.last_visible=visible; self.last_sync=self.c
                self.tia[a]=v
        self.events.clear()
class Machine:
    def __init__(self,tv,bank=0):
        self.tv=tv
        self.syms={m[1]:int(m[2],16) for l in Path(f"build/{tv}.sym").read_text().splitlines() if (m:=re.match(r"^\s*(\S+)\s+([0-9a-fA-F]{4})\b",l))}
        self.bus=Bus(Path(f"build/SLUICE_PANIC_{tv}.bin").read_bytes())
        self.bus.bank=bank
        self.cpu=MPU(memory=self.bus,pc=None)
        self.minsp=255
        self.frame()
    def get(self,k,i=0): return self.bus.ram[(self.syms[k]+i)&127]
    def set(self,k,v,i=0): self.bus.ram[(self.syms[k]+i)&127]=v
    def frame(self,joy=255,fire=False,reset=False,select=False):
        self.bus.joy=joy; self.bus.fire=0 if fire else 128; self.bus.reset=255-(1 if reset else 0)-(2 if select else 0)
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
    for b in range(4):
        boot=Machine(tv,b);boot.ticks(2)
        assert boot.get('mode')==0 and boot.get('lives')==3 and boot.bus.bank==1,(tv,b)
    def ok(name,cond):
        assert cond,(tv,name,m.score(),m.get("lives"),m.get("mode"))
        checks.append(name)
    m.ticks(3)
    ok("all four startup banks",True)
    ok("power-on ready",m.get("mode")==0 and m.get("lives")==3 and m.score()==0)
    e=Machine(tv);e.ticks(3)
    e.frame(select=True)
    ok("SELECT chooses expert",e.get("variant")==1 and e.get("mode")==0 and e.get("active")==4)
    e.ticks(3,select=True)
    ok("SELECT edge only",e.get("variant")==1)
    e.frame();e.frame(fire=True)
    ok("expert starts level seven",e.get("mode")==1 and e.get("level")==7 and e.get("speed")==2)
    e.setup(1,1,123400);e.frame()
    ok("session best",e.score()==123500 and [e.get("sessionBest",i) for i in range(3)]==[0,0x35,0x12])
    e.frame(reset=True)
    ok("session best persists reset",e.score()==0 and e.get("sessionBest",2)==0x12 and e.get("variant")==1)
    e.setup(1,1,0,lives=2);e.set("level",4);e.set("roundN",1);e.frame()
    ok("clean fourth-round extra life",e.get("lives")==3 and e.score()==600)
    e.setup(1,1,0);e.clear();e.set("active",4);e.set("spawnGap",0)
    for j in range(4):e.set("delay",0,j)
    e.frame()
    ok("staggered simultaneous spawn",sum(bool(e.get("kind",j)) for j in range(4))==1)
    e.ticks(5)
    ok("spawn cooldown",sum(bool(e.get("kind",j)) for j in range(4))==1)
    for b in range(4):
        assert len(e.bus.rom[b*4096:(b+1)*4096])==4096
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
        assert all(m.get("kind",j)<=6 for j in range(4))
        assert 0<=m.score()<=999999
    # Autonomous score-chase, reading live RAM only to choose joystick input.
    m.frame(); m.frame(reset=True); m.frame()
    for _ in range(7200):
        candidates=[(m.get("pos",j),j) for j in range(m.get("active")) if m.get("kind",j) in (1,2) and bool(m.get("gates")&(1<<j)) != (m.get("kind",j)==1)]
        joy=255; fire=False
        if candidates:
            _,j=max(candidates); current=m.get("keeper")
            if j==current: fire=not m.get("fireHeld")
            else:
                desired=0x20 if j<current else 0x10
                if m.get("oldDir")!=desired: joy=0xef if j<current else 0xdf
        m.frame(joy=joy,fire=fire)
    print(tv,"AUTOPLAY",m.score(),m.get("level"),m.get("lives"),m.get("active"),flush=True)
    ok("autoplay four lanes",m.get("active")==4 and m.get("level")>=5 and m.get("lives")==3)
    ok("autoplay points",m.score()>5000)
    # Explicitly test simultaneous directed results, all 16 masks, high speed and all digits.
    for mask in range(16):
        m.setup(1,mask,123456)
        m.clear(); m.set("active",4); m.set("keeper",mask%4)
        for j in range(4):
            m.set("kind",1 if mask&(1<<j) else 2,j); m.set("pos",110,j)
        m.set("level",12); m.set("speed",2); m.frame()
        expected_score=123456+sum(100 if mask&(1<<j) else 25 for j in range(4))
        ok(f"four simultaneous outcomes mask={mask}",m.score()==expected_score and m.get("lives")==3)
    expected=262 if tv=="NTSC" else 312
    gaps=[b-a for a,b in zip(m.bus.frames,m.bus.frames[1:])]
    hist={x:gaps.count(x) for x in sorted(set(gaps))}
    print(tv,"checks",checks,"frame histogram",hist,"visible WSYNC gaps",sorted(set(m.bus.visible_gaps)),"minSP",hex(m.minsp), "ramEnd",hex(m.syms["ramEnd"]),"visible max cycles",max(m.bus.visible_cycles),"timer logic max",max(m.bus.timer_usage),flush=True)
    ok("all four F6 banks exercised",m.bus.visited=={0,1,2,3})
    ok("frame model",set(gaps)=={expected})
    ok("visible WSYNC model",max(m.bus.visible_gaps)==1)
    ok("stack model",m.minsp>=m.syms["ramEnd"])
    return {"format":tv,"checks":checks,"frames":hist,"stack_min":m.minsp,"ram_end":m.syms["ramEnd"],"visible_max_cycles":max(m.bus.visible_cycles),"timer_logic_max":max(m.bus.timer_usage),"bank_switches":m.bus.switches,"scope":"actual F6 ROM CPU/approximate RIOT bus; not TIA"}
result=[check(tv) for tv in ("NTSC","PAL")]
Path("build/cpu-tests.json").write_text(json.dumps(result,indent=2))
