; GRAPHICS V1, top-down, each byte repeated two scanlines
keeper_idle:
    .byte $3C,$7E,$38,$38,$7C,$FE,$7C,$38,$28,$6C
keeper_operate:
    .byte $3C,$7E,$38,$38,$78,$F8,$7C,$38,$28,$6C
keeper_error:
    .byte $3C,$7E,$38,$BA,$7C,$38,$38,$28,$44,$82
cargo:
    .byte $7E,$FF,$C3,$A5,$99,$A5,$C3,$FF,$7E,$00
debris:
    .byte $00,$04,$46,$6C,$38,$7E,$1C,$32,$20,$00
cargo_hit:
    .byte $42,$24,$18,$81,$3C,$3C,$81,$18,$24,$42
debris_hit:
    .byte $00,$81,$24,$00,$18,$18,$00,$24,$81,$00
digits:
    .byte $07,$05,$05,$05,$07
    .byte $02,$06,$02,$02,$07
    .byte $07,$01,$07,$04,$07
    .byte $07,$01,$07,$01,$07
    .byte $05,$05,$07,$01,$01
    .byte $07,$04,$07,$01,$07
    .byte $07,$04,$07,$05,$07
    .byte $07,$01,$01,$01,$01
    .byte $07,$05,$07,$05,$07
    .byte $07,$05,$07,$01,$07
