    processor 6502
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
REFP0 = $0B
REFP1 = $0C
PF0 = $0D
PF1 = $0E
PF2 = $0F
RESP0 = $10
RESP1 = $11
RESBL = $14
AUDV0 = $19
AUDV1 = $1A
GRP0 = $1B
GRP1 = $1C
ENAM0 = $1D
ENAM1 = $1E
ENABL = $1F
HMP0 = $20
HMP1 = $21
HMBL = $24
VDELP0 = $25
VDELP1 = $26
VDELBL = $27
RESMP0 = $28
RESMP1 = $29
HMOVE = $2A
HMCLR = $2B
CXCLR = $2C
    org $F000
Reset:
    sei
    cld
    ldx #$FF
    txs
    lda #$02
    sta VBLANK
    sta WSYNC
    lda #$00
    sta NUSIZ0
    sta NUSIZ1
    sta COLUP0
    sta COLUP1
    sta COLUPF
    sta COLUBK
    sta CTRLPF
    sta WSYNC
    lda #$00
    sta REFP0
    sta REFP1
    sta PF0
    sta PF1
    sta PF2
    sta AUDV0
    sta AUDV1
    sta WSYNC
    lda #$00
    sta GRP0
    sta GRP1
    sta ENAM0
    sta ENAM1
    sta ENABL
    sta VDELP0
    sta VDELP1
    sta VDELBL
    sta RESMP0
    sta RESMP1
    sta HMCLR
    sta CXCLR
    sta WSYNC
Frame:
    lda #$02
    sta VSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$00
    sta VSYNC
    lda #$02
    sta VBLANK
    sta WSYNC
    lda #$88
    ldx #$00
    sec
    sta WSYNC
    sec
Pos0:
    sbc #15
    bcs Pos0
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
    nop
    sta HMCLR
    sta WSYNC
    lda #$78
    ldx #$04
    sec
    sta WSYNC
    sec
Pos1:
    sbc #15
    bcs Pos1
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
    nop
    sta HMCLR
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$00
    sta VBLANK
    lda #$00
    sta COLUBK
    lda #$0E
    sta COLUPF
    lda #$00
    sta CTRLPF
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0E
    sta PF1
    lda #$27
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EE
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0E
    sta PF1
    lda #$27
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EE
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$35
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$40
    sta PF0
    bit $80
    nop
    lda #$8A
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$35
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$40
    sta PF0
    bit $80
    nop
    lda #$8A
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$25
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EA
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$25
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EA
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$25
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$10
    sta PF0
    bit $80
    nop
    lda #$2A
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0A
    sta PF1
    lda #$25
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$10
    sta PF0
    bit $80
    nop
    lda #$2A
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0E
    sta PF1
    lda #$77
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EE
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$0E
    sta PF1
    lda #$77
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$70
    sta PF0
    bit $80
    nop
    lda #$EE
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$B0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$D0
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$B0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$D0
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$B0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$D0
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$B0
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$D0
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    nop
    nop
    nop
    nop
    nop
    nop
    lda #$00
    sta PF0
    bit $80
    nop
    lda #$00
    sta PF1
    bit $80
    nop
    lda #$00
    sta PF2
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$0A
    sta COLUPF
    lda #$21
    sta CTRLPF
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    lda #$00
    sta ENABL
    sta WSYNC
    lda #$18
    ldx #$01
    sec
    sta WSYNC
    sec
Pos2:
    sbc #15
    bcs Pos2
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
    nop
    sta HMCLR
    sta WSYNC
    lda #$0E
    sta COLUP0
    lda #$1E
    sta COLUP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$82
    sta COLUBK
    lda #$30
    sta PF0
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$99
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$99
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$00
    sta PF0
    lda #$00
    sta ENABL
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$0A
    sta COLUPF
    lda #$21
    sta CTRLPF
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    lda #$00
    sta ENABL
    sta WSYNC
    lda #$3D
    ldx #$01
    sec
    sta WSYNC
    sec
Pos3:
    sbc #15
    bcs Pos3
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
    nop
    sta HMCLR
    sta WSYNC
    lda #$0E
    sta COLUP0
    lda #$48
    sta COLUP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$82
    sta COLUBK
    lda #$30
    sta PF0
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$3C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$3C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$04
    sta GRP1
    lda #$7E
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$04
    sta GRP1
    lda #$7E
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$46
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$46
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$6C
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$6C
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$38
    sta GRP1
    lda #$7C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$38
    sta GRP1
    lda #$7C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$FE
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$FE
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$1C
    sta GRP1
    lda #$7C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$1C
    sta GRP1
    lda #$7C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$32
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$32
    sta GRP1
    lda #$38
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$20
    sta GRP1
    lda #$28
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$20
    sta GRP1
    lda #$28
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$6C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$6C
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$00
    sta PF0
    lda #$00
    sta ENABL
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$0A
    sta COLUPF
    lda #$21
    sta CTRLPF
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    lda #$00
    sta ENABL
    sta WSYNC
    lda #$5B
    ldx #$01
    sec
    sta WSYNC
    sec
Pos4:
    sbc #15
    bcs Pos4
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
    nop
    sta HMCLR
    sta WSYNC
    lda #$0E
    sta COLUP0
    lda #$1E
    sta COLUP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$82
    sta COLUBK
    lda #$30
    sta PF0
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$99
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$99
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$A5
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$C3
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$FF
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$00
    sta PF0
    lda #$00
    sta ENABL
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$0A
    sta COLUPF
    lda #$21
    sta CTRLPF
    lda #$00
    sta PF0
    lda #$00
    sta PF1
    lda #$00
    sta PF2
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    lda #$00
    sta ENABL
    sta WSYNC
    lda #$6C
    ldx #$01
    sec
    sta WSYNC
    sec
Pos5:
    sbc #15
    bcs Pos5
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
    nop
    sta HMCLR
    sta WSYNC
    lda #$0E
    sta COLUP0
    lda #$48
    sta COLUP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$82
    sta COLUBK
    lda #$30
    sta PF0
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$04
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$04
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$46
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$46
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$6C
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$6C
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$38
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$38
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$7E
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$1C
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$1C
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$32
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$32
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$20
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$20
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$00
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$02
    sta ENABL
    lda #$00
    sta GRP1
    lda #$00
    sta GRP0
    sta WSYNC
    lda #$04
    sta COLUBK
    lda #$00
    sta PF0
    lda #$00
    sta ENABL
    lda #$00
    sta GRP0
    lda #$00
    sta GRP1
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$00
    sta COLUBK
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #$02
    sta VBLANK
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    jmp Frame
    ds $FFFA-*,0
    .word Reset, Reset, Reset
