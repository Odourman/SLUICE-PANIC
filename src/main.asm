    processor 6502
; SLUICE PANIC! development build. DASM -f3 -DTV=0/1
    IF TV = 1
WATER = $B2
COLOR_CARGO = $2E
COLOR_DEBRIS = $66
VBT = 73
OST = 65
MOVE_REPEAT = 8
POSE_T = 7
ERROR_T = 17
BONUS_T = 25
INPUT_T = 3
    ELSE
WATER = $82
COLOR_CARGO = $1E
COLOR_DEBRIS = $48
VBT = 43
OST = 35
MOVE_REPEAT = 10
POSE_T = 8
ERROR_T = 20
BONUS_T = 30
INPUT_T = 4
    ENDIF
VSYNC = $00
VBLANK = $01
WSYNC = $02
NUSIZ0 = $04
NUSIZ1 = $05
COLUP0 = $06
COLUP1 = $07
COLUPF = $08
COLUBK = $09
CTRLPF = $0A
PF0 = $0D
PF1 = $0E
PF2 = $0F
RESP0 = $10
RESP1 = $11
AUDC0 = $15
AUDC1 = $16
AUDF0 = $17
AUDF1 = $18
AUDV0 = $19
AUDV1 = $1A
GRP0 = $1B
GRP1 = $1C
ENABL = $1F
HMP0 = $20
HMOVE = $2A
HMCLR = $2B
INPT4 = $0C
SWCHA = $0280
SWCHB = $0282
INTIM = $0284
TIM64T = $0296
    SEG.U RAM
    ORG $80
mode    ds 1
lives   ds 1
active  ds 1
keeper  ds 1
gates   ds 1
level   ds 1
roundN  ds 1
dirty   ds 1
score   ds 3
kind    ds 4
pos     ds 4
delay   ds 4
rng     ds 1
phase   ds 1
fireHeld ds 1
oldDir  ds 1
moveDelay ds 1
resetHeld ds 1
pose    ds 1
poseTimer ds 1
flashLane ds 1
flashTimer ds 1
flashColor ds 1
bonusTimer ds 1
snd0    ds 1
snd1    ds 1
priority ds 1
addLo   ds 1
addMid  ds 1
lane    ds 1
p0ptr   ds 2
p1ptr   ds 2
gateMid ds 1
laneWater ds 1
digit   ds 6
h1      ds 5
h2      ds 5
h3      ds 5
h4      ds 5
lifeL   ds 1
lifeR   ds 1
speed   ds 1
motionPhase ds 1
stepSpeed ds 1
errorKind ds 1
ramEnd  ds 0
    SEG CODE
    ORG $F000
Reset:
    sei
    cld
    ldx #$FF
    txs
    lda #0
Clear:
    sta $00,x
    dex
    bne Clear
    sta $00
    lda #$A7
    sta rng
    jsr NewGame
    lda #0
    sta mode
    lda #2
    sta VBLANK
    sta WSYNC
Frame:
    lda #2
    sta VSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #0
    sta VSYNC
    lda #VBT
    sta TIM64T
    lda #133
    ldx #0
    jsr Position
    lda #118
    ldx #4
    jsr Position
    jsr PrepareHUD
WaitVB:
    lda INTIM
    bne WaitVB
    sta WSYNC
    sta VBLANK
    sta COLUBK
    sta PF0
    sta PF1
    sta PF2
    sta CTRLPF
    sta GRP0
    sta GRP1
    sta ENABL
    lda #$0E
    ldx bonusTimer
    beq HudNoBonus
    lda #COLOR_CARGO
HudNoBonus:
    ldx mode
    cpx #2
    bne HudColor
    lda #COLOR_DEBRIS
