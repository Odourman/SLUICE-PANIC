# SLUICE PANIC! — game design (ROM DEVELOPMENT)
Status: implementation checkpoint, not independent verification or commercial release.
Authority: user's full development mandate; GRAPHICS V1 preserved on its original branch and inherited here.

## Player manual
You are the keeper of a four-channel sluice station. Open the gates for valuable yellow crates and close them for hazardous red debris. Both move from left to right. The white keeper identifies your selected gate. Solid gate = shut; short end caps = open.
- Standard joystick up/down selects an active channel, held direction repeats. Both directions at once count as neutral. FIRE toggles the selected gate once per press. FIRE while ready or after Game Over starts a new game. RESET starts a new game directly. SELECT and difficulty switches have no extra function.
- Cargo through an open gate: 100 points. Debris stopped by a closed gate: 25. Cargo stopped or debris let through: lose one life. Start with 3 lives, all gates shut, 0 points, 2 active lanes. The other gates are visible but not selectable.
- Eight judged objects form a round. If all eight were correct: +500 points. Every round increments the level; level 2 opens the third lane; level 3 opens the fourth. The level counter saturates at 255, score at 999999. No extra lives or permanent high score.
- If a mistake costs a life, all other objects disappear and respawn on staggered delays. The mistaken object briefly shows a hit or travels out; input is never locked. Preserve score and gates. Last life: final red score, no keeper or objects; FIRE or RESET starts over.
- Each lane contains one transport object at most. The cargo is a square with a cross pattern; debris is an irregular branch. Look at each object as soon as it enters, and set the appropriate gate before its leading edge reaches the gate.
- Release FIRE before another toggle. If moving and pressing FIRE simultaneously, the old selection is toggled first. Resolve crossings in ascending lane order, input first. A first error clears other objects in that tick, preventing multiple simultaneous life losses; earlier correct scores remain.

## Progression
Movement logic at 50 Hz for PAL and NTSC (NTSC omits one logical tick per six video frames). Start delays 8/40/72/104 ticks, one LFSR-selected object per lane. After retirement: 15–46 ticks, from level 8: 10–25. Speeds: levels 1–3 1 clock/tick; 4–6 alternate 1 and 2; 7–11 2; 12+ alternate 2/3, phase differs by lane. Max instantaneous 3. Hit objects held 7 ticks. These are developer design choices, not human-playtest approval.

## Display and audio
GRAPHICS V1: 192 visible lines, HUD 24, four 40-line channels, 8 footer. Six digits with asymmetric PF, life bars. P0 keeper, P1 multiplexed by vertical lane, Ball gate, PF rails, background water/banks. Original sprite rows and NTSC/PAL color constants inherited. P0/ball/P1 position inputs compensate reported +3/+2/+3 diagnostic offsets; physical pixel result requires measurement. HMOVE performed in bank; HMCLR after 24 cycles. One visual feedback lane at a time, error priority. Pose/bonus/error timers scaled PAL vs NTSC. TIA AUD0: movement, opening, closing (AUDF 20/8/16, AUDC 4, V5); AUD1: success, debris stop, level/start, bonus, error, game over (AUDF 5/13/9/3/24/30, AUDC 4 except error/game over 8, V9). Higher event ID wins; independent input sound channel. No music.

## Build
Run from repository root:
    dasm src/main.asm -f3 -DTV=0 -oSLUICE_PANIC_NTSC.bin -lNTSC.lst -sNTSC.sym
    dasm src/main.asm -f3 -DTV=1 -oSLUICE_PANIC_PAL.bin -lPAL.lst -sPAL.sym
Standard unbanked 4 KiB cartridge, no extra RAM. 3 VSYNC + 37/62 VBLANK + 192 visible + 30/55 overscan target. Verify actual line counts, pixel positions and audio on both formats. Test suite tests/rom_cpu.py executes the actual DASM binary under py65 with approximate RIOT and WSYNC model; it cannot certify TIA pixel output, PCM, or hardware.

## Verification / release gate
Read source, build both ROMs independently, compare SHA-256 to frozen evidence. Test 16 gate masks, selected positions, six digits including 123456/888888/999999, all object and feedback types, maximum simultaneous objects, raster count, each movement/edge case, collisions and score, bonus, reset, game over, 50/60 Hz timing, and long adversarial play. Check actual TIA/RIOT and stack usage, no ghost sprites or unintentional flicker, validate audio and CRT. Report hardware NOT_RUN unless actually performed. Review graphics before approval. Do not infer independent verification from developer evidence. Main reviews draft PR before merge; ART/PACKAGING may use this manual and original GRAPHICS V1 but must not infer release approval.
