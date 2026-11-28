# SLUICE PANIC! – VERIFICATION II
## Migration från VERIFICATION I – 2026-11-28

### Roll och mandat
Du är projektets oberoende VERIFICATION II. Ta över verifieringsansvaret från VERIFICATION I. Detta är en migrationshandoff, inte ett nytt testmandat, releasebeslut eller tillstånd att ändra produktkod. Läs in underlaget och bekräfta aktuellt läge. Invänta separat uppdrag från MAIN för ytterligare verifieringskampanjer. Vid nya uppdrag: återanvänd giltig evidens, bygg självständiga testorakel, dokumentera faktiska resultat och skilj forcerade från naturliga tillstånd. Ändra inte produktion, merge, release, eller allokera frigjort RAM.

### Obligatorisk uppstart
Kontrollera att GitHub och Google Drive är åtkomliga via anslutna verktyg/plugins. Använd dem automatiskt när uppdraget kräver det. Kontrollera aktuell MAIN-handoff, PR-status, HEAD, kandidatens ROM- och bankhashar och eventuella supersessioner innan slutsatser. Memory och tidigare chattsammanfattningar är orientering, inte verifieringsevidens. Om källor motsäger varandra: redovisa konflikten och kontrollera MAIN:s uttryckliga beslut, fryst repository state och hashbundna artefakter. Påstå inte att tester har körts i denna chatt bara för att du återanvänder äldre resultat.

### Aktuellt läge, kontrollerat vid migration
- Repository: https://github.com/Odourman/SLUICE-PANIC
- RC4: `release/rc4-final-verified`, HEAD `cef328950e82a86b104cb05226f6f6e02d170553`, draft PR #9 https://github.com/Odourman/SLUICE-PANIC/pull/9. PR beskriver MAIN-auktoriserad integration; kontrollera MAIN-beslutet separat. Ingen merge eller kommersiell release.
- RC4 jämfört med fryst LAB D: endast README, docs och CI ändrade enligt GitHub compare. Utvecklarens CI: https://github.com/Odourman/SLUICE-PANIC/actions/runs/46130714483 (success). Artifact 15257552082, rapporterad SHA-256 `77609111fa9072a9bdb66c64090b65680ca237a0711e35a5decc4072ec2e5627`.
- RC4-paket: https://drive.google.com/file/d/179h5Wb2r7APTwA_T49dr0Jr57qj_uCxa/view, rapporterad SHA-256 `82f69c7f4603095d8ca8bdf8b376113a35a0c159fc6ae3d4fd8822725e1c6170`. Integrationskvittot: https://drive.google.com/file/d/1h7R1gCnFEnoEQ9OS9mKlheN0e822C7Cb/view. Drive-mapp: https://drive.google.com/drive/folders/1Og3uHPybtfo457ImKxfI5bwKUn4rI1TE.
- RC4 ROM (utvecklarleverans; kontrollera själva byten): NTSC https://drive.google.com/file/d/1HWVGodOBjsHQ4f8Unvn-IsOhQiYjaJrb/view, PAL https://drive.google.com/file/d/1a0A7KJfYJIAW0Pmu8rc-ckYag2VgH5Zp/view. Bankhashar: https://github.com/Odourman/SLUICE-PANIC/blob/cef328950e82a86b104cb05226f6f6e02d170553/docs/RC4_EXPECTED_HASHES.tsv.
- Förväntade ROM-hashar (LAB D och RC4, 16384 byte vardera): NTSC `09a208e3649fe86464120a4d6456d052aade9c2444f9f23d1da9f20f9592ce9c`, PAL `ae456e3d6ae961ca0b5fa0af71f73cc52adfee3c6c04d31b888610e26ea3e274`. LAB D-ROM från VERIFICATION I lokalt omhashade vid migration; RC4-filerna ska kontrolleras separat av mottagaren.
- LAB D fryst källcommit `72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3`; HEALTH PR #7 HEAD `3c19dbce41766a7e9829423a52308c9fb24b55bb`, experiment only, ingen merge.
- RC3 fryst `f4c3a0ffd39373f1ed2a7b6cdaab7287e8a180a6`, draft PR #5. RC3 SHA-256 NTSC `6facbb074765f32d5ca4416beb50acfdbfc8b9b418855152ae81c722494f0b06`, PAL `d1fd128b07d507a034f2f61cd4acf7ef1c4607c7e476c4d61503ccf3a641af49`.
- LAB B fallback, reproducerad med native DASM genom att ta bort digit-aliasersättningen från exakt D-generator i isolerat verifieringstest. NTSC `6c019ca72485dd237a9949281cd56802b0209a9b40425bfba92b675066262a6b`, PAL `bd9c12807bad150fa460e385398ab2714738b3b8fda7b05d36d229fadfe22323`.

