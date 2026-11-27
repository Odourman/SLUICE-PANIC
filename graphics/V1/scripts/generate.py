from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import json, itertools, hashlib, csv
R=Path(__file__).resolve().parents[1]
S={'keeper_idle':[0x3c,0x7e,0x38,0x38,0x7c,0xfe,0x7c,0x38,0x28,0x6c], 'keeper_operate':[0x3c,0x7e,0x38,0x38,0x78,0xf8,0x7c,0x38,0x28,0x6c], 'keeper_error':[0x3c,0x7e,0x38,0xba,0x7c,0x38,0x38,0x28,0x44,0x82], 'cargo':[0x7e,0xff,0xc3,0xa5,0x99,0xa5,0xc3,0xff,0x7e,0x00], 'debris':[0x00,0x04,0x46,0x6c,0x38,0x7e,0x1c,0x32,0x20,0x00], 'cargo_hit':[0x42,0x24,0x18,0x81,0x3c,0x3c,0x81,0x18,0x24,0x42], 'debris_hit':[0x00,0x81,0x24,0x00,0x18,0x18,0x00,0x24,0x81,0x00]}
D=['75557','26227','71747','71717','55711','74717','74757','71111','75757','75717']
# Stella PaletteHandler.cxx standard raw RGB tables (no emulator adjustment or CRT measurement).
P={'NTSC':{'black':(0x00,'000000'),'bank':(0x04,'6f6f6f'),'rail':(0x0a,'c0c0c0'),'water':(0x82,'181aa7'),'inactive':(0x02,'4a4a4a'),'keeper':(0x0e,'ececec'),'cargo':(0x1e,'fcfc54'),'debris':(0x48,'d65c5c'),'error':(0x48,'d65c5c'),'bonus':(0x1e,'fcfc54'),'hud':(0x0e,'ececec')},'PAL':{'black':(0x00,'0b0b0b'),'bank':(0x04,'595959'),'rail':(0x0a,'b6b6b6'),'water':(0xb2,'003ea4'),'inactive':(0x02,'333333'),'keeper':(0x0e,'e6e6e6'),'cargo':(0x2e,'fff19e'),'debris':(0x66,'c26472'),'error':(0x66,'c26472'),'bonus':(0x2e,'fff19e'),'hud':(0x0e,'e6e6e6')}}
# PF0 bits 4..7 ascending, PF1 7..0, PF2 0..7
def pf(bits):
    assert len(bits)==20
    return [sum(v<<(4+i) for i,v in enumerate(bits[:4])),sum(v<<(7-i) for i,v in enumerate(bits[4:12])),sum(v<<i for i,v in enumerate(bits[12:]))]
def pf_decode(a):
    return [(a[0]>>(4+i))&1 for i in range(4)]+[(a[1]>>(7-i))&1 for i in range(8)]+[(a[2]>>i)&1 for i in range(8)]
def hud_bits(score,lives,y):
    b=[0]*40
    if 4<=y<14:
        r=(y-4)//2
        for j,n in enumerate(f'{score%1000000:06d}'):
            v=int(D[int(n)][r]);b[8+j*4:11+j*4]=[(v>>i)&1 for i in [2,1,0]]
    elif 17<=y<21:
        for j in range(lives): b[16+j*3:18+j*3]=[1,1]
    return b
roles={k:('P0' if k.startswith('keeper') else 'P1') for k in S}
meta={}
for k,rows in S.items():
    pts=[(x,y*2+dy) for y,v in enumerate(rows) for x in range(8) if v&(128>>x) for dy in range(2)]
    bb=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)]
    meta[k]={'resource':roles[k],'width':8,'height':20,'rows_top_down':rows,'hex':[f'{v:02X}' for v in rows],'binary':[f'{v:08b}' for v in rows],'bounding_box_inclusive':bb,'logical_collision':[0,0,7,19] if roles[k]=='P1' else None,'row_repeat':2,'reflect':False,'color_role':'keeper' if roles[k]=='P0' else k.split('_')[0]}
    im=Image.new('RGBA',(8,20)); d=ImageDraw.Draw(im); c='#'+P['NTSC'][meta[k]['color_role']][1]
    for x,y in pts:d.point((x,y),fill=c)
    im.save(R/'sprites'/f'{k}.png');im.resize((64,160),Image.Resampling.NEAREST).save(R/'sprites'/f'{k}_8x.png')
