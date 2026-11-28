# SLUICE PANIC! – GRAPHICS II – RC5 diagnostic R4B
2026-11-28. **GRAPHICS_DIAGNOSTIC_R4B_DELIVERED / NATIVE_BUILD_PASS / STELLA_BOUNDED_PASS / GOPHER_REGRESSION_PASS / DIRECT_RASTER_AND_INDEPENDENT_VERIFICATION_PENDING.** Recommend MAIN II accept R4B as diagnostic design reference, not a playable product or release gate. RC4 remains frozen, no production integration, bonus rule, release or merge authorized.

## Identity and provenance
- RC4 frozen authority: `cef328950e82a86b104cb05226f6f6e02d170553`.
- R3 starting branch HEAD: `46bea8f7d9a1583207804f3d6bb6c09780916184`; R3 source ZIP SHA-256 `2994206d6faa5bd934c4e59445b2c9d9c1164b795d498b6d4237cd2cd7ba49af`.
- R4A CI `46150909213`, commit `35b21c198d6adebc3b4d038d73710620add4a838`; evidence SHA-256 `8e443764847ea7e94d1aeaf80369dac00c5dbbfff26e085d299f8385780c8ed6`. R4A retained, not final recommendation.
- R4B source/evidence build commit `5e4b63ca3606a06d610f4178d63c24390e83f089`, Actions `46151252807`; [source](https://github.com/Odourman/SLUICE-PANIC/tree/5e4b63ca3606a06d610f4178d63c24390e83f089/graphics/RC5), [CI](https://github.com/Odourman/SLUICE-PANIC/actions/runs/46151252807).
- R4B source ZIP SHA-256 `06a7bb4595d8d1440c8f54ce272f639117cef6cef88d0768f719d35bc9350be8`. Evidence ZIP SHA-256 `e126963dc0ef127d181db58370e48871156222bae2c1f7508c220dbb16950007`, 603 manifest entries verified locally. Native build artifact `15266240653`; full evidence artifact `15265952570`.
- NTSC 16384 bytes SHA-256 `9d5d9c573d763ac170d37a71ddfa48df4afe783d66e08cae4bdd9269fa0c8495`; 4096-byte bank SHA-256 `f6b74b75e1dc35c7a2aeda272c58ecbb386193312470a09f13daffc1d7c7a3ec`.
- PAL 16384 bytes SHA-256 `fff2fd59c190d399e4b86cd84e274f2805b9a28e0b8d54532bdc8fac9f0a0065`; bank SHA-256 `12ecdd9476ea795a4931098bcf982c83a760edf19fd763aeace0b3cc76a52a57`.

## Findings and correction
R3 PAL was corrupted in earlier captured images. Fresh, separate processes on the same exact R3 ROMs displayed both correctly. R3 isolated control `46150678660` has an unsuccessful overall CI disposition because Gopher could not start with the runner ABI; isolated Stella captures succeeded, reproduced exact R3 ROM hashes, and are preserved. The prior in-process sequence and capture implementation changed together in this control. Thus corruption is localized to emulator/process/capture chain, not established to a specific libretro internal cause; no ROM change was needed to restore R3 PAL display. R4B final uses isolated processes, pitch-aware RGB conversion and verifies equality of manual and Pillow conversions on final framebuffer in each region. The Gopher dynamic linking failure was corrected with SDL2 dependencies and Ubuntu 24.04 (22.04 lacked required GLIBC/GLIBCXX versions). Failed runs preserved.

R4 corrects title/BEST/final score spacing and adds BEST label to both title modes; retains fixed illustrative values, not live scores. R4B changes only water palette constants relative to R4A (lower maximum luminance 8 to 6; minimum 6 to 4). Original fish, octopus, bomb, keeper and burst artwork unchanged. Four diagnostic replays cover six fish colors and four water colors; selection is fixed by replay/lane, not random gameplay spawn. Keeper changes pose by stage. Progressive gate removal and broken rail fragments implemented in diagnostic (not full physical gate-collapse animation as in design mockups). No new game mechanics.

## Actual evidence
DASM 2.20.14.1 package: two native builds per region, banks byte-identical, full F6 images are four identical banks; no switching in standalone diagnostic. CPU subset execution on actual native bytes: 4200 frames per region, 262/312 lines at every modeled frame, max 73/76 cycles from WSYNC release, two stack bytes, no modeled overruns. 16 local diagnostic RAM bytes $80–$8F plus stack; these are NOT permissions to allocate product RAM. The six text tables have page-aligned bases F600–FB00, 101 bytes each. Last data end at FB65 exclusive, leaving F6 hotspot/vector region intact; this is not proof of spare space in RC4.

Actual Stella 8.0_pre ca1371c, core SHA-256 `05b289b979f1640b454854c06c0b8dd86cc8559c9a684bc08c9edb8ea4ba1ac4`: 4200 video callbacks and 4200 input polls per region; four replay modes, all eight stage IDs observed, 264 native sampled PNGs per region. Video geometry: 160×228 NTSC and 160×274 PAL callbacks, including blanking/crop; core reports nominal 60/50 fps. The output contains native PNGs, pitch and raw hashes and sampled GIFs. GIF/MP4 are derived from actual Stella callback frames, resized nearest-neighbor and sampled every fourth frame, not recordings of playable gameplay. R4B text verification: 72 screenshots per region (both title variants, persistent Game Over); exact 160×192 text mask comparison with generated 40-column PF data repeated 4 horizontal clocks and 6 scanlines per row, offsets 14 NTSC/35 PAL. All 144 screenshots matched, zero differing thresholded pixels (4,423,680 compared pixels). This is a bounded pixel audit, not exhaustive visual proof of every object frame. Actual PNG phase sampling in artifact covers phase 0/2; animations are present in GIFs, but do not claim exhaustive per-phase native still proof.

Gopher2600 v0.55.0: two 1180-frame video regression records and reruns, 2 success / 0 fail. This proves repeatable visual digest in that emulator, not independent pixel equality against Stella or physical hardware. Supplemental headless STEP FRAME attempt executed, FRAMEINFO unsupported in this version; no direct emulator scanline measurement obtained. Nominal FPS and callback height are NOT direct scanline evidence. CPU model raster results are explicitly separate. No independent verification or real hardware test performed.

## Contrast review (actual sampled RGB)
Selected stage-1 frames away from gate (tick mod 64 < 48); per lane interior crop, dominant RGB background and next most frequent object color, third color for fuse. Rec.601 luma Y'=0.299R+0.587G+0.114B; minimum absolute difference across samples, scale 0–255. This is an illustrative grayscale contrast measure, not WCAG or hardware palette certification.

| Region | Object | R4A min | R4B min |
|---|---|---:|---:|
| NTSC | Fish |21.4|49.8|
| NTSC | Octopus |18.2|45.1|
| NTSC | Bomb body |117.4|90.6|
| NTSC | Fuse |13.0|39.8|
| PAL | Fish |60.6|93.3|
| PAL | Octopus |71.5|103.4|
| PAL | Bomb body |110.8|75.7|
| PAL | Fuse |7.6|22.8|

Both regions sampled six fish RGB colors and four water RGB colors. R4B preferred because lowest fish/octopus/fuse contrast improves; bomb body contrast decreases but remains clearly separated in samples. NTSC actual water is green/teal, PAL magenta/purple under this Stella palette; not identical regional hue. PAL black appears near-black (7,7,7) through emulator palette; register body value is $00. Fuse remains grayscale except deliberate spark color. No promise of absolute physical TV hue. The diagnostic has one fixed lane per object kind in swimming stage, then prescribed local destruction and chain sequence. Future product integration must prove all reachable palette combinations, object widths, overlapping/collision behavior, stable per-spawn random colors, all phases, real input/gameplay, and actual production kernel timing.

## Final disposition and handoffs
DASM_REPRODUCIBLE_PASS; STELLA_PASS bounded actual visual samples; GOPHER2600_PASS bounded deterministic regression; NTSC_VISUAL_PASS and PAL_VISUAL_PASS for inspected diagnostic stages/text/contrast, not every pixel/frame. GRAPHICS_DIAGNOSTIC_R4_READY only as R4B diagnostic design handoff. Unresolved: exact internal PAL capture fault, direct emulator raster measurement, exhaustive phase/pixel and physical checks. MAIN II must authorize any production integration separately. Preserve RC4 and all failed attempts. ROM DEVELOPMENT V and VERIFICATION II handoffs attached. No changes to score/bonus semantics, no gameplay integration, no released RAM allocation.


Complete Drive package: https://drive.google.com/file/d/1xXWxZ9unFqj3XDnxHkOhf2PIkQzOYu1W/view
