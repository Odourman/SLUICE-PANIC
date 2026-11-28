# HEALTH I — EXPERIMENT ONLY — DO NOT MERGE

Frozen RC3: f4c3a0ffd39373f1ed2a7b6cdaab7287e8a180a6.
LAB D generator commit: 72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3.
ROM hashes (16,384 bytes F6 each):
- NTSC 09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c
- PAL ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274

Native DASM 2.20.14.1 built RC3 byte-identically. A: tail-call, B: local presentation, C: digit scratch alias, D: B+C. All isolated variants built and observed. D vs RC3: 97→91 allocated bytes; 24-byte stack reserve unchanged; 23976→15984 bank transitions per TV in 3996 instrumented frames; stack writes 65344→49360 NTSC, 65728→49744 PAL; min SP F7 unchanged. 4000/4000 symbol-projected state (91 bytes), framebuffer and raster equal per TV; PCM equal; visible beam histogram equal. First 40-line callback is boot partial; remaining 3999 lines count normal 262/312. 524 forced cases and 12 natural scenarios passed in real Stella 6.7.1; 24408 active agent gameplay frames. No new confirmed product defect. Timer polling differs. Legacy observer boundary does not establish newly freed DB-E0 write safety. No exhaustive timing/stack/liveness proof or physical hardware/Gopher new test. D is EXPERIMENT_ONLY and overall HEALTH_AUDIT_PARTIAL; B fallback; RC3 remains frozen.

Build from source root: python tools/build_rc2.py build. Use new generated symbols for all agents. Do not allocate newly free RAM without independent verification. Private research is not included. No merge or commercial release authority.
