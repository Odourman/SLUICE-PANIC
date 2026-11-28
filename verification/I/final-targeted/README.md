# VERIFICATION I — final targeted closure

**RECOMMEND_LAB_D_FOR_PRODUCT_INTEGRATION** — bounded recommendation to MAIN only. RC3 remains official pending separate decision. No product code change, merge, release or new RAM allocation.

Frozen RC3 f4c3a0ffd39373f1ed2a7b6cdaab7287e8a180a6; D 72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3.

Complete evidence ZIP (including prior checkpoint, all scripts, raw bus traces, builds, reports and hashes): https://drive.google.com/file/d/1JSJefdBPyRFAPvjv-f_H7UHgyGkGVA7U/view — 103584444 bytes, SHA256 f64e1857d1332c7e2b7e0ff31c0f9baa45fadd52d051bedafe314737069ee019; 2055 manifest entries; redownloaded and exact hash verified.

Exact separate D ROMs: [NTSC](https://drive.google.com/file/d/1CC1Uwpf654qzUbnv_NHfsYoLiZqo4Ij9/view) 09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c; [PAL](https://drive.google.com/file/d/17zjzVnXrhu4tNz2rvKzNUd0tq13fjL_g/view) ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274. Both redownloaded and verified.

[Test matrix](https://drive.google.com/file/d/1d-pXuA9cyCsGVdo35MrYEPFZZa4wwcK3/view); [exact ROM and bank hashes](https://drive.google.com/file/d/1Ok9rw62xL2qsKV5_iLjsbgzIcqN6J5sv/view); [all evidence and scripts](https://drive.google.com/drive/folders/1H7rRc0IgfCJfyQhrGhuaXlX0zDCyDc8R).

[CI](https://github.com/Odourman/SLUICE-PANIC/actions/runs/46128497968): three jobs passed, RC3/B/D exact builds, Gopher controller gameplay and Stella 7 GUI. Artifacts RC3 15256877304, B 15256592514, D 15256332815.

New full CPU bus records 7321666, D 142832 alias semantic reads, 48640 indirect indexed accesses; 88/88 reachable indexed sites; five negative controls detected. Natural conditional WCET NTSC VBLANK/overscan margin 811/664 cycles, visible max 67/76. SP-VER-011 shared forced four-simultaneous-outcome 263-line NTSC case; excluded by current natural spawn invariant, preserve warning. New active frames 900100 per format; cumulative 1030441 NTSC / 1030110 PAL. Gopher 3600 frames per candidate/TV, recorded fields identical. LFSR255. Physical/human tests not run. Keep six freed bytes unallocated. See detailed reports and full hash-bound ZIP.
