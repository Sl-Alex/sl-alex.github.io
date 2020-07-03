#!/usr/bin/env python3
# Windows users: please add openscad to PATH

import os;
import sys;
import subprocess;

if len(sys.argv) < 2:
    sys.exit('Usage: %s [*.scad file]' % sys.argv[0])

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: file %s was not found!' % sys.argv[1])

bom_mark = "BOM_ITEM: ";

print("Generating BOM...");

scad_log = subprocess.check_output('openscad.exe -o preview.png --viewall --autocenter --imgsize=1920,1080 ' + sys.argv[1], stderr=subprocess.STDOUT).decode("utf-8");
pos = 0;

#print(scad_log);
print("Calculating...");

bom_list = {};

while (pos >= 0):
    pos = scad_log.find(bom_mark, pos);
    if (pos > 0):
        pos = pos + len(bom_mark);
        pos2 = scad_log.find("\"", pos);
        if (pos2 < 0):
            print("BOM item not found");
            continue;
        bom_item = scad_log[pos:pos2];
        cnt = 0;
        if (bom_item in bom_list):
            cnt = bom_list[bom_item];
        bom_list[bom_item] = cnt + 1;
        pos = pos2;

sorted_list = sorted(bom_list, key=str.casefold);

print("#########################");

for item in sorted_list:
    print(item + ': ' + str(bom_list[item]));

