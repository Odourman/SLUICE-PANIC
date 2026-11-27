"""Generate DASM source and independently encoded fixed-scene diagnostic (not a game).
Encoder is intentionally tiny, with line-cycle accounting; not a TIA emulator."""
from pathlib import Path
import json,sys,hashlib
from generate import S,P,pf,hud_bits
R=Path(__file__).resolve().parents[1]
REG={'VSYNC':0,'VBLANK':1,'WSYNC':2,'NUSIZ0':4,'NUSIZ1':5,'COLUP0':6,'COLUP1':7,'COLUPF':8,'COLUBK':9,'CTRLPF':10,'REFP0':11,'REFP1':12,'PF0':13,'PF1':14,'PF2':15,'RESP0':16,'RESP1':17,'RESBL':20,'AUDV0':25,'AUDV1':26,'GRP0':27,'GRP1':28,'ENAM0':29,'ENAM1':30,'ENABL':31,'HMP0':32,'HMP1':33,'HMBL':36,'VDELP0':37,'VDELP1':38,'VDELBL':39,'RESMP0':40,'RESMP1':41,'HMOVE':42,'HMCLR':43,'CXCLR':44}
for tv in ('NTSC','PAL'):
    code=bytearray();src=['    processor 6502']+[f'{k} = ${v:02X}' for k,v in REG.items()]+['    org $F000'];labels={};fix=[];cycle=0;lines=[];phase='init';poscount=0
    def label(n):labels[n]=0xf000+len(code);src.append(n+':')
    def op(s,bs,c):
        global cycle
        src.append('    '+s);code.extend(bs);cycle+=c
    def imm(n):op(f'lda #${n:02X}',[0xa9,n],2)
    def sta(r):op('sta '+r,[0x85,REG[r]],3)
    def val(r,n):imm(n);sta(r)
    def w():
        global cycle
        sta('WSYNC');assert cycle<=76,(tv,phase,len(lines),cycle);lines.append((phase,cycle));cycle=0
    def pad(n):
        assert n>=0 and n!=1,n
        if n%2:op('bit $80',[0x24,0x80],3);n-=3
        for _ in range(n//2):op('nop',[0xea],2)
    def jump(n):fix.append((len(code)+1,n,'abs'));op('jmp '+n,[0x4c,0,0],3)
    def position(x,obj):
        # Standard 15-clock coarse / fine algorithm, inlined; x <= 136.
        global poscount,cycle
        assert cycle==0
        imm(x);op(f'ldx #${obj:02X}',[0xa2,obj],2);op('sec',[0x38],2)
        # Four cycles from LDA/LDX must not be in timed position line: use preceding prep instead.
        # Position starts on following line; caller accounts for prep line.
        w();op('sec',[0x38],2)
        name=f'Pos{poscount}';poscount+=1;label(name)
        op('sbc #15',[0xe9,15],2);fix.append((len(code)+1,name,'rel'));op('bcs '+name,[0xb0,0],2)
        cycle+=5*(x//15) # model total taken loop executions, first untaken already counted
        op('eor #7',[0x49,7],2)
        for _ in range(4):op('asl',[0x0a],2)
        op('sta HMP0,x',[0x95,0x20],4);op('sta RESP0,x',[0x95,0x10],4);w()
        sta('HMOVE');pad(26);sta('HMCLR');w()
    # power-up initialization outside measured frame
    label('Reset');op('sei',[0x78],2);op('cld',[0xd8],2);op('ldx #$FF',[0xa2,255],2);op('txs',[0x9a],2);val('VBLANK',2);w()
    for group in [list(REG)[3:10],['REFP0','REFP1','PF0','PF1','PF2','AUDV0','AUDV1'],['GRP0','GRP1','ENAM0','ENAM1','ENABL','VDELP0','VDELP1','VDELBL','RESMP0','RESMP1','HMCLR','CXCLR']]:
        imm(0)
        for r in group:sta(r)
        w()
    label('Frame');phase='vsync';val('VSYNC',2);w();w();w()
    phase='vblank';val('VSYNC',0);val('VBLANK',2);w();position(136,0);position(120,4)
    for _ in range((37 if tv=='NTSC' else 62)-7):w()
    phase='visible';colors=P[tv];c=lambda k:colors[k][0]
    # HUD: preloads left fields within first 15 cycles, changes PF0/PF1/PF2 after left use.
    for y in range(24):
        b=hud_bits(1250,3,y);left,right=pf(b[:20]),pf(b[20:]);
        if y==0:val('VBLANK',0);val('COLUBK',c('black'));val('COLUPF',c('hud'));val('CTRLPF',0)
        for i,n in enumerate(left):val(f'PF{i}',n)
        # y0 is blank; all left and right zero; no rewrite necessary
        if y!=0:
            for i,target in enumerate((32,42,52)):
                pad(target-5-cycle);val(f'PF{i}',right[i]);assert cycle==target
        w()
    for i,x in enumerate((24,61,91,108)):
        base=24+40*i;kind=('cargo','debris','cargo','debris')[i];closed=i in (0,2)
        val('COLUBK',c('bank'));val('COLUPF',c('rail'));val('CTRLPF',0x21);val('PF0',0);val('PF1',0);val('PF2',0);val('GRP0',0);val('GRP1',0);val('ENABL',0);w()
        position(x,1)
        # last 4 top bank scanlines, with explicit HMOVE-black bar accepted on bank line
        for j in range(4):
            if j==0:val('COLUP0',c('keeper'));val('COLUP1',c(kind))
            w()
        for y in range(8,36):
            if y==8:val('COLUBK',c('water'));val('PF0',0x30)
            val('ENABL',2 if closed or y in (8,9,34,35) else 0)
            n=(y-12)//2 if 12<=y<32 else -1
            val('GRP1',S[kind][n] if n>=0 else 0);val('GRP0',S['keeper_idle'][n] if i==1 and n>=0 else 0)
            w()
        for j in range(4):
            if j==0:val('COLUBK',c('bank'));val('PF0',0);val('ENABL',0);val('GRP0',0);val('GRP1',0)
            w()
    for j in range(8):
        if j==0:val('COLUBK',0)
        w()
    phase='overscan';val('VBLANK',2);w()
    for _ in range((30 if tv=='NTSC' else 55)-1):w()
    # Jump occurs at the beginning of next measured VSYNC line; add cycles to that line.
    jump('Frame');assert lines[[x[0] for x in lines].index('vsync')][1]+3<=76
    for at,n,k in fix:
        a=labels[n]
        if k=='abs':code[at:at+2]=a.to_bytes(2,'little')
        else:
            off=a-(0xf000+at+1);assert -128<=off<=127;assert a&0xff00==(0xf000+at+1)&0xff00,('branch page cross',hex(a),hex(0xf000+at+1));code[at]=off&255
    assert len(code)<=4090,len(code)
    reset=labels['Reset'];used=len(code);code.extend(bytes(4090-len(code)));code.extend(reset.to_bytes(2,'little')*3)
    src+=['    ds $FFFA-*,0','    .word Reset, Reset, Reset']
    (R/'asm'/f'diagnostic_{tv}.asm').write_text('\n'.join(src)+'\n');(R/'experimental_roms'/f'SLUICE_PANIC_GRAPHICS_DIAGNOSTIC_{tv}.bin').write_bytes(code)
    counts={p:sum(a==p for a,b in lines) for p in ('vsync','vblank','visible','overscan')};assert counts==({'vsync':3,'vblank':37,'visible':192,'overscan':30} if tv=='NTSC' else {'vsync':3,'vblank':62,'visible':192,'overscan':55}),counts
    (R/'evidence'/f'{tv}_static_cycles.json').write_text(json.dumps({'status':'STATIC_MODEL_ONLY','frame_line_counts':counts,'max_cycles_to_WSYNC':max(b for a,b in lines if a!='init'),'used_bytes_before_padding':used,'sha256':hashlib.sha256(code).hexdigest(),'lines':lines,'caveats':['No CPU execution or TIA emulator; position branches checked not to cross page.','DASM not run; DASM equivalence not executed; explicit zero fill specified.','Position calibration, initial VSYNC transition and HMOVE artifact not empirically checked.']},indent=2))
    print(tv,counts,used,hashlib.sha256(code).hexdigest())