HudColor:
    sta COLUPF
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #0
    sta PF0
    lda h1+0
    sta PF1
    lda h2+0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+0
    sta PF0
    nop
    nop
    lda h4+0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+0
    sta PF1
    lda h2+0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+0
    sta PF0
    nop
    nop
    lda h4+0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+1
    sta PF1
    lda h2+1
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+1
    sta PF0
    nop
    nop
    lda h4+1
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+1
    sta PF1
    lda h2+1
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+1
    sta PF0
    nop
    nop
    lda h4+1
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+2
    sta PF1
    lda h2+2
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+2
    sta PF0
    nop
    nop
    lda h4+2
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+2
    sta PF1
    lda h2+2
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+2
    sta PF0
    nop
    nop
    lda h4+2
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+3
    sta PF1
    lda h2+3
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+3
    sta PF0
    nop
    nop
    lda h4+3
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+3
    sta PF1
    lda h2+3
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+3
    sta PF0
    nop
    nop
    lda h4+3
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+4
    sta PF1
    lda h2+4
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+4
    sta PF0
    nop
    nop
    lda h4+4
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda h1+4
    sta PF1
    lda h2+4
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda h3+4
    sta PF0
    nop
    nop
    lda h4+4
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    sta PF1
    sta PF2
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #0
    sta PF0
    lda #0
    sta PF1
    lda lifeL
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda lifeR
    sta PF0
    nop
    nop
    lda #0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda #0
    sta PF1
    lda lifeL
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda lifeR
    sta PF0
    nop
    nop
    lda #0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda #0
    sta PF1
    lda lifeL
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda lifeR
    sta PF0
    nop
    nop
    lda #0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    lda #0
    sta PF1
    lda lifeL
    sta PF2
    nop
    nop
    nop
    nop
    nop
    lda lifeR
    sta PF0
    nop
    nop
    lda #0
    sta PF1
    nop
    nop
    lda #0
    sta PF2
    sta WSYNC
    lda #0
    sta PF0
    sta PF1
    sta PF2
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #0
    sta lane
LaneStart:
    ldx lane
    lda #$21
    sta CTRLPF
    lda #$30
    sta PF0
    lda #4
    sta COLUBK
    lda #$0A
    ldy flashTimer
    beq RailSet
    cpx flashLane
    bne RailSet
    lda flashColor
RailSet:
    sta COLUPF
    lda #0
    sta GRP0
    sta GRP1
    sta ENABL
    sta WSYNC
    ; top bank line 1: pointers, source assets in a single page.
    ldx lane
    lda #<Blank
    cpx keeper
    bne KeeperPtr
    ldy mode
    cpy #2
    beq KeeperPtr
    ldy pose
    lda KeeperTable,y
KeeperPtr:
    sta p0ptr
    lda #>Blank
    sta p0ptr+1
    sta p1ptr+1
    ldy kind,x
    lda ObjectTable,y
    sta p1ptr
    lda pos,x
    sec
    sbc #3
    ldx #1
    sta WSYNC
    sec
LanePos:
    sbc #15
    bcs LanePos
    eor #7
    asl
    asl
    asl
    asl
    sta HMP0,x
    sta RESP0,x
    sta WSYNC
    sta HMOVE
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sta HMCLR
    sta WSYNC
    ldx lane
    lda #2
    cpx active
    bcs WaterSet
    lda #WATER
WaterSet:
    sta laneWater
    ldy kind,x
    lda ObjColor,y
    sta COLUP1
    lda #$0E
    sta COLUP0
    lda #2
    ldy gates
    tya
    and Masks,x
    beq Closed
    lda #0
    beq GateSet
Closed:
    lda #2
GateSet:
    sta gateMid
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    ; water lines 8-11, two cap lines then middle.
    lda laneWater
    sta COLUBK
    lda #2
    sta ENABL
    sta WSYNC
    sta WSYNC
    lda gateMid
    sta ENABL
    sta WSYNC
    sta WSYNC
    ldy #0
ObjectRows:
    lda (p0ptr),y
    sta GRP0
    lda (p1ptr),y
    sta GRP1
    sta WSYNC
    sta WSYNC
    iny
    cpy #10
    bne ObjectRows
    lda #0
    sta GRP0
    sta GRP1
    sta WSYNC
    sta WSYNC
    lda #2
    sta ENABL
    sta WSYNC
    sta WSYNC
    lda #0
    sta ENABL
    lda #4
    sta COLUBK
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    inc lane
    lda lane
    cmp #4
    beq Footer
    jmp LaneStart
Footer:
    lda #0
    sta PF0
    sta PF1
    sta PF2
    sta COLUBK
    ldx #8
FooterLoop:
    sta WSYNC
    dex
    bne FooterLoop
    lda #2
    sta VBLANK
    lda #OST
    sta TIM64T
    jsr Update
WaitOS:
    lda INTIM
    bne WaitOS
    sta WSYNC
    jmp Frame
Position:
    sta WSYNC
    sec
PosLoop:
    sbc #15
    bcs PosLoop
    eor #7
    asl
    asl
    asl
    asl
    sta HMP0,x
    sta RESP0,x
    sta WSYNC
    sta HMOVE
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sta HMCLR
    sta WSYNC
    rts
