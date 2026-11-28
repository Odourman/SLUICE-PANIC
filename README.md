# SLUICE PANIC! — RC4
Atari 2600 arcade score chase. The separate RC4 product branch integrates exactly the independently verified LAB D source at 72d2ca6fc6e8f2de96f4a1cb1b897d1e05b848c3, authorized by MAIN on 2026-11-28. Functionality frozen: no gameplay, graphics, audio or balance changes. RC4 acceptance requires the successful exact-hash integration workflow; no commercial release authorized.

## Build from repository root
Install Python 3 and native DASM; run `python tools/build_rc2.py build`. The historical generator name is retained intentionally. It creates both 16 KiB standard F6 ROMs plus four ASM banks, per-bank binary/listing/symbol/log files and bank_report.json. Run again from a separate clean source checkout and compare ROMs. Rename the output files externally, not inside the ROM. Expected hashes: [docs/RC4_EXPECTED_HASHES.tsv](docs/RC4_EXPECTED_HASHES.tsv). The original src/main.asm is an RC1 input, not the final standalone build.

## Documentation
[Game design](docs/GAME_DESIGN.md) · [Swedish manual](docs/RC4_PLAYER_MANUAL.md) · [Technical specification and known limitations](docs/RC4_TECHNICAL.md) · [Freeze and release checklist](docs/RC4_FREEZE.md) · [Physical playtest](docs/RC4_PHYSICAL_PLAYTEST.md) · [Handoffs](docs/RC4_HANDOFFS.md).
