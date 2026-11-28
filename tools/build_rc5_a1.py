"""RC5-A1: deliberately data-only integration of accepted R4B into RC4.
Run from repository root: python tools/build_rc5_a1.py build
The canonical RC4 generator and V1 assets remain unchanged.
"""
from pathlib import Path
import re, sys
source=Path("tools/build_rc2.py").read_text()
marker='out=Path(sys.argv[1] if len(sys.argv)>1 else "build")'
assert source.count(marker)==1
patch=r'''
# RC5-A1: use R4B rows at existing addresses, avoiding kernel/code/RAM changes.
rows={
 "keeper_idle":"3C,7E,1C,1C,3E,7F,3E,1C,14,36",
 "keeper_operate":"3C,7E,1C,1C,1E,1F,3E,1C,14,36",
 "keeper_error":"3C,7E,1C,5D,3E,1C,1C,14,22,41",
 "cargo":"00,00,10,BC,7D,7F,BC,80,00,00",
 "debris":"00,04,08,3C,7E,7E,7E,3C,00,00",
 "cargo_hit":"00,18,5A,3C,7E,FF,7E,3C,5A,18",
 "debris_hit":"42,24,99,5A,24,24,5A,99,24,42",
 "CargoAlt":"00,00,10,3C,BD,7F,3C,40,00,00",
 "DebrisAlt":"00,06,08,3C,7E,7E,7E,3C,00,00",
}
def asmrow(s):return ",".join("$"+v for v in s.split(","))
v1=Path("graphics/V1/asm/graphics_data.inc").read_text()
for name in list(rows)[:7]:
    v1,n=re.subn(r"(?m)^"+name+r":\s*\n    \.byte [^\n]+",name+":\n    .byte "+asmrow(rows[name]),v1)
    assert n==1,name
old='    include "graphics/V1/asm/graphics_data.inc"'
assert display.count(old)==1
display=display.replace(old,v1.rstrip())
for name in ("CargoAlt","DebrisAlt"):
    display,n=re.subn(r"(?m)^"+name+r": \.byte [^\n]+",name+": .byte "+asmrow(rows[name]),display)
    assert n==1,name
old="ObjColor: .byte 0,COLOR_CARGO,COLOR_DEBRIS,COLOR_CARGO,COLOR_DEBRIS,COLOR_CARGO,COLOR_DEBRIS"
assert display.count(old)==1
# moving/passed bombs black; existing hit sprites retain conspicuous colors.
display=display.replace(old,"ObjColor: .byte 0,COLOR_CARGO,0,COLOR_CARGO,COLOR_DEBRIS,COLOR_CARGO,0")
for old,new in (("$B2,$B4,$D2,$D4","$B4,$B6,$D4,$D6"),("$82,$84,$A2,$A4","$84,$86,$A4,$A6")):
    assert hud.count(old)==pres.count(old)==1
    hud=hud.replace(old,new)
    pres=pres.replace(old,new)
'''
exec(compile(source.replace(marker,patch+"\n"+marker),"tools/build_rc2.py+RC5-A1","exec"))