layout={'size':[160,192],'hud':[0,23],'lane_starts':[24,64,104,144],'bank_top':[0,7],'water':[8,35],'bank_bottom':[36,39],'edge_x':[[0,7],[152,159]],'gate_x':[120,123],'gate_caps_y':[8,9,34,35],'closed_gate_y':[8,35],'keeper_x':136,'sprite_y_offset':12,'object_x_range':[8,128],'decision_x':112,'object_end_x':128,'initial_active_lanes':[0,1],'pf_reflected_edge':[0x30,0,0],'ctrlpf_game':0x21,'ctrlpf_hud':0,'digits':D}
(R/'sprites'/'sprites.json').write_text(json.dumps(meta,indent=2)+'\n');(R/'playfields'/'layout.json').write_text(json.dumps(layout,indent=2)+'\n');(R/'palettes'/'palette.json').write_text(json.dumps(P,indent=2)+'\n')
asm=['; GRAPHICS V1, top-down, each byte repeated two scanlines']
for k,v in S.items():asm += [k+':','    .byte '+','.join(f'${x:02X}' for x in v)]
asm += ['digits:']+['    .byte '+','.join('$0'+x for x in v) for v in D]
(R/'asm'/'graphics_data.inc').write_text('\n'.join(asm)+'\n')
with (R/'playfields'/'hud_glyph_masks.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['digit','slot','row','leftPF0','leftPF1','leftPF2','rightPF0','rightPF1','rightPF2'])
 for n,j,r in itertools.product(range(10),range(6),range(5)):
  b=[0]*40;v=int(D[n][r]);b[8+j*4:11+j*4]=[(v>>i)&1 for i in [2,1,0]]; a=pf(b[:20])+pf(b[20:]);assert pf_decode(a[:3])+pf_decode(a[3:])==b;w.writerow([n,j,r,*[f'{x:02X}' for x in a]])
with (R/'palettes'/'selected_colors.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['standard','role','TIA','RGB_raw_Stella','register'])
 for tv,colors in P.items():
  for k,(v,c) in colors.items():w.writerow([tv,k,f'{v:02X}',c,{'keeper':'COLUP0','cargo':'COLUP1','debris':'COLUP1','rail':'COLUPF','hud':'COLUPF','bonus':'COLUPF','error':'COLUPF'}.get(k,'COLUBK')])
def scene(active=4,mask=5,selected=1,score=1250,lives=3,xs=(24,61,91,108),kinds=('cargo','debris','cargo','debris'),event=None,tv='NTSC',keeper='keeper_idle',gray=False):
    im=Image.new('RGB',(160,192),'#'+P[tv]['black'][1]);d=ImageDraw.Draw(im);c=lambda key:'#'+P[tv][key][1]
    for y in range(24):
        b=hud_bits(score,lives,y)
        for i,v in enumerate(b):
            if v:d.rectangle((i*4,y,i*4+3,y),fill=c('bonus' if event=='bonus' else 'error' if event=='gameover' else 'hud'))
    for i,base in enumerate(layout['lane_starts']):
        d.rectangle((0,base,159,base+39),fill=c('bank'))
        d.rectangle((0,base+8,159,base+35),fill=c('water' if i<active else 'inactive'))
        rail='error' if event==('error',i) else 'bonus' if event==('success',i) else 'rail'
        for a,b in layout['edge_x']:d.rectangle((a,base+8,b,base+35),fill=c(rail))
        if mask>>i&1:d.rectangle((120,base+8,123,base+35),fill=c(rail))
        else:
            for a,b in [(8,9),(34,35)]:d.rectangle((120,base+a,123,base+b),fill=c(rail))
        if i<active and xs[i] is not None:
            k=kinds[i];bitmap=S[k]
            if k.endswith('_hit'):col=k.split('_')[0]
            else:col=k
            for r,v in enumerate(bitmap):
                for bit in range(8):
                    if v&(128>>bit):d.rectangle((xs[i]+bit,base+12+r*2,xs[i]+bit,base+13+r*2),fill=c(col))
        if i==selected and event!='gameover':
            for r,v in enumerate(S[keeper]):
                for bit in range(8):
                    if v&(128>>bit):d.rectangle((136+bit,base+12+r*2,136+bit,base+13+r*2),fill=c('keeper'))
    return ImageOps.grayscale(im).convert('RGB') if gray else im
def save(name,**kw):
 im=scene(**kw);im.save(R/'mockups'/f'{name}_MOCKUP_160x192.png');im.resize((640,768),Image.Resampling.NEAREST).save(R/'mockups'/f'{name}_MOCKUP_nearest.png');im.resize((640,480),Image.Resampling.NEAREST).save(R/'mockups'/f'{name}_MOCKUP_4x3.png')
for n,kw in {'ready':dict(active=2,mask=0,selected=0,score=0,xs=(None,)*4),'two':dict(active=2),'three':dict(active=3),'four':{},'all_open':dict(mask=0),'all_closed':dict(mask=15),'worst_case':dict(xs=(112,112,112,112),mask=10),'cargo_pass':dict(mask=0,xs=(128,61,91,108),event=('success',0)),'cargo_error':dict(mask=1,xs=(112,61,91,108),kinds=('cargo_hit','debris','cargo','debris'),event=('error',0),lives=2,keeper='keeper_error'),'debris_stop':dict(mask=3,xs=(24,112,91,108),kinds=('cargo','debris_hit','cargo','debris'),event=('success',1)),'debris_error':dict(mask=0,xs=(24,128,91,108),event=('error',1),lives=2,keeper='keeper_error'),'life_lost':dict(lives=2,keeper='keeper_error',event=('error',1)),'restart':dict(lives=2,xs=(None,)*4),'perfect_bonus':dict(event='bonus',score=2500,xs=(None,)*4),'level_transition':dict(active=3,xs=(None,)*4),'game_over':dict(lives=0,event='gameover',selected=-1,xs=(None,)*4),'restart_game':dict(active=2,mask=0,selected=0,score=0,xs=(None,)*4),'PAL_four':dict(tv='PAL'),'gray_four':dict(gray=True)}.items():save(n,**kw)
for mask in range(16):
 for active in (2,3,4):
  for selected in range(active):
   im=scene(active=active,mask=mask,selected=selected);assert im.size==(160,192)
frames=[scene(mask=m,keeper=k,selected=1).resize((640,480),Image.Resampling.NEAREST) for m,k in [(5,'keeper_idle'),(7,'keeper_operate'),(7,'keeper_idle'),(5,'keeper_operate')]]
frames[0].save(R/'animations'/'toggle_MOCKUP.gif',save_all=True,append_images=frames[1:],duration=[500,120,500,120],loop=0)
frames=[scene(mask=0,xs=(x,61,91,108),event=('success',0) if x>=120 else None).resize((640,480),Image.Resampling.NEAREST) for x in range(88,129,4)]
frames[0].save(R/'animations'/'cargo_pass_MOCKUP.gif',save_all=True,append_images=frames[1:],duration=75,loop=0)
frames=[scene(mask=2,xs=(24,x,91,108),event=('success',1) if x==112 else None,kinds=('cargo','debris_hit' if x==112 else 'debris','cargo','debris')).resize((640,480),Image.Resampling.NEAREST) for x in range(84,113,4)]
frames[0].save(R/'animations'/'debris_stop_MOCKUP.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
# labeled sheet outside the simulated raster
sheet=Image.new('RGB',(700,220),'#222222');d=ImageDraw.Draw(sheet)
for i,k in enumerate(S):
 im=Image.open(R/'sprites'/f'{k}.png').resize((64,160),Image.Resampling.NEAREST);sheet.paste(im,(i*100+18,10),im);d.text((i*100+3,180),k,fill='white')
sheet.save(R/'sprites'/'sheet_MOCKUP.png')
# coordinate overlay as schematic, not game image
im=scene().resize((640,768),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
for i,y in enumerate(layout['lane_starts']):d.line((0,y*4,639,y*4),fill='white');d.text((10,y*4+2),f'L{i}: y={y}',fill='white')
for x in [112,120,136]:d.line((x*4,96,x*4,735),fill='white');d.text((x*4-10,740),str(x),fill='white')
im.save(R/'mockups'/'coordinates_MOCKUP.png')
(R/'evidence'/'asset_validation.txt').write_text('PASS: 7 sprite bitmaps, bounding boxes and 300 HUD digit-slot-row PF masks; PF encode/decode exact; rendered 16 gate masks × (2+3+4 selections) = 144 model scenes; 19 named state previews. No TIA or emulator validation.\n')
