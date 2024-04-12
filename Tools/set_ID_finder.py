import struct
import os.path as osp
import json
from binascii import hexlify
import sys
import os

'''
This script looks through the set files of billy and sees all the IDs used of each type.
This is not necessarily the full set of IDs, but it at least gives a range.
This script also allows for lookups of the IDs.
'''

#TODO: probably could ask what type of ID they're searching for...
if not len(sys.argv) > 1:
	print("script <billy/folder> [id to find instances of] [ene/obj (default = all)]")
	exit(0)

class SetItem:
	def __init__(self, item):
		self.item = item
	def __eq__(self, other):
		return self.item['id'] == other.item['id']
	def __hash__(self):
		return hash(self.item['id'])
	def __str__(self):
		return self.item['id']
	def __repr__(self):
		return str(self)
	def __lt__(self, other):
		return int(self.item['id'],16) < int(other.item['id'],16)

isLookup = len(sys.argv) >= 3

obj = []
ene = []
design = []
locations = []

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
		continue # skip for now...

	# Read the set data
	with open(f"{sys.argv[1]}/{filename}","rb") as setf:
		setf.seek(0,2)
		fsize = setf.tell()
		setf.seek(0,0)
		while setf.tell() < fsize:
			currobj = {}
			objid, x, y, z = struct.unpack('>Ifff',setf.read(0x10))
			if x == 0.0 and y == 0.0 and z == 0.0:
				break
			currobj['file'] = filename
			currobj["id"] = hex(objid)
			currobj["position"] = [x,y,z]
			currobj['extra'] = hexlify(setf.read(struct_size - 0x10)).decode("utf-8")
			if isLookup:
				if currobj['id'] == sys.argv[2].lower() and (len(sys.argv) == 3 or sys.argv[3] in struct_type):
					locations.append(currobj['file'])

			if struct_type == 'enemy':
				ene.append(SetItem(currobj))
			elif struct_type == 'object':
				obj.append(SetItem(currobj))
			elif struct_type == 'design':
				design.append(SetItem(currobj))

if isLookup:
	print("\nLocations:")
	print('\t',end ='')
	locations = list(set(locations))
	locations.sort()
	print("\n\t".join(locations))
else:
	ene = list(set(ene))
	ene.sort()			
	obj = list(set(obj))
	obj.sort()
	design = list(set(design))
	design.sort()
	print("\nEnemies:")
	print('\t',ene)
	print("Objects:")
	print('\t',obj)
	print("Designs:")
	print('\t',design)