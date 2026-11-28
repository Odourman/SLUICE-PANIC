# RC4 freeze / version history / release checklist
MAIN 2026-11-28 authorizes exact LAB D integration only. RC1 4K; RC2 F6 Classic/Expert and session best; RC3 SELECT latch correction (PACH-RC2-001); RC4 = LAB D technical optimization: presentation folded into HUD and six-byte digit/lane alias, no new functionality. Keep RC1–RC3, LAB B/D, diagnostic and verification branches intact; no merge. RC4 branch only documentation and CI changes relative to LAB D. No embedded version number change.
- [ ] Integration gate: exact product source diff limited to docs and CI, two clean native builds and all expected ROM/bank hashes, compare actual Drive reference bytes separately.
- [ ] RC4 Stella and Gopher smoke tests successful; CI mandatory and not masked.
- [ ] Verify final artifact archive SHA and manifest; Drive readback.
- [ ] Original Atari 2600 physical test NOT_RUN (separate release gate).
- [ ] RetroN 77 physical test NOT_RUN (separate release gate).
- [ ] Human playtest NOT_RUN (separate release gate).
- [ ] MAIN commercial release authorization NOT_GRANTED.
SP-VER-011 accepted by MAIN as bounded robustness risk; no change. Status and actual pass evidence recorded in integration receipt/CI, not presumed by this checklist.
