'''
Finds the levels for a given object and offset that have non-zero values
This helps see how the game uses/modifies the values
Note that this relies on the data within the set files in the folder provided
'''

import struct
import os.path as osp
import json
from binascii import hexlify
import sys
import os
import csv

if not len(sys.argv) == 2 and not len(sys.argv) == 6:
    print("script <billy/folder/path>")
    exit(0)

def prettyprint(obj,ene,cam,design):
    headers = ["ID", "Param", "Hex Value", "Dec Value", "Filenames"]
    ignoredKeys = ["ID", "X pos", "Y pos", "Z pos", "X rotation", "Y rotation", "Z rotation"]

    with open('offsetusage.csv','w',newline='',encoding='utf-8') as file:
        output = csv.writer(file)
        
        def printDict(dictName, dict):
            output.writerow([f"{dictName} Offsets"])
            output.writerow(headers)

            reverse_mapping = {}
            for key, values in dict.items():
                for value in values:
                    filename, val1, val2 = value
                    if (val1, val2) not in reverse_mapping:
                        reverse_mapping[(val1, val2)] = []
                    reverse_mapping[(val1, val2)].append(filename)

            for key, values in dict.items():
                if key[1].replace(invisibleSpace, "") in ignoredKeys:
                    continue

                unique_values = set((val1, val2) for filename, val1, val2 in values)
                for val1, val2 in unique_values:
                    filenames = reverse_mapping[(val1, val2)]
                    output.writerow([key[0], key[1], val1, val2, ', '.join(filenames)])

            output.writerow("")     
    
        printDict('Object', obj)
        printDict('Enemy', ene)
        printDict('Camera', cam)
        printDict('Design', design)

def getParameter(sizes, offset):
    total = 0
    ind = 0
    for ind in range(len(sizes)):
        total += sizes[ind][0]
        if total > offset:
            return sizes[ind][1]
    return "Out of Bounds"

#setID = sys.argv[3]

obj = {}
ene = {}
cam = {}
design = {}
invisibleSpace = '\u200B'

