# Animationer (grafisk tid, ej gameplaylås)
|ID|Rutor|NTSC frames|PAL frames|
|---|---|---|---|
|A01 idle|keeper_idle|obegränsat|obegränsat|
|A02 toggle|keeper_operate → idle|8|7|
|A03 move|idle i ny zon, ingen interpolering|1|1|
|A04 cargo pass|cargo, normal translation; port/kant bonusfärg|8|7|
|A05 debris stop|debris_hit, sedan borta; port/kant bonusfärg|8|7|
|A06 cargo error|cargo_hit; keeper_error; port/kant röd|20|17|
|A07 debris error|debris fortsätter, keeper_error; port/kant röd|20|17|
|A08 bonus|HUD gul, ingen blinkning|30|25|
|A09 level transition|ny lane byter mörk→blå, ingen fade|1|1|
|A10 game over|vakt borta, inga objekt, röd slutpoäng|tills restart|tills restart|
Händelsernas färg/pose är presentation, påverkar inte input eller spawnregler; vid samtidiga events prioriteras error framför success, game over framför allt. Om flera fel samtidigt: visa alla berörda lanes om timerbudget tillåter; annars senaste fel i en lane, global errorpose. GIF är illustration, inte exakt spelhastighet.