NewGame:
    lda #0
    sta keeper
    sta gates
    sta dirty
    sta score
    sta score+1
    sta score+2
    sta pose
    sta poseTimer
    sta flashTimer
    sta bonusTimer
    sta snd0
    sta snd1
    sta priority
    sta AUDV0
    sta AUDV1
    sta phase
    sta motionPhase
    sta oldDir
    sta moveDelay
    lda #3
    sta lives
    lda #2
    sta active
    lda #1
    sta mode
    sta level
    sta speed
    lda #8
    sta roundN
    jsr ClearObjects
    rts
ClearObjects:
    ldx #3
ClearObjLoop:
    lda #0
    sta kind,x
    lda #8
    sta pos,x
    lda InitialDelay,x
    sta delay,x
    dex
    bpl ClearObjLoop
    rts
Update:
    ; timers are real video frames; logic advances 50 times/sec.
    lda snd0
    beq Audio1
    dec snd0
    bne Audio1
    lda #0
    sta AUDV0
Audio1:
    lda snd1
    beq PoseTick
    dec snd1
    bne PoseTick
    lda #0
    sta AUDV1
    sta priority
PoseTick:
    lda poseTimer
    beq FlashTick
    dec poseTimer
    bne FlashTick
    lda #0
    sta pose
FlashTick:
    lda flashTimer
    beq BonusTick
    dec flashTimer
BonusTick:
    lda bonusTimer
    beq ResetInput
    dec bonusTimer
ResetInput:
    lda SWCHB
    and #1
    bne ResetReleased
    lda resetHeld
    beq LongBranch1
    jmp ReadFire
LongBranch1:
    inc resetHeld
    jsr NewGame
    ldy #3
    jsr EventSound
    lda INPT4
    bmi ResetNoFire
    lda #1
    sta fireHeld
    rts
ResetNoFire:
    lda #0
    sta fireHeld
    rts
ResetReleased:
    lda #0
    sta resetHeld
ReadFire:
    lda INPT4
    bmi FireReleased
    lda fireHeld
    beq LongBranch2
    jmp ReadMove
LongBranch2:
    inc fireHeld
    lda mode
    cmp #1
    beq Toggle
    jsr NewGame
    ldy #3
    jsr EventSound
    rts
Toggle:
    ldx keeper
    lda gates
    eor Masks,x
    sta gates
    and Masks,x
    beq Closing
    ldy #1
    bne ToggleSound
Closing:
    ldy #2
ToggleSound:
    jsr InputSound
    lda pose
    cmp #2
    bne LongBranch3
    jmp ReadMove
LongBranch3:
    lda #1
    sta pose
    lda #POSE_T
    sta poseTimer
    jmp ReadMove
FireReleased:
    lda #0
    sta fireHeld
ReadMove:
    lda mode
    cmp #1
    beq Movement
    jsr Random
    rts
Movement:
    lda SWCHA
    and #$30
    beq Neutral
    cmp #$30
    beq Neutral
    cmp oldDir
    bne MoveNow
    dec moveDelay
    beq LongBranch4
    jmp Tick
LongBranch4:
MoveNow:
    sta oldDir
    lda #MOVE_REPEAT
    sta moveDelay
    lda oldDir
    cmp #$20
    bne Down
    lda keeper
    bne LongBranch5
    jmp Tick
LongBranch5:
    dec keeper
    jmp MoveSound
Down:
    lda keeper
    clc
    adc #1
    cmp active
    bcc LongBranch6
    jmp Tick
LongBranch6:
    sta keeper
MoveSound:
    ldy #0
    jsr InputSound
    jmp Tick
Neutral:
    lda #0
    sta oldDir
    sta moveDelay
Tick:
    IF TV = 0
    inc phase
    lda phase
    cmp #6
    bne RunTick
    lda #0
    sta phase
    rts
RunTick:
    ENDIF
    inc motionPhase
    ldx #0
ObjectLoop:
    lda kind,x
    bne Existing
    lda delay,x
    beq Spawn
    dec delay,x
    jmp NextObject
Spawn:
    jsr Random
    and #1
    clc
    adc #1
    sta kind,x
    lda #8
    sta pos,x
    jmp NextObject
Existing:
    cmp #4
    beq HoldHit
    cmp #5
    bne Moving
HoldHit:
    dec delay,x
    beq LongBranch7
    jmp NextObject
LongBranch7:
    jmp Retire
