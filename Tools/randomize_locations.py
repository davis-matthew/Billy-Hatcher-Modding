'''
Randomly swaps the location bytes for objects and enemies within a set file.
Assumes that the objects/enemies are front-loaded (no 0 rows in between objects) into the set file.
'''

import struct
import os.path as osp
import json
from binascii import hexlify
import sys
import os
import csv
import ntpath
import random

if not len(sys.argv) == 2:
    print("script <set/file/path>")
    exit(0)

head, tail = ntpath.split(sys.argv[1])
filename = tail or ntpath.basename(head)

# What type of object are we parsing
if 'ene' in filename:
    struct_size = 80 # size in bytes of 1 enemy
elif 'obj' in filename:
    struct_size = 64 # size in bytes of 1 object
elif 'design' in filename:
    struct_size = 64 # size in bytes of 1 design
else:
    struct_size = 64 # maybe cam size...

with open(f"{sys.argv[1]}","rb") as setfile:
    data = bytearray(setfile.read())

locations = []
byte = 5
while byte < len(data):
    location = data[byte:byte+4]
    if location != bytearray([0x00, 0x00, 0x00, 0x00]):
        locations.append(data[byte:byte+4])
    byte += struct_size

random.shuffle(locations)

item = 0
byte = 5
while item < len(locations):
    data[byte:byte+4] = locations[item]
    byte += struct_size
    item += 1

with open(f"{sys.argv[1]}","wb") as setfile:
    setfile.write(data)

print("Randomized Locations!")
