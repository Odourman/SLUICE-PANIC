# Grafiska tillstånd
|Tillstånd|Bildkontrakt|
|---|---|
|Titel/start|Ingen separat titel eller logotyp; ready visar 000000, 3 liv, 2 blå lanes, vakt i 0, inga objekt; portmask från spelstate|
|Gameplay 2/3/4|Alla fyra lanes syns, aktiva blå, inaktiva mörka; en P1 per aktiv lane, vakt i vald lane|
|Alla öppna/stängda/blandat|ENABL caps / hel port enligt 4-bitars mask; alla 16 kombinationer|
|Last passerar korrekt|Låda till höger om port, gul port + kant kort|
|Last stoppas felaktigt|Cargo_hit vid x112, röd port/kant, vakt error, ett liv bort enligt regler|
|Bråte stoppas korrekt|Debris_hit vid x112, gul port/kant, sedan bort|
|Bråte passerar felaktigt|Gren fortsätter till x128, röd port/kant, errorpose, liv bort|
|Förlorat liv|Errorpose, uppdaterat liv; ingen helskärmsblinkning|
|Återstart efter förlorat liv|Normalpose, inga objekt i illustrativ första frame, verklig state från ROMDEV|
|Felfri omgång/bonus|Gul poäng, uppdaterad score; inga extra symboler|
|Nivåövergång|Aktiv lane ändras till blå; ingen extra skärm|
|Game Over/slutpoäng|Röd sexsiffrig score, 0 liv, inga objekt eller vakt, portar kvar|
|Återstart|Ready-kontrakt, normal färg|
|Attract|Utelämnat|
|Reset|Samma visuella kontrakt som ready; faktisk resetlogik ej del av GRAPHICS|
|Pause|Utelämnat, ej del av grundregler|
|Rekordvisning|Utelämnad|
Händelser sammansätts utan att ändra spelreglerna. Ingen påstådd final ROM-implementation. Mockupfiler är representativa frames; JSON och regler definierar alla kombinationer.
