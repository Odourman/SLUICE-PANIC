"""RC2 source generator: preserve frozen src/main.asm, extract and specialize four banks."""
from pathlib import Path
import sys,subprocess,hashlib,json
a=Path("src/main.asm").read_text()
def section(s,e):return a[a.index("\n"+s+":")+1:a.index("\n"+e+":")+1]
head=a[:a.index("Reset:")].replace("ramEnd  ds 0","spawnGap ds 1\nobjectPtr ds 4\nthemeWater ds 1\nhudValid ds 1\nhudMode ds 1\nhudLives ds 1\nhudScore ds 3\naudioTmp ds 1\nvariant ds 1\nselectHeld ds 1\nsessionBest ds 3\nramEnd ds 0")
stub="""
    IF * > $FFC0
    ERR
    ENDIF
    ORG $FFC0
F6Boot:
    bit $FFF6
    jmp $F000
F6HUD:
    bit $FFF8
    jsr $F000
    bit $FFF7
    rts
F6Logic:
    bit $FFF6
    jsr $F100
    bit $FFF7
    rts
F6Start:
    bit $FFF7
    jmp $F01F
F6Presentation:
    bit $FFF9
    jsr $F000
    bit $FFF8
    rts
    ORG $FFF6
    .byte 0,0,0,0
    .word F6Boot,F6Boot,F6Boot
"""
engine=section("Reset","Frame")+"    jmp F6Start\n"+section("NewGame","Update").replace("    sta dirty\n","    sta dirty\n    sta spawnGap\n    sta hudValid\n")
engine+="    IF * > $F100\n    ERR\n    ENDIF\n    ORG $F100\n"+section("Update","PrepareHUD")
engine=engine.replace("    dec snd1\n    bne PoseTick\n    lda #0","""    dec snd1
    beq AudioStop
    lda snd1
    and #3
    sta audioTmp
    ldy priority
    lda EventFreq,y
    sec
    sbc audioTmp
    sta AUDF1
    lda snd1
    cmp #5
    bcs PoseTick
    lda #4
    sta AUDV1
    jmp PoseTick
AudioStop:
    lda #0""")
engine=engine.replace("    inc motionPhase\n    ldx #0","    inc motionPhase\n    lda spawnGap\n    beq GapReady\n    dec spawnGap\nGapReady:\n    ldx #0")
engine=engine.replace("Spawn:\n    jsr Random","""Spawn:
    lda spawnGap
    beq SpawnReady
    jmp NextObject
SpawnReady:
    lda #12
    ldy level
    cpy #12
    bcc SetGap
    lda #8
SetGap:
    sta spawnGap
    jsr Random""")
# RC2 modes and skill rewards.
engine=engine.replace("    sta level\n    sta speed\n    lda #8","""    sta level
    sta speed
    lda variant
    beq StandardStart
    lda #4
    sta active
    lda #7
    sta level
    lda #2
    sta speed
StandardStart:
    lda #8""")
engine=engine.replace("ResetReleased:\n    lda #0\n    sta resetHeld\nReadFire:","""ResetReleased:
    lda #0
    sta resetHeld
    lda mode
    cmp #1
    beq ReadFire
    lda SWCHB
    and #2
    bne SelectReleased
    lda selectHeld
    bne ReadFire
    inc selectHeld
    lda variant
    eor #1
    sta variant
    jsr NewGame
    lda #0
    sta mode
    jmp ReadFire
SelectReleased:
    lda #0
    sta selectHeld
ReadFire:""")
engine=engine.replace("    cmp #12\n    bcc BaseStep\n    txa","""    cmp #12
    bcc BaseStep
    and #3
    cmp #1
    beq BaseStep
    cmp #3
    bne AlternateFast
    inc stepSpeed
    jmp BaseStep
AlternateFast:
    txa""")
engine=engine.replace("    ldy #4\n    jsr EventSound\nNoBonus:","""    ldy #4
    jsr EventSound
    lda level
    and #3
    bne NoBonus
    lda lives
    cmp #3
    bcs NoBonus
    inc lives
NoBonus:""")
engine=engine.replace("ScoreDone:\n    rts","""ScoreDone:
    lda score+2
    cmp sessionBest+2
    bcc BestDone
    bne BestStore
    lda score+1
    cmp sessionBest+1
    bcc BestDone
    bne BestStore
    lda score
    cmp sessionBest
    bcc BestDone
BestStore:
    lda score
    sta sessionBest
    lda score+1
    sta sessionBest+1
    lda score+2
    sta sessionBest+2
BestDone:
    rts""")