Moving:
    lda speed
    sta stepSpeed
    lda level
    cmp #4
    bcc BaseStep
    cmp #7
    bcs LateStep
    lda motionPhase
    and #1
    beq BaseStep
    inc stepSpeed
    jmp BaseStep
LateStep:
    cmp #12
    bcc BaseStep
    txa
    eor motionPhase
    and #1
    beq BaseStep
    inc stepSpeed
BaseStep:
    lda pos,x
    clc
    adc stepSpeed
    sta pos,x
    cmp #129
    bcc LongBranch8
    jmp Retire
LongBranch8:
    lda kind,x
    cmp #3
    bcc LongBranch9
    jmp NextObject
LongBranch9:
    lda pos,x
    cmp #112
    bcs LongBranch10
    jmp NextObject
LongBranch10:
    lda gates
    and Masks,x
    beq ShutGate
    lda kind,x
    cmp #1
    beq LongBranch11
    jmp Mistake
LongBranch11:
    lda #3
    sta kind,x
    lda #0
    sta addLo
    lda #1
    sta addMid
    ldy #1
    bne Success
ShutGate:
    lda kind,x
    cmp #2
    beq LongBranch12
    jmp Mistake
LongBranch12:
    lda #4
    sta kind,x
    lda #112
    sta pos,x
    lda #7
    sta delay,x
    lda #$25
    sta addLo
    lda #0
    sta addMid
    ldy #2
Success:
    jsr EventSound
    jsr AddScore
    lda #COLOR_CARGO
    jsr Flash
    jsr CountOutcome
    jmp NextObject
Mistake:
    lda kind,x
    sta errorKind
    lda #1
    sta dirty
    lda #COLOR_DEBRIS
    jsr Flash
    lda #2
    sta pose
    lda #ERROR_T
    sta poseTimer
    dec lives
    ldy #5
    jsr EventSound
    jsr CountOutcome
    jsr ClearObjects
    lda lives
    bne ErrorDisplay
    lda #2
    sta mode
    ldy #6
    jsr EventSound
    rts
ErrorDisplay:
    ldx flashLane
    lda #112
    sta pos,x
    lda errorKind
    cmp #1
    bne ErrorPassed
    lda #5
    sta kind,x
    lda #7
    sta delay,x
    rts
ErrorPassed:
    lda #6
    sta kind,x
    rts
Retire:
    lda #0
    sta kind,x
    jsr Random
    and #31
    ldy level
    cpy #8
    bcc NormalDelay
    lsr
    clc
    adc #10
    bne StoreDelay
NormalDelay:
    clc
    adc #15
StoreDelay:
    sta delay,x
NextObject:
    inx
    cpx active
    bcs ObjectsDone
    jmp ObjectLoop
ObjectsDone:
    rts
Random:
    lda rng
    lsr
    bcc RandomStore
    eor #$B8
RandomStore:
    sta rng
    rts
Flash:
    cmp #COLOR_DEBRIS
    beq FlashError
    ldy flashTimer
    beq FlashStore
    ldy flashColor
    cpy #COLOR_DEBRIS
    beq FlashDone
FlashStore:
    sta flashColor
    stx flashLane
    lda #POSE_T
    sta flashTimer
FlashDone:
    rts
FlashError:
    sta flashColor
    stx flashLane
    lda #ERROR_T
    sta flashTimer
    rts
CountOutcome:
    dec roundN
    bne RoundDone
    lda #8
    sta roundN
    lda dirty
    bne NoBonus
    lda #0
    sta addLo
    lda #5
    sta addMid
    jsr AddScore
    lda #BONUS_T
    sta bonusTimer
    ldy #4
    jsr EventSound
NoBonus:
    ldy #3
    jsr EventSound
    lda #0
    sta dirty
    lda level
    cmp #255
    beq MaxLevel
    inc level
MaxLevel:
    lda active
    cmp #4
    bcs Faster
    inc active
    rts
Faster:
    lda level
    cmp #7
    bcc RoundDone
    lda #2
    sta speed
RoundDone:
    rts
AddScore:
    sed
    clc
    lda score
    adc addLo
    sta score
    lda score+1
    adc addMid
    sta score+1
    lda score+2
    adc #0
    sta score+2
    cld
    bcc ScoreDone
    lda #$99
    sta score
    sta score+1
    sta score+2
ScoreDone:
    rts
