import struct
import os.path as osp
import json
from binascii import hexlify
import sys


if not len(sys.argv) > 1:
	print("script [set_obj_level.bin]")
	exit(0)

setfn = sys.argv[1]
fmt = ">Ifff"
datalist = []

with open(setfn,"rb") as setf:
	setf.seek(0,2)
	fsize = setf.tell()
	setf.seek(0,0)
	while setf.tell() < fsize:
		currobj = {}
		print(filename)
		objid, x, y, z = struct.unpack(fmt,setf.read(0x10))
		if x == 0.0 and y == 0.0 and z == 0.0:
			break
		currobj["id"] = hex(objid)
		currobj["position"] = [x,y,z]
		currobj['extra'] = hexlify(setf.read(0x30)).decode("utf-8")
		datalist.append(currobj)
outfn = setfn[:-4] + ".json"
json.dump(datalist,open(outfn,"w"),indent=2)
print("IDs:")
print(list(set([o['id'] for o in datalist])))
print("done")