engine+=section("Masks","Times5")+section("InputFreq","ObjColor")
display="    .byte $00\n    ORG $F01F\n"+section("Frame","NewGame").replace("jsr PrepareHUD","jsr F6HUD").replace("jsr Update","jsr F6Logic").replace("    ldy kind,x\n    lda ObjectTable,y\n    sta p1ptr","    lda objectPtr,x\n    sta p1ptr").replace("    lda #WATER\nWaterSet:","    lda themeWater\nWaterSet:")
# Keep normal HMOVE strobe; conceal the notch with a deliberate dark separator.
old="    sta HMOVE\n"+"    nop\n"*12+"    sta HMCLR\n    sta WSYNC\n    ldx lane"
new="    sta HMOVE\n    lda #0\n    sta COLUBK\n    sta PF0\n"+"    nop\n"*8+"    sta HMCLR\n    sta WSYNC\n    ldx lane"
assert old in display
display=display.replace(old,new).replace("    sta gateMid\n    sta WSYNC\n    sta WSYNC\n    sta WSYNC\n    sta WSYNC","    sta gateMid\n    sta WSYNC\n    lda #$30\n    sta PF0\n    lda #4\n    sta COLUBK\n    sta WSYNC\n    sta WSYNC\n    sta WSYNC")
# Water surface and floor highlights; preserve line count.
display=display.replace("    lda laneWater\n    sta COLUBK\n    lda #2","    lda laneWater\n    eor #2\n    sta COLUBK\n    lda #2",1)
display=display.replace("    lda gateMid\n    sta ENABL","    lda laneWater\n    sta COLUBK\n    lda gateMid\n    sta ENABL",1)
display=display.replace("    sta GRP1\n    sta WSYNC\n    sta WSYNC\n    lda #2\n    sta ENABL","    sta GRP1\n    sta WSYNC\n    sta WSYNC\n    lda laneWater\n    eor #2\n    sta COLUBK\n    lda #2\n    sta ENABL",1)
display+=section("Masks","InitialDelay")+section("ObjColor","GlyphL1")
display+="""
    ORG $F900
Blank: .byte 0,0,0,0,0,0,0,0,0,0
    include "graphics/V1/asm/graphics_data.inc"
CargoAlt: .byte $7E,$FF,$C3,$BD,$A5,$BD,$C3,$FF,$7E,$00
DebrisAlt: .byte $00,$20,$62,$36,$1C,$7E,$38,$4C,$04,$00
    IF cargo != $F928
    ERR
    ENDIF
    IF debris != $F932
    ERR
    ENDIF
    IF cargo_hit != $F93C
    ERR
    ENDIF
    IF debris_hit != $F946
    ERR
    ENDIF
    IF CargoAlt != $F982
    ERR
    ENDIF
"""
hud=section("PrepareHUD","Masks").replace("PrepareHUD:\n","""PrepareHUD:
    lda hudValid
    beq HUDRefresh
    lda mode
    cmp hudMode
    bne HUDRefresh
    lda lives
    cmp hudLives
    bne HUDRefresh
    lda score
    cmp hudScore
    bne HUDRefresh
    lda score+1
    cmp hudScore+1
    bne HUDRefresh
    lda score+2
    cmp hudScore+2
    bne HUDRefresh
    jmp HUDPresent
HUDRefresh:
    lda #1
    sta hudValid
    lda mode
    sta hudMode
    lda lives
    sta hudLives
    lda score
    sta hudScore
    lda score+1
    sta hudScore+1
    lda score+2
    sta hudScore+2
""").replace("    sta lifeR\n    rts","    sta lifeR\nHUDPresent:\n    jsr F6Presentation\n    rts")
# Ready screen can display retained session record while RIGHT is held.
hud=hud.replace("PrepareHUD:\n    lda hudValid","PrepareHUD:\n    lda mode\n    beq HUDRefresh\n    lda hudValid")
hud=hud.replace("    sta hudScore+2\n    lda score+2","""    sta hudScore+2
    lda mode
    bne UseHUDScore
    lda SWCHA
    and #$80
    bne UseHUDScore
    lda sessionBest
    sta hudScore
    lda sessionBest+1
    sta hudScore+1
    lda sessionBest+2
    sta hudScore+2
UseHUDScore:
    lda hudScore+2""")
