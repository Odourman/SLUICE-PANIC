# SLUICE PANIC! – RC4: inspelad gameplay och stresstest
**Handoff till MAIN | 2026-11-28 | PASS inom testad omfattning**

## Kandidat och reproducerbarhet
- Produktgren: `release/rc4-final-verified`, commit `cef328950e82a86b104cb05226f6f6e02d170553`.
- NTSC SHA-256: `09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c`.
- PAL SHA-256: `ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274`.
- Separat verifieringsgren: `verification/rc4-gameplay-video-20261128`, commit `611ea0c19e6a4766d1a4c4623ba9f3382d5444c3`. Endast en CI-workflow tillagd; ingen ändring av produktgren eller ROM-genererande kod.
- [CI-körning 46131763934](https://github.com/Odourman/SLUICE-PANIC/actions/runs/46131763934): båda matrix-jobben success; båda byggda ROM-hasharna matchade fryst RC4.
- Stella libretro 8.0_pre ca1371c; core SHA-256 `05b289b979f1640b454854c06c0b8dd86cc8559c9a684bc08c9edb8ea4ba1ac4`.

## Resultat
| TV | Scenario | Frames | Aktiva | Starter | Game over/omstart | Maxnivå | Maxpoäng |
|---|---|---:|---:|---:|---:|---:|---:|
| NTSC | Classic strategi | 5400 | 5385 | 1 | 0/0 | 23 | 22450 |
| NTSC | Expert strategi | 5400 | 5385 | 1 | 0/0 | 37 | 30475 |
| NTSC | Expert inputstress | 7200 | 7045 | 18 | 17/17 | 8 | 850 |
| NTSC | Classic förlust/omstart | 3600 | 3562 | 3 | 2/2 | 6 | 4775 |
| PAL | Classic strategi | 4500 | 4485 | 1 | 0/0 | 23 | 22350 |
| PAL | Expert strategi | 4500 | 4485 | 1 | 0/0 | 37 | 30475 |
| PAL | Expert inputstress | 6000 | 5860 | 19 | 18/18 | 8 | 450 |
| PAL | Classic förlust/omstart | 3000 | 2969 | 4 | 3/3 | 4 | 3550 |

Totalt: 8 scenarier, 39 600 emulerade frames och lika många videoframe-callbacks, 39 176 aktiva gameplayframes, 48 starter inklusive omstarter, 40 Game Over och 40 omstarter. 136 registrerade livsförluster. Inga brott mot de kontrollerade spelinvarianterna i något scenario. Max fyra samtidiga objekt i varje scenario. Båda spellägena observerades enligt avsikt. Alla klipp innehåller icke-tyst TIA-ljud (PCM peak 20851). Inga krascher observerades. Strategifallen gick utan livsförlust; Expert nådde nivå 37 i båda formaten.

## Metod och avgränsningar
Automatiserad state-aware strategi observerar RAM men skriver inte till RAM. Kontrollerna omfattar bland annat riktiga joystick-/Fire-inputs, snabba riktningsbyten, hållna knappar, motstridiga riktningar, slumpade kombinationer samt samtidiga Reset/Select/Fire i stresstestet. Avsiktlig förlust och återstart provas separat. Full inputlogg, RAM-stickprov, tillståndsövergångar, resultat-JSON, rå TIA-PCM och MP4 ingår i originalarkiven. Kontrollerade invariants är inte en fullständig kontroll av alla möjliga spelbuggar. Ingen oberoende ny scanline-/WCET-mätning, fysisk Atari/RetroN77-testning eller mänsklig balansbedömning. Tidigare SP-VER-011 kvarstår; detta test stänger inte den frågan. Inget påstående om verifierad mänsklig svårighetsgrad. Stickprov på bild från alla åtta videor granskades; hela sammanslagna filen maskinavkodades utan fel, men samtliga bildrutor har inte granskats visuellt.

## Leveranser och integritetskontroll
- [NTSC originalarkiv](https://github.com/Odourman/SLUICE-PANIC/actions/runs/46131763934/artifacts/15257861774), SHA-256 `c3faaa9f346485f0d7db1b69226376ceea2f88b8c0dec30dbd31882b26fa9fb2`.
- [PAL originalarkiv](https://github.com/Odourman/SLUICE-PANIC/actions/runs/46131763934/artifacts/15257647007), SHA-256 `fdbfe11326483f4d204d8b5ccfc4007f0144951a5d1c6b49c2344ef91f63b917`.
- Båda ZIP-filerna nedladdade; arkivhashar matchade GitHub; 44/44 manifestposter verifierade lokalt.
- Sammanfogad presentationsvideo: `SLUICE_PANIC_RC4_GAMEPLAY_STRESS_FULL.mp4`, 719,957 s, 21 090 827 bytes, SHA-256 `7cfd7c632393e8fd75500ab668e54f20bdb24ae3152d1031f8275ae467f835e8`. NTSC 0:00–6:00, PAL 6:00–12:00. Varje format: Classic strategi 0:00–1:30, Expert strategi 1:30–3:00, Expert stress 3:00–5:00, Classic förlust 5:00–6:00 (relativt formatets start). Omkodad visningskopia med scenariorubrik utanför spelbilden och PAL konverterad till 60 fps för sammanfogning. Originalen har NTSC 60 fps/PAL 50 fps. Varje original-MP4 är en frame kortare än emulatorns callbackantal, vid slutet, vilket stämmer med muxningens kortaste ström; ingen fullständig frame-exakt videoleverans påstås. Original-PCM bevarad.
- [PR #9](https://github.com/Odourman/SLUICE-PANIC/pull/9) är produktkandidatens befintliga samlingspunkt.

## Rekommendation till MAIN
Acceptera detta som kompletterande inspelad emulatorevidens för oförändrad RC4, inte som ny release eller ersättning för tidigare oberoende verifiering. Nästa steg är mänsklig playtest och vid behov fysisk konsoltestning. Inga ROM- eller produktändringar, ingen merge och ingen release utförd. Drive-kopieringen av CI-arkiven avvisades av connectorns filreferensvalidering; GitHub-arkiven och lokala filer finns tillgängliga. MAIN-chatten kan inte direkt adresseras från denna chatt; rapporten är avsedd för handoff dit.


## Migration supplement — 2026-11-28
The earlier Drive upload rejection is resolved. All four original delivery files plus VIDEO II start prompt have been uploaded and their Drive sizes checked. Original local SHA-256 values are retained; no new full byte-by-byte Drive download check claimed.
- Full video: https://drive.google.com/file/d/1kaK0lGNOL0u6qAVTR4iHoSwN1Dwz8dHl/view
- Original report: https://docs.google.com/document/d/1qq8tyaft7kL5aXdZZv22W8FOARqvfY8B/edit
- NTSC ZIP: https://drive.google.com/file/d/17kzvOwmxmerYgpAUz6W9klHOyh3yNZcQ/view
- PAL ZIP: https://drive.google.com/file/d/1DjvQ-P4i6qqKEtXjjHQ_ddDbHMlP1zLm/view
- VIDEO II: https://docs.google.com/document/d/1--oPPV0dOUO_NqQOUZSyUMk8Uku3cSAN/edit
