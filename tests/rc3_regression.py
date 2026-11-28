"""Native Stella RC2/RC3 witness replay. Forced fixtures separated."""
import sys,pathlib,json,ctypes as C
from stella_libretro import Core,mapping_for
so=sys.argv[1];root=pathlib.Path(sys.argv[2]);results={}
def run(tv,version,romdir):
 out=root/'rc3-regression'/tv/version;out.mkdir(parents=True,exist_ok=True)
 syms={}
 for l in (romdir/(tv+'.sym')).read_text().splitlines():
  f=l.split()
  if len(f)>1:
   try:syms[f[0]]=int(f[1],16)&127
   except ValueError:pass
 rom=romdir/('SLUICE_PANIC_'+tv+'.bin');rows=[]
 def trial(name,policy,done,check):
  d=out/name;d.mkdir(exist_ok=True);c=Core(so,str(rom),d,600);m=mapping_for(c.desc);trace=[]
  for f in range(3000):
   keys=policy(f,trace);c.run({m[x] for x in keys},f);r=c.memory();assert len(r)==128
   v={k:r[syms[k]] for k in ['mode','variant','selectHeld','resetHeld','fireHeld','level','lives','gates','keeper','roundN']}
   trace.append([f,sorted(keys),v])
   if v['mode']==2 and (f==0 or trace[-2][2]['mode']!=2):c.snapshot(f)
   if done(f,trace):break
  c.snapshot(f);c.close();(d/'trace.json').write_text(json.dumps(trace,separators=(',',':')))
  rows.append(dict(name=name,passed=bool(check(f,trace)),frames=len(trace),last=trace[-1],core=c.info,callbacks=c.counters))
 for held in (False,True):
  def p(f,t):
   keys={'Select'} if f==4 or held and 4<=f<=8 else set()
   if f==8:keys.add('Fire')
   if t and t[-1][2]['mode']==2:keys={'Select'}
   return keys
  def done(f,t):return f>0 and t[-2][2]['mode']==2 and 'Select' in t[-1][1]
  def check(f,t):return done(f,t) and t[8][2]['mode']==1 and t[8][2]['variant']==1 and (t[-1][2]['mode'],t[-1][2]['variant'])==((2,1) if version=='RC2' and held else (0,0))
  trial('pachinko_held_'+str(held),p,done,check)
 if version=='RC3':
  def fixed(name,inputs,expected):
   trial(name,lambda f,t:set(inputs.get(f,[])),lambda f,t:f>=max(expected),lambda f,t:all(all(t[i][2][k]==v for k,v in exp.items()) for i,exp in expected.items()))
  fixed('ready_repeat_hold',{4:['Select'],5:['Select'],6:['Select'],8:['Select'],10:['Select','Fire'],11:['Select','Fire'],12:['Select'],14:['Select'],15:['Select'],17:['Fire']},{4:{'variant':1,'mode':0},6:{'variant':1},8:{'variant':0},10:{'variant':1,'mode':1},12:{'selectHeld':1,'gates':0},13:{'selectHeld':0},14:{'variant':1,'selectHeld':1},16:{'selectHeld':0},17:{'gates':1}})
  fixed('reset_priority',{4:['Select','Reset','Fire'],5:['Select','Reset','Fire'],6:['Select','Fire'],8:['Reset'],9:['Reset'],10:['Fire']},{4:{'mode':1,'variant':0,'selectHeld':1,'fireHeld':1,'gates':0},6:{'variant':0,'gates':0},7:{'selectHeld':0,'fireHeld':0},8:{'mode':1,'gates':0},10:{'gates':1}})
  for expert in (False,True):
   def dead(t):return next((i for i,_,s in t if s['mode']==2),None)
   def p(f,t):
    if f==4 and expert:return {'Select'}
    if f==8:return {'Fire'}
    if f<12:return set()
    d=dead(t)
    return {'Select'} if d is None or f<=d+2 or f==d+4 else set()
   def done(f,t):
    d=dead(t);return d is not None and f>=d+4
   def check(f,t):
    d=dead(t)
    return done(f,t) and all(t[j][2]['variant']==int(expert) for j in range(8,d+4)) and t[d+2][2]['mode']==2 and t[d+3][2]['selectHeld']==0 and t[d+4][2]['mode']==0 and t[d+4][2]['variant']==1-int(expert)
   trial('held_across_death_'+str(expert),p,done,check)
  d=out/'FORCED_DIAGNOSTIC';d.mkdir(exist_ok=True);c=Core(so,str(rom),d,0);m=mapping_for(c.desc)
  c.run(set(),0);c.run({m['Fire']},1);c.run(set(),2)
  r=(C.c_uint8*128).from_address(c.lib.retro_get_memory_data(2))
  def put(k,v):
   if isinstance(v,int):v=[v]
   for i,x in enumerate(v):r[syms[k]+i]=x
  def get(k):return r[syms[k]]
  def bcd(n):return [((n//100**i//10)%10)*16+(n//100**i)%10 for i in range(3)]
  def score():return sum(((r[syms['score']+i]>>4)*10+(r[syms['score']+i]&15))*100**i for i in range(3))
  cases=[]
  def fixture(name,mask,kinds,level=7,lives=3,points=0,roundN=8,dirty=0,expect=None):
   for k,v in dict(mode=1,variant=1,active=4,keeper=0,gates=mask,lives=lives,level=level,roundN=roundN,dirty=dirty,fireHeld=0,selectHeld=0,resetHeld=0,oldDir=0,phase=0,score=bcd(points),sessionBest=bcd(points),kind=kinds,pos=[110]*4,delay=[0,100,100,100],speed=2,spawnGap=100).items():put(k,v)
   c.run(set(),3+len(cases));actual=[score(),get('lives'),get('level'),get('roundN'),get('mode')]
   cases.append(dict(name=name,expected=expect,actual=actual,passed=actual==expect))
  for mask in range(16):
   for types in range(16):
    kinds=[1 if types>>j&1 else 2 for j in range(4)];s=0;lives=3;n=8
    for j,k in enumerate(kinds):
     n-=1
     if bool(mask>>j&1)!=(k==1):lives-=1;break
     s+=100 if k==1 else 25
    fixture(f'{mask}/{types}',mask,kinds,expect=[s,lives,7,n,1])
  for name,level,lives,points,n,dirty,good,exp in [('score_saturation',7,3,999950,8,0,1,[999999,3,7,7,1]),('bonus_life',8,2,1000,1,0,1,[1600,3,9,8,1]),('life_cap',8,3,1000,1,0,1,[1600,3,9,8,1]),('dirty_round',8,2,1000,1,1,1,[1100,2,9,8,1]),('last_life',8,1,1000,1,0,0,[1000,0,9,8,2]),('level_cap',255,3,999950,1,0,1,[999999,3,255,8,1])]:
   fixture(name,good,[1,0,0,0],level,lives,points,n,dirty,exp)
  c.close();(d/'matrix.json').write_text(json.dumps(cases,indent=2))
  rows.append(dict(name='forced_matrix_and_boundaries',passed=all(x['passed'] for x in cases),cases=len(cases),case_pass=sum(x['passed'] for x in cases),core=c.info,callbacks=c.counters))
 (out/'result.json').write_text(json.dumps(rows,indent=2))
 return rows
for tv in ('NTSC','PAL'):
 for v,p in [('RC2',root/'rc2-baseline'),('RC3',root)]:
  results[tv+'/'+v]=run(tv,v,p)
(root/'rc3-regression'/'summary.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2));assert all(x['passed'] for rows in results.values() for x in rows)
