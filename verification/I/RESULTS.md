# VERIFICATION I — independent evidence, 2026-11-28
Disposition: VERIFICATION_INCONCLUSIVE for complete product integration/release. LAB D strongest bounded technical candidate; RC3 remains official. No production changes, no merge/release.

Frozen RC3 f4c3a0ffd39373f1ed2a7b6cdaab7287e8a180a6; LAB D 72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3.
- RC3 NTSC 6facbb074765f32d5ca4416beb50acfdbfc8b9b418855152ae81c722494f0b06; PAL d1fd128b07d507a034f2f61cd4acf7ef1c4607c7e476c4d61503ccf3a641af49.
- D NTSC 09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c; PAL ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274.
- 4/4 exact native DASM ROMs twice, matching downloaded Drive bytes. Initial CI failure missing SDL2 resolved in verification workflow, run 46126980911 successful. Gopher v0.55.0 600-frame video repeat per ROM, 2 success/0 fail per candidate. Not Gopher gameplay differential.
- Stella 6.7.1: independent fresh RC3/D same-ROM repeat 6000 callbacks per TV per run; all A/B pixel/projected RAM/raster/PCM match. 100000 A/B callbacks per TV, 99999 complete, all 100 block hashes and PCM/input hashes match. Additional original-core stress D 30375 NTSC/30045 PAL active; combined long campaigns 260351 active D frames. Million active per TV not reached.
- RC3, D, B each 524/524 forced +12/12 natural regression cases. RC2 historical held SELECT bug reproduced, corrected in RC3/D/B. New 896/896 forced graphical comparisons per TV, and 60500/60500 sampled visible TIA writes per TV exactly match in register/data/order/line/clock; 181 audio writes total match.
- Bank crossings 6->4/frame; allocated RAM 97->91; stack 8B observed both; direct alias CFG no undef read; zero observed nonstack runtime writes DB-E7/E8-FF for D in 105992 instrumented frames per TV after boot. No all-path effective-address/alias-read proof, no global WCET, no physical/human tests. New six bytes remain reserved.
- B exact archived fallback ROMs tested but no independent clean native B build/Gopher. No new reproduced product defect; absence not proven.

Full evidence archive and six separately labelled ROMs, scripts, raw results, bank hashes, matrices, traces, WAV/MP4, handoffs and RESTART:
https://drive.google.com/drive/folders/1H7rRc0IgfCJfyQhrGhuaXlX0zDCyDc8R
ZIP: https://drive.google.com/file/d/1DFQeNMbbLCVMj_wYJzKSSlCmIagYfFdf/view — SHA256 d84a5a07cdc08ff26aa2ef413fe1b011f0e73e5ef4a6d850647304d1886364fe, 12756170 bytes, 671 manifest entries. Re-downloaded ZIP and six ROMs verified by SHA256.
Report: https://docs.google.com/document/d/1npWGbPIGFkJ25usuMQHBNxpGKMpTQGcw/edit
MAIN handoff: https://docs.google.com/document/d/1Sm9A0qBsGBNonSINeKmljJNl7kdeHOm3/edit
CI: https://github.com/Odourman/SLUICE-PANIC/actions/runs/46126980911
CI artifacts 15256131168 RC3; 15255634146 D. No product merge authorized.
