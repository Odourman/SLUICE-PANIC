# SLUICE PANIC! — RC3 game design and player manual
Status: developer release candidate; independent verification and release approval separate.

## Player controls
You keep a four-channel sluice station. Open gates for yellow cargo; shut gates for red debris. Both travel left to right. Solid gate means closed; short end caps mean open. The white keeper marks your selection; inactive channels are grey.
- Ready: SELECT toggles Classic (SLUICE) / EXPERT; hold RIGHT to view session best and release to return to the title. FIRE starts. RESET starts the current variant directly.
- Gameplay: UP/DOWN selects an active channel, held direction repeats (NTSC 10 video frames; PAL 8); opposing directions neutralize. FIRE toggles one gate per press, before movement if simultaneous. SELECT updates its edge latch but never changes variant during gameplay.
- Game Over: FIRE or RESET restarts current variant. New SELECT press goes to ready screen in the other variant. SELECT held across death cannot trigger a toggle. RESET has priority over simultaneous SELECT, and FIRE held during a fresh RESET is consumed. Difficulty switches have no gameplay function.
- Session best persists across game resets, not power-off. No permanent storage.

## Rules and progression
Classic starts level 1 with two active lanes; level 2 adds lane 3, level 3 adds lane 4. Expert starts level 7 with four lanes and speed 2. All gates shut, three lives, zero score. Correct cargo/open +100; debris/shut +25. Wrong gate costs one life, clears other objects, retains gates and earned score. Input is processed before object judgments, lanes in ascending order; one loss at most per tick and earlier correct points remain. Eight judged objects constitute a round. Clean round +500 and restores one life when current level is divisible by four, capped at three. All rounds increase level up to 255; score saturates at 999999. Last life lost: Game Over.
- 50 logical ticks/sec; NTSC skips one tick per six video frames. Levels 1–3 speed 1; 4–6 alternate 1/2; 7–11 speed 2; 12+ wave: modulo 4=0/2 alternate 2/3 by lane and phase, 1 speed 2, 3 speed 3. Max 3 clocks/tick.
- Initial delays 8/40/72/104 logical ticks; after retirement 15–46 ticks, level 8+ 10–25. Global spawn gap 12 ticks before level 12, 8 afterwards. One object per lane. Judgment at pos>=112; stopped hit holds 7 ticks; retirement at pos>=129. LFSR seeded at power-on and advances on idle/retirement/spawn. This is not proof of human fairness.

## Display and audio
192 visible lines: 24 HUD, four 40-line channels, 8 footer. Asymmetric six-digit playfield HUD; life bars; P0 keeper; P1 vertically multiplexed object; Ball gate; playfield rails. Alternating cargo/debris shapes (motionPhase bit 3), water palettes cycle by level/4, surface and floor highlights. Error flash priority; bonus score cue. Dark separator masks HMOVE notch rather than eliminating hardware blanking. No intentional flicker.
TIA AUD0 input: AUDF 20/8/16, AUDC 4, V5. AUD1 game events: higher event ID wins; two independent channels. Stepped pitch from EventFreq minus remaining timer low 2 bits; tail volume 4, stop volume 0. No music.

## Build and architecture
From repository root with native DASM and Python 3: `python tools/build_rc2.py build` (historical generator filename retained; on RC3 branch generates RC3). Builds NTSC/PAL standard 16,384-byte F6 ROMs, four 4 KiB banks, no extra cartridge RAM or processor. Bank0 engine, bank1 display, bank2 cached HUD, bank3 presentation. Shared trampolines at $FFC0; hotspots $FFF6–$FFF9; bank switches in blanking, not visible kernel. 128 bytes RIOT RAM, 97 allocated, stack reserve $E8–$FF. NTSC 262 / PAL 312 target lines; 76 CPU cycles per line. Original src/main.asm is the frozen RC1 input to generator, not final standalone F6 build.
Tests: `python tests/rc2_cpu.py` (actual ROM, approximate RIOT bus); `python tests/rc3_regression.py /path/to/stella_libretro.so build` (requires build/rc2-baseline exact RC2 ROM/symbols); `python tests/stella_libretro.py --help`. See CI for full build, baseline and repeat. No independent/hardware/human claims.