pre,post=hud.split("UseHUDScore:",1)
hud=pre+"UseHUDScore:"+post.replace("lda score","lda hudScore")
hud+=section("Times5","InputFreq")+a[a.index("\nGlyphL1:")+1:a.index("    ALIGN 256")]
import re
hud=re.sub(r"^GlyphR0:.*$","GlyphR0 = GlyphL3",hud,flags=re.M)
pres="""
Present:
    lda level
    lsr
    lsr
    and #3
    tax
    lda WaterThemes,x
    sta themeWater
    ldx #3
ArtLoop:
    ldy kind,x
    lda BasePtr,y
    cpy #1
    beq Anim
    cpy #2
    bne ArtStore
Anim:
    lda motionPhase
    and #8
    beq ArtBase
    lda AltPtr,y
    bne ArtStore
ArtBase:
    lda BasePtr,y
ArtStore:
    sta objectPtr,x
    dex
    bpl ArtLoop
    lda mode
    bne PresentDone
    lda SWCHA
    and #$80
    beq PresentDone
    lda variant
    bne ExpertTitle
    ldx #4
TitleLoop:
    lda Title1,x
    sta h1,x
    lda Title2,x
    sta h2,x
    lda Title3,x
    sta h3,x
    lda Title4,x
    sta h4,x
    dex
    bpl TitleLoop
    rts
ExpertTitle:
    ldx #4
ExpertLoop:
    lda Expert1,x
    sta h1,x
    lda Expert2,x
    sta h2,x
    lda Expert3,x
    sta h3,x
    lda Expert4,x
    sta h4,x
    dex
    bpl ExpertLoop
PresentDone:
    rts
BasePtr: .byte $00,$28,$32,$28,$46,$3C,$32
AltPtr: .byte $00,$82,$8C
    IF TV = 1
WaterThemes: .byte $B2,$B4,$D2,$D4
    ELSE
WaterThemes: .byte $82,$84,$A2,$A4
    ENDIF
"""
def rev(v):return ((v&1)<<2)|(v&2)|((v&4)>>2)
def title(name,letters):
    rows=[[letters[0][y]<<1 for y in range(5)],[(rev(letters[1][y])|rev(letters[2][y])<<4) for y in range(5)],[rev(letters[3][y])<<4 for y in range(5)],[(letters[4][y]<<5|letters[5][y]<<1) for y in range(5)]]
    return "\n".join("%s%d: .byte %s"%(name,i+1,",".join(map(str,row))) for i,row in enumerate(rows))+"\n"
pres+=title("Title",[[7,4,7,1,7],[4,4,4,4,7],[5,5,5,5,7],[7,2,2,2,7],[7,4,4,4,7],[7,4,7,4,7]])
pres+=title("Expert",[[7,4,7,4,7],[5,5,2,5,5],[7,5,7,4,4],[7,4,7,4,7],[7,5,7,6,5],[7,2,2,2,2]])
out=Path(sys.argv[1] if len(sys.argv)>1 else "build");out.mkdir(parents=True,exist_ok=True)
for b,code in enumerate([engine,display,hud,pres]):
    (out/f"bank{b}.asm").write_text(head+"    IF ramEnd > $E0\n    ERR\n    ENDIF\n"+code+"\nBankUsedEnd:\n"+stub)
report={}
for tv,flag in [("NTSC",0),("PAL",1)]:
    banks=[];used=[]
    for b in range(4):
        stem=out/f"{tv}_bank{b}"
        cmd=["dasm",str(out/f"bank{b}.asm"),"-f3",f"-DTV={flag}",f"-o{stem}.bin",f"-l{stem}.lst",f"-s{stem}.sym"]
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        Path(f"{stem}.log").write_text(p.stdout);print(tv,b,p.stdout,flush=True);p.check_returncode()
        data=Path(f"{stem}.bin").read_bytes()
        assert len(data)==4096,(tv,b,len(data))
        assert data[-6:]==bytes([0xc0,0xff])*3
        assert not banks or data[0xfc0:0xffa]==banks[0][0xfc0:0xffa]
        banks.append(data)
        syms={f[0]:int(f[1],16) for l in Path(f"{stem}.sym").read_text().splitlines() if len(f:=l.split())>1 and len(f[1])==4 and all(c in '0123456789abcdefABCDEF' for c in f[1])}
        used.append({"bank":b,"end":hex(syms["BankUsedEnd"]),"span_before_stub":syms["BankUsedEnd"]-0xf000,"tail_free":0xffc0-syms["BankUsedEnd"],"sha256":hashlib.sha256(data).hexdigest()})
    assert len(set(banks))==4
    rom=b"".join(banks);(out/f"SLUICE_PANIC_{tv}.bin").write_bytes(rom)
    (out/f"{tv}.sym").write_bytes((out/f"{tv}_bank0.sym").read_bytes())
    report[tv]={"bytes":len(rom),"sha256":hashlib.sha256(rom).hexdigest(),"banks":used}
(out/"bank_report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
