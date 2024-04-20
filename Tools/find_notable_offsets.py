'''
Finds the offsets within the bytes that are non-zero ignoring some values we already know
This will help indicate which offsets should be tested for behavior
Note that this relies on the data within the set files in the folder provided
'''

import struct
import os.path as osp
import json
from binascii import hexlify
import sys
import os
import csv

'''
Print each as:
dec_id/hex_id decoffsets/hexoffsets
'''
def prettyprint(obj,ene,cam,design):
    with open('usedoffsets.csv','w',newline='') as file:
        output = csv.writer(file)
        headers = ["Decimal Set ID", "Hex Set ID", "Decimal Notable Offsets", "Hex Notable Offsets"]
        
        output.writerow(["Object Offsets"])
        output.writerow(headers)
        for entry in obj: 
            output.writerow([entry[0],hex(entry[0]),entry[1],[hex(x) for x in entry[1]]])
        
        output.writerow("")
        output.writerow(["Enemy Offsets"])
        output.writerow(headers)
        for entry in ene: 
            output.writerow([entry[0],hex(entry[0]),entry[1],[hex(x) for x in entry[1]]])

        output.writerow("")
        output.writerow(["Camera Offsets"])
        output.writerow(headers)
        for entry in cam: 
            output.writerow([entry[0],hex(entry[0]),entry[1],[hex(x) for x in entry[1]]])

        output.writerow("")
        output.writerow(["Design Offsets"])
        output.writerow(headers)
        for entry in design: 
            output.writerow([entry[0],hex(entry[0]),entry[1],[hex(x) for x in entry[1]]])


if not len(sys.argv) == 2:
    print("script <billy/folder/path>")
    exit(0)

obj = {}
ene = {}
cam = {}
design = {}

for filename in os.listdir(sys.argv[1]):
    if not filename.endswith('.bin') or not filename.startswith('set'):
        continue
	
    # What type of object are we parsing
    if 'ene' in filename:
        struct_type = 'enemy'
        struct_size = 80 # size in bytes of 1 enemy
    elif 'obj' in filename:
        struct_type = 'object'
        struct_size = 64 # size in bytes of 1 object
    elif 'design' in filename:
        struct_type = 'design'
        struct_size = 64 # size in bytes of 1 design
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
            hex_id = data[:8].lstrip('0')
            if hex_id == '': # 00 00 00 00
                continue
            dec_id = int(hex_id,16) 
            
            byteSplit = [data[i:i+2] for i in range(8, len(data), 2)]
            for byte in range(len(byteSplit)):
                value = byteSplit[byte]
                offset = byte + 4
                if value == '00':
                    continue

                if struct_type == 'enemy':
                    if dec_id not in ene:
                        ene[dec_id] = set()
                    ene[dec_id].add(offset)
                elif struct_type == 'object':
                    if dec_id not in obj:
                        obj[dec_id] = set()
                    obj[dec_id].add(offset)
                elif struct_type == 'design':
                    if dec_id not in design:
                        design[dec_id] = set()
                    design[dec_id].add(offset)
                else:
                    if dec_id not in cam:
                        cam[dec_id] = set()
                    cam[dec_id].add(offset)
                

# The important offsets come out as: 
'''
{
   dec_id : [dec offset 1, dec offset 2, etc.]
}
'''

# This is a tad ridiculous but whatever
prettyprint(
    sorted({k: sorted(v) for k, v in sorted(obj.items())}.items()), 
    sorted({k: sorted(v) for k, v in sorted(ene.items())}.items()),
    sorted({k: sorted(v) for k, v in sorted(cam.items())}.items()),
    sorted({k: sorted(v) for k, v in sorted(design.items())}.items())
)

print("Created file usedoffsets.csv")