# MAIN I → MAIN II — migration receipt (2026-11-28)

Status: RC4_ACCEPTED_PRODUCT_FROZEN / RC4_AUDIO_VISUAL_AUDIT_PASS_BOUNDED.
Product authority: release/rc4-final-verified @ cef328950e82a86b104cb05226f6f6e02d170553, PR #9 draft/unmerged. No product changes or merges authorized.
LAB D source 72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3; independent verification 876b6bbf4e888e28d1c27295ae5ea524f4eeb872. RC4 native build CI 46130714483.
NTSC SHA256 09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c
PAL SHA256 ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274
16KiB F6; 91 allocated, 13 unallocated, 24 reserved RAM bytes. No reallocation of six recovered bytes. Four normal bank transitions/frame. No new development without concrete defect and explicit scope.

## Durable migration
- [Drive migration folder](https://drive.google.com/drive/folders/1ZgmDPRpwnUpVB3kaTI2_Gbn-4L6UQ_G7)
- [MAIN II full startprompt](https://docs.google.com/document/d/1DUmnDGrNETDi3dz__e_SUag_TIsh9x7P/edit)
- [MAIN I AV audit report](https://docs.google.com/document/d/1YRtkUeQFE9mkJ11JVECA1y37Wro0exDW/edit)
- [Migration ZIP](https://drive.google.com/file/d/1AsxBzXoCeV9vhy11QUqHUM4V0eK_NFdS/view), 15861674 bytes, SHA256 708e46f9ab54ff6ac252eeaf8fcb51a0adf7ad23d1950f6799435958985de315; 11 payloads + SHA256SUMS.txt. Contains both untouched original GitHub recording archives (all eight MP4s, WAV tracks, inputs and samples), audit metrics JSON, visual crosscheck JSON, five visual exhibits, audit report and full migration prompt. Upload inventory and size checked. Combined MP4 from original gameplay chat is not included.
- [RC4 final ZIP](https://drive.google.com/file/d/179h5Wb2r7APTwA_T49dr0Jr57qj_uCxa/view)
- [RC4 manual](https://docs.google.com/document/d/1jTsQBCFABRi1PkDffyi8uvvPeEhygHuy/edit)
- [Physical protocol](https://docs.google.com/document/d/1WPBwEL7GxKc97Lf9ZtNqWYqLIzHiXG2U/edit)
- [Independent closure](https://github.com/Odourman/SLUICE-PANIC/tree/876b6bbf4e888e28d1c27295ae5ea524f4eeb872/verification/I/final-targeted)

## Recorded evidence and audit
Run 46131763934, recording branch verification/rc4-gameplay-video-20261128 @ 611ea0c19e6a4766d1a4c4623ba9f3382d5444c3. Both TV jobs success; only separate workflow added. Original artifacts 15257861774 NTSC and 15257647007 PAL; original SHA256 c3faaa9f346485f0d7db1b69226376ceea2f88b8c0dec30dbd31882b26fa9fb2 and fdbfe11326483f4d204d8b5ccfc4007f0144951a5d1c6b49c2344ef91f63b917 respectively, CRC and 44/44 manifest entries verified. 39600 callbacks, 39176 active, 40/40 restarts, 136 losses, zero logged invariant violations. MAIN analyzed 39592 decoded video frames and 45091616 PCM values; 39080 stable-active frames with no missing/duplicate keeper, black frame or HUD low-brightness flags; 652 keeper samples match, 2401 gate samples with 73 overlapping-object flags reviewed, no confirmed defect. Peak 20851/32767, zero clipped PCM, 24 sampled AAC windows no detected lag. No subjective listening, exhaustive pixel semantics or new raster proof. AV-001 one last frame missing from each MP4; AV-002 rescaling; AV-003 lossy codecs; AV-004 sparse RAM state logs; AV-005 no new raster proof. These are recording limitations. SP-VER-011 retained as shared forced-state 263-line NTSC warning; nonblocking under current reachability assumptions. No new confirmed product defect.

## Next phase
Read full MAIN II prompt and verify live sources and access to tools/plugins. Continue ART / PACKAGING & MANUAL, human playtest, physical RetroN77/original Atari testing, then separate release decision. Human subjective audio/balance and physical compatibility NOT_RUN. Commercial release NOT_AUTHORIZED. Preserve frozen ROM, no new RC5/HEALTH/PACHINKO absent concrete cause. This branch is documentation only; not for merge into production. User must open MAIN II chat and provide prompt; migration receipt does not create a chat.