InputSound:
    lda InputFreq,y
    sta AUDF0
    lda #4
    sta AUDC0
    lda #5
    sta AUDV0
    lda #INPUT_T
    sta snd0
    rts
EventSound:
    tya
    cmp priority
    bcc EventDone
    sta priority
    lda EventFreq,y
    sta AUDF1
    lda EventCtrl,y
    sta AUDC1
    lda #9
    sta AUDV1
    lda EventLen,y
    sta snd1
EventDone:
    rts
PrepareHUD:
    lda score+2
    lsr
    lsr
    lsr
    lsr
    tax
    lda Times5,x
    sta digit+0
    lda score+2
    and #15
    tax
    lda Times5,x
    sta digit+1
    lda score+1
    lsr
    lsr
    lsr
    lsr
    tax
    lda Times5,x
    sta digit+2
    lda score+1
    and #15
    tax
    lda Times5,x
    sta digit+3
    lda score+0
    lsr
    lsr
    lsr
    lsr
    tax
    lda Times5,x
    sta digit+4
    lda score+0
    and #15
    tax
    lda Times5,x
    sta digit+5
    ldy #0
PrepRow:
    ldx digit
    lda GlyphL1,x
    sta h1,y
    ldx digit+1
    lda GlyphL2,x
    ldx digit+2
    ora GlyphL3,x
    sta h2,y
    ldx digit+3
    lda GlyphR0,x
    sta h3,y
    ldx digit+4
    lda GlyphR1,x
    ldx digit+5
    ora GlyphL1,x
    sta h4,y
    inc digit
    inc digit+1
    inc digit+2
    inc digit+3
    inc digit+4
    inc digit+5
    iny
    cpy #5
    bne PrepRow
    ldx lives
    lda LivesL,x
    sta lifeL
    lda LivesR,x
    sta lifeR
    rts
Masks: .byte 1,2,4,8
InitialDelay: .byte 8,40,72,104
Times5: .byte 0,5,10,15,20,25,30,35,40,45
LivesL: .byte 0,$30,$B0,$B0
LivesR: .byte 0,0,$10,$D0
InputFreq: .byte 20,8,16
EventFreq: .byte 0,5,13,9,3,24,30
EventCtrl: .byte 0,4,4,4,4,8,8
    IF TV = 1
EventLen: .byte 0,7,7,10,25,17,38
    ELSE
EventLen: .byte 0,8,8,12,30,20,45
    ENDIF
ObjColor: .byte 0,COLOR_CARGO,COLOR_DEBRIS,COLOR_CARGO,COLOR_DEBRIS,COLOR_CARGO,COLOR_DEBRIS
KeeperTable: .byte <keeper_idle,<keeper_operate,<keeper_error
ObjectTable: .byte <Blank,<cargo,<debris,<cargo,<debris_hit,<cargo_hit,<debris
GlyphL1: .byte 14,10,10,10,14,4,12,4,4,14,14,2,14,8,14,14,2,14,2,14,10,10,14,2,2,14,8,14,2,14,14,8,14,10,14,14,2,2,2,2,14,10,14,10,14,14,10,14,2,14
GlyphL2: .byte 7,5,5,5,7,2,3,2,2,7,7,4,7,1,7,7,4,7,4,7,5,5,7,4,4,7,1,7,4,7,7,1,7,5,7,7,4,4,4,4,7,5,7,5,7,7,5,7,4,7
GlyphL3: .byte 112,80,80,80,112,32,48,32,32,112,112,64,112,16,112,112,64,112,64,112,80,80,112,64,64,112,16,112,64,112,112,16,112,80,112,112,64,64,64,64,112,80,112,80,112,112,80,112,64,112
GlyphR0: .byte 112,80,80,80,112,32,48,32,32,112,112,64,112,16,112,112,64,112,64,112,80,80,112,64,64,112,16,112,64,112,112,16,112,80,112,112,64,64,64,64,112,80,112,80,112,112,80,112,64,112
GlyphR1: .byte 224,160,160,160,224,64,192,64,64,224,224,32,224,128,224,224,32,224,32,224,160,160,224,32,32,224,128,224,32,224,224,128,224,160,224,224,32,32,32,32,224,160,224,160,224,224,160,224,32,224
    ALIGN 256
Blank: .byte 0,0,0,0,0,0,0,0,0,0
    include "graphics/V1/asm/graphics_data.inc"
EndCode:
    IF EndCode > $FFFA
    ERR
    ENDIF
    ORG $FFFA
    .word Reset,Reset,Reset
