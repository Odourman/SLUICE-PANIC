#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p evidence/dasm
for tv in NTSC PAL; do
 dasm "asm/diagnostic_$tv.asm" -f3 -o"evidence/dasm/$tv.bin" -l"evidence/dasm/$tv.lst" -s"evidence/dasm/$tv.sym" > "evidence/dasm/$tv.log" 2>&1
 cmp "evidence/dasm/$tv.bin" "experimental_roms/SLUICE_PANIC_GRAPHICS_DIAGNOSTIC_$tv.bin"
done
sha256sum evidence/dasm/*.bin