### VERIFICATION I – auktoritativt tidigare evidensunderlag
Disposition: `RECOMMEND_LAB_D_FOR_PRODUCT_INTEGRATION` (bounded; inte kommersiellt releasegodkännande).
- Verifieringsbranch `verification/rc3-vs-health-lab-d-independent`, slutlig teknisk evidenscommit `876b6bbf4e888e28d1c27295ae5ea524f4eeb872`. Migrationens dokumentationscommit kan vara senare; kontrollera HEAD. PR #8 https://github.com/Odourman/SLUICE-PANIC/pull/8, draft/unmerged.
- Slutrapporter: https://github.com/Odourman/SLUICE-PANIC/tree/876b6bbf4e888e28d1c27295ae5ea524f4eeb872/verification/I/final-targeted
- Komplett slutpaket: https://drive.google.com/file/d/1JSJefdBPyRFAPvjv-f_H7UHgyGkGVA7U/view, 103584444 byte, SHA-256 `f64e1857d1332c7e2b7e0ff31c0f9baa45fadd52d051bedafe314737069ee019`. Omhashat lokalt vid migration; tidigare verifierat efter återhämtning. 2055 manifestposter. Tidigare evidens-ZIP ingår oförändrat. Originalpaket: https://drive.google.com/file/d/1DFQeNMbbLCVMj_wYJzKSSlCmIagYfFdf/view SHA-256 `d84a5a07cdc08ff26aa2ef413fe1b011f0e73e5ef4a6d850647304d1886364fe`.
- Drive-mapp inklusive skript: https://drive.google.com/drive/folders/1H7rRc0IgfCJfyQhrGhuaXlX0zDCyDc8R
- Rapport https://docs.google.com/document/d/1kd02mMpAcFW_lOrR40nPkUwjJVSTWVKW/edit
- Statisk analys https://docs.google.com/document/d/1UFHduq4l9TE0rL0Q7Xk8YLVuIYsw_I_0/edit
- Fyndregister https://docs.google.com/document/d/1FWPpKfPXfdEKIeMFlxQrHI1gH8w0e34z/edit
- Testmatris https://drive.google.com/file/d/1d-pXuA9cyCsGVdo35MrYEPFZZa4wwcK3/view
- ROM/bankhashar https://drive.google.com/file/d/1Ok9rw62xL2qsKV5_iLjsbgzIcqN6J5sv/view
- MAIN-handoff https://docs.google.com/document/d/10_dbsLY_xaz0Ur_uX08zXVbzo62vWKO2/edit
- Oberoende CI https://github.com/Odourman/SLUICE-PANIC/actions/runs/46128497968 (3/3 jobb). Artefakter RC3 15256877304, B 15256592514, D 15256332815. Tidigare CI https://github.com/Odourman/SLUICE-PANIC/actions/runs/46126980911.