for filename in os.listdir(sys.argv[1]):
    if not filename.endswith('.bin') or not filename.startswith('set'):
        continue
	
    # What type of object are we parsing
    if 'ene' in filename:
        struct_type = 'enemy'
        struct_size = 80 # size in bytes of 1 enemy
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 , invisibleSpace * 1 + 'ID'),
                (4 , invisibleSpace * 2 + 'X pos'),
                (4 , invisibleSpace * 3 + 'Y pos'),
                (4 , invisibleSpace * 4 + 'Z pos'),
                (1 , invisibleSpace * 5 + 'Offset 0x10'),
                (1 , invisibleSpace * 6 + 'Offset 0x11'),
                (1 , invisibleSpace * 7 + 'Offset 0x12'),
                (1 , invisibleSpace * 8 + 'Offset 0x13'),
                (1 , invisibleSpace * 9 + 'Offset 0x14'),
                (1 , invisibleSpace * 10 + 'Offset 0x15'),
                (1 , invisibleSpace * 11 + 'Offset 0x16'),
                (1 , invisibleSpace * 12 + 'Offset 0x17'),
                (1 , invisibleSpace * 13 + 'Offset 0x18'),
                (1 , invisibleSpace * 14 + 'Offset 0x19'),
                (1 , invisibleSpace * 15 + 'Offset 0x1A'),
                (1 , invisibleSpace * 16 + 'Offset 0x1B'),
                (1 , invisibleSpace * 17 + 'Offset 0x1C'),
                (1 , invisibleSpace * 18 + 'Offset 0x1D'),
                (1 , invisibleSpace * 19 + 'Offset 0x1E'),
                (1 , invisibleSpace * 20 + 'Offset 0x1F'),
                (1 , invisibleSpace * 21 + 'Offset 0x20'),
                (1 , invisibleSpace * 22 + 'Offset 0x21'),
                (1 , invisibleSpace * 23 + 'Offset 0x22'),
                (1 , invisibleSpace * 24 + 'Offset 0x23'),
                (1 , invisibleSpace * 25 + 'Offset 0x24'),
                (1 , invisibleSpace * 26 + 'Offset 0x25'),
                (1 , invisibleSpace * 27 + 'Offset 0x26'),
                (1 , invisibleSpace * 28 + 'Offset 0x27'),
                (1 , invisibleSpace * 29 + 'Offset 0x28'),
                (1 , invisibleSpace * 30 + 'Offset 0x29'),
                (1 , invisibleSpace * 31 + 'Offset 0x2A'),
                (1 , invisibleSpace * 32 + 'Offset 0x2B'),
                (1 , invisibleSpace * 33 + 'Offset 0x2C'),
                (1 , invisibleSpace * 34 + 'Offset 0x2D'),
                (1 , invisibleSpace * 35 + 'Offset 0x2E'),
                (1 , invisibleSpace * 36 + 'Offset 0x2F'),
                (1 , invisibleSpace * 37 + 'Offset 0x30'),
                (1 , invisibleSpace * 38 + 'Offset 0x31'),
                (1 , invisibleSpace * 39 + 'Offset 0x32'),
                (1 , invisibleSpace * 40 + 'Offset 0x33'),
                (1 , invisibleSpace * 41 + 'Offset 0x34'),
                (1 , invisibleSpace * 42 + 'Offset 0x35'),
                (1 , invisibleSpace * 43 + 'Offset 0x36'),
                (1 , invisibleSpace * 44 + 'Offset 0x37'),
                (1 , invisibleSpace * 45 + 'Offset 0x38'),
                (1 , invisibleSpace * 46 + 'Offset 0x39'),
                (1 , invisibleSpace * 47 + 'Offset 0x3A'),
                (1 , invisibleSpace * 48 + 'Offset 0x3B'),
                (1 , invisibleSpace * 49 + 'Offset 0x3C'),
                (1 , invisibleSpace * 50 + 'Offset 0x3D'),
                (1 , invisibleSpace * 51 + 'Offset 0x3E'),
                (1 , invisibleSpace * 52 + 'Offset 0x3F'),
                (1 , invisibleSpace * 53 + 'Offset 0x40'),
                (1 , invisibleSpace * 54 + 'Offset 0x41'),
                (1 , invisibleSpace * 55 + 'Offset 0x42'),
                (1 , invisibleSpace * 56 + 'Offset 0x43'),
                (1 , invisibleSpace * 57 + 'Offset 0x44'),
                (1 , invisibleSpace * 58 + 'Offset 0x45'),
                (1 , invisibleSpace * 59 + 'Offset 0x46'),
                (1 , invisibleSpace * 60 + 'Offset 0x47'),
                (1 , invisibleSpace * 61 + 'Offset 0x48'),
                (1 , invisibleSpace * 62 + 'Offset 0x49'),
                (1 , invisibleSpace * 63 + 'Offset 0x4A'),
                (1 , invisibleSpace * 64 + 'Offset 0x4B'),
                (1 , invisibleSpace * 65 + 'Offset 0x4C'),
                (1 , invisibleSpace * 66 + 'Offset 0x4D'),
                (1 , invisibleSpace * 67 + 'Offset 0x4E'),
                (1 , invisibleSpace * 68 + 'Offset 0x4F')
            ]
    elif 'obj' in filename:
        struct_type = 'object'
        struct_size = 64 # size in bytes of 1 object
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 , invisibleSpace * 1 + 'ID'),
                (4 , invisibleSpace * 2 + 'X pos'),
                (4 , invisibleSpace * 3 + 'Y pos'),
                (4 , invisibleSpace * 4 + 'Z pos'),
                (4 , invisibleSpace * 5 + 'X rotation'),
                (4 , invisibleSpace * 6 + 'Y rotation'),
                (4 , invisibleSpace * 7 + 'Z rotation'),
                (4 , invisibleSpace * 8 + 'Int Param 1'),
                (4 , invisibleSpace * 9 + 'Int Param 2'),
                (4 , invisibleSpace * 10 + 'Int Param 3'),
                (4 , invisibleSpace * 11 + 'Int Param 4'),
                (4 , invisibleSpace * 12 + 'Float Param 1'),
                (4 , invisibleSpace * 13 + 'Float Param 2'),
                (4 , invisibleSpace * 14 + 'Float Param 3'),
                (4 , invisibleSpace * 15 + 'Float Param 4'),
                (1 , invisibleSpace * 16 + 'Byte Param 1'),
                (1 , invisibleSpace * 17 + 'Byte Param 2'),
                (1 , invisibleSpace * 18 + 'Byte Param 3'),
                (1 , invisibleSpace * 19 + 'Byte Param 4')
            ]
    elif 'design' in filename:
        struct_type = 'design'
        struct_size = 64 # size in bytes of 1 design
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 , invisibleSpace * 1 + 'ID'),
                (4 , invisibleSpace * 2 + 'X pos'),
                (4 , invisibleSpace * 3 + 'Y pos'),
                (4 , invisibleSpace * 4 + 'Z pos'),
                (1 , invisibleSpace * 5 + 'Offset 0x10'),
                (1 , invisibleSpace * 6 + 'Offset 0x11'),
                (1 , invisibleSpace * 7 + 'Offset 0x12'),
                (1 , invisibleSpace * 8 + 'Offset 0x13'),
                (1 , invisibleSpace * 9 + 'Offset 0x14'),
                (1 , invisibleSpace * 10 + 'Offset 0x15'),
                (1 , invisibleSpace * 11 + 'Offset 0x16'),
                (1 , invisibleSpace * 12 + 'Offset 0x17'),
                (1 , invisibleSpace * 13 + 'Offset 0x18'),
                (1 , invisibleSpace * 14 + 'Offset 0x19'),
                (1 , invisibleSpace * 15 + 'Offset 0x1A'),
                (1 , invisibleSpace * 16 + 'Offset 0x1B'),
                (1 , invisibleSpace * 17 + 'Offset 0x1C'),
                (1 , invisibleSpace * 18 + 'Offset 0x1D'),
                (1 , invisibleSpace * 19 + 'Offset 0x1E'),
                (1 , invisibleSpace * 20 + 'Offset 0x1F'),
                (1 , invisibleSpace * 21 + 'Offset 0x20'),
                (1 , invisibleSpace * 22 + 'Offset 0x21'),
                (1 , invisibleSpace * 23 + 'Offset 0x22'),
                (1 , invisibleSpace * 24 + 'Offset 0x23'),
                (1 , invisibleSpace * 25 + 'Offset 0x24'),
                (1 , invisibleSpace * 26 + 'Offset 0x25'),
                (1 , invisibleSpace * 27 + 'Offset 0x26'),
                (1 , invisibleSpace * 28 + 'Offset 0x27'),
                (1 , invisibleSpace * 29 + 'Offset 0x28'),
                (1 , invisibleSpace * 30 + 'Offset 0x29'),
                (1 , invisibleSpace * 31 + 'Offset 0x2A'),
                (1 , invisibleSpace * 32 + 'Offset 0x2B'),
                (1 , invisibleSpace * 33 + 'Offset 0x2C'),
                (1 , invisibleSpace * 34 + 'Offset 0x2D'),
                (1 , invisibleSpace * 35 + 'Offset 0x2E'),
                (1 , invisibleSpace * 36 + 'Offset 0x2F'),
                (1 , invisibleSpace * 37 + 'Offset 0x30'),
                (1 , invisibleSpace * 38 + 'Offset 0x31'),
                (1 , invisibleSpace * 39 + 'Offset 0x32'),
                (1 , invisibleSpace * 40 + 'Offset 0x33'),
                (1 , invisibleSpace * 41 + 'Offset 0x34'),
                (1 , invisibleSpace * 42 + 'Offset 0x35'),
                (1 , invisibleSpace * 43 + 'Offset 0x36'),
                (1 , invisibleSpace * 44 + 'Offset 0x37'),
                (1 , invisibleSpace * 45 + 'Offset 0x38'),
                (1 , invisibleSpace * 46 + 'Offset 0x39'),
                (1 , invisibleSpace * 47 + 'Offset 0x3A'),
                (1 , invisibleSpace * 48 + 'Offset 0x3B'),
                (1 , invisibleSpace * 49 + 'Offset 0x3C'),
                (1 , invisibleSpace * 50 + 'Offset 0x3D'),
                (1 , invisibleSpace * 51 + 'Offset 0x3E'),
                (1 , invisibleSpace * 52 + 'Offset 0x3F')
            ]
    else:
        struct_type = 'cam'
        struct_size = 64 # maybe cam size...
        continue # skip for now

	# Read the set file
    with open(f"{sys.argv[1]}/{filename}","rb") as setfile:
        # Get filesize
        setfile.seek(0,2)
        fsize = setfile.tell()
        setfile.seek(0,0)
        
        while setfile.tell() < fsize:
            data = hexlify(setfile.read(struct_size)).decode("utf-8")
            byteSplit = [data[i:i+2] for i in range(0, len(data), 2)]
            
            hex_id = data[:8]
            dec_id = int(hex_id,16)
            if dec_id == 0:
                continue
            
            
            byte = 0
            i = 0
            while byte < len(byteSplit):
                value = byteSplit[byte:byte+struct_arg_sizes[i][0]]
                value = "".join(value)
                dec_value = int(value,16)
                if dec_value != 0 and byte < 56:
                    if struct_type == 'enemy':
                        t = (dec_id, getParameter(struct_arg_sizes, byte))
                        if t not in ene:
                            ene[t] = set()
                        ene[t].add((filename, value, dec_value))
                    elif struct_type == 'object':
                        t = (dec_id, getParameter(struct_arg_sizes, byte))
                        if t not in obj:
                            obj[t] = set()
                        obj[t].add((filename, value, dec_value))
                    elif struct_type == 'design':
                        t = (dec_id, getParameter(struct_arg_sizes, byte))
                        if t not in design:
                            design[t] = set()
                        design[t].add((filename, value, dec_value))
                    else:
                        if dec_id not in cam:
                            cam[dec_id] = set()
                        cam[dec_id].add(byte)
                
                byte += struct_arg_sizes[i][0]

# This is a tad ridiculous but whatever
prettyprint(obj,ene,cam,design)
# prettyprint(
#     sorted({k: sorted(v) for k, v in sorted(obj.items())}.items()), 
#     sorted({k: sorted(v) for k, v in sorted(ene.items())}.items()),
#     sorted({k: sorted(v) for k, v in sorted(cam.items())}.items()),
#     sorted({k: sorted(v) for k, v in sorted(design.items())}.items())
# )
