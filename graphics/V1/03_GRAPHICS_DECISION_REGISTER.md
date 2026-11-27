# Beslut (GRAPHICS I, specialistfastställda)
|ID|Beslut|Motivering|
|---|---|---|
|SP-G01|Fyra 40-raders band, fast vatten|P1 kan återanvändas, tydlig separation|
|SP-G02|8×20 fysiska rader, 10 bytes/sprite|2-line kernel, tydliga former|
|SP-G03|Ball som port, PF symmetriska kanter|Undvik högerhalvs-PF-race i gameplay|
|SP-G04|Vakt x136, port x120, objekt x8–128|Separera vakt från transport|
|SP-G05|Sex siffror 3×5 PF-glyphs, tre livstaplar|Inga sprites krävs i HUD|
|SP-G06|Direkt start, ingen ROM-logotyp/attract|Lägre ROM-kostnad, autentiskt|
|SP-G07|Ingen avsiktlig flicker, inga dekorativa animeringar|Stabilitet|
|SP-G08|Normal NTSC 262, PAL 312 med 192 identiska synliga rader|Samma layout, separat färgtabell|
|SP-G09|Händelsefärg i port + kant, statisk pose|TIA-färgkoppling respekteras|
|SP-G10|Mjukvarukollision vid portgräns|TIA-latch är delad över zoner, risk för stale collisions|
|SP-G11|4 KB första mål, ingen bankväxling/extra RAM|Enkel arkitektur; ej bevisad fullspelbudget|
|SP-G12|Startmockup alla öppna, första två kanaler; ingen fastställd regel om initial mask|Illustrativ, MAIN avgör initiering|