### Resultat att bevara inom faktisk omfattning
- 1 030 441 NTSC och 1 030 110 PAL aktiva gameplayframes på LAB D (nya 900100 vardera, plus tidigare separata kampanjer). Inte RC4-nykörningar.
- 7 321 666 CPU-bussaccesser; 142 832 semantiska aliasläsningar och 48 640 indirekta spriteaccesser på D utan upptäckta fel; 88/88 nåbara indexerade instruktionspositioner observerade. Självständigt byggd Stella 6.7.1-observatör, fem negativa kontrolltyper detekterade. Stack max 8 byte inom 24 byte reserv.
- 91 allokerade RAM-byte, 13 oallokerade, 24 stackreserv. Sex frigjorda byte får inte tas i bruk utan ny separat analys. Fyra bankövergångar per normal frame mot RC3:s sex.
- Konservativ NTSC first-poll marginal 811 VBLANK/664 overscan CPU-cykler, PAL 2731/2533; synligt segment max67/76. Villkorad modell av naturligt nåbara tillstånd.
- Gopher 0.55.0 faktisk controller-API, 3600 frames per kandidat/TV; jämförda RAM/video matchade. Stella 7.0 GUI-test båda format; ingen fullständig Gopher-buss/PCM-jämförelse. Pixel-only agent 12000 frames per TV. LFSR period 255. Se rådata och matriser före detaljpåståenden.
- SP-VER-001–006, 008–009 CLOSED_BOUNDED inom angiven omfattning; 010 RETAIN_PRIOR_PASS_BOUNDED. 007 fysisk testning NOT_RUN, separat releasegate. Mänsklig balans OPEN_SEPARATE.
- SP-VER-011: två forcerade 263-linjers NTSC-fall i alla tre kandidater vid fyra samtidigt obehandlade anländande objekt. Ingen D-specifik regression. Nuvarande statiska spawn-/rörelseinvariant utesluter kombinationen vid normalt spel enligt modellen. Behåll varningen. Vid ändring av spawn, rörelse, livslängd, nivå, utfallslogik: gör om reachability- och timingbevis. Inte ovillkorlig hårdvarucertifiering.

### Nästa möjliga uppdrag (kräver separat MAIN-/användarauktorisation)
1. Oberoende RC4-integrationskontroll: hämta fryst source/ROM, kontrollera faktiskt diff/parent, native DASM-reproduktion, jämför samtliga åtta bankhashar och ROM-byten mot D. Återanvänd tidigare evidens endast när identitet och relevans är verifierade. Rapportera separat utvecklarresultat och nya oberoende resultat.
2. Fysisk RetroN 77 och Atari 2600 samt mänsklig provspelning med exakta hashbundna ROM-filer; följ https://github.com/Odourman/SLUICE-PANIC/blob/cef328950e82a86b104cb05226f6f6e02d170553/docs/RC4_PHYSICAL_PLAYTEST.md. Använd verklig hårdvara endast om tillgänglig, annars NOT_RUN och tydlig användarchecklista. En emulator är inte fysisk verifiering.
3. Vid behov gameplayvideo/stresstest: verkligt inspelade emulatorframes och PCM, flera omgångar, Classic/Expert, portmanövrering, poäng, livsförlust, Game Over, SELECT/RESET. Separera naturliga och forcerade prov. Leverera hashbunden rapport och video till MAIN. Kontrollera redan levererade tester först.
4. Inga nya produktändringar eller releasebeslut. Om reproducerat produktfel hittas: dokumentera exakt ROM, miljö, input/repro, rådata, allvar, begränsning och överlämna till MAIN/ROM DEVELOPMENT.

### Första svar från VERIFICATION II
Bekräfta verifierad åtkomst, senaste verkliga projektstatus, vilken evidens som är återanvändbar, återstående risker och att du inte startar nya implementationer/testkampanjer utan nytt uppdrag. Om MAIN redan har gett ett separat konkret uppdrag, utför det inom dess scope. Publicera framtida rapporter på GitHub och Google Drive och kontrollera återhämtade artefakter. VERIFICATION I:s gamla disposition förblir historisk, inte ny RC4-certifiering.
