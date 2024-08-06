'''
Finds the levels for a given object and offset that have non-zero values
This helps see how the game uses/modifies the values
Note that this relies on the data within the set files in the folder provided
'''

import struct
from binascii import hexlify
import sys
import os


fcontent = '''
<!DOCTYPE html>
<html>
<style>
.nested-div {
    margin-left: 0px;
}
.nested-div .nested-div {
    margin-left: 20px;
    display:none;
}
.nested-div .nested-div .nested-div {
    margin-left: 40px;
    display:none;
}
.nested-div .nested-div .nested-div .nested-div {
    margin-left: 60px;
    display:none;
}
.nested-div .nested-div .nested-div .nested-div .nested-div {
    margin-left: 80px;
    display:none;
}
</style>
<body>
'''

if not len(sys.argv) == 2 and not len(sys.argv) == 6:
    print("script <billy/folder/path>")
    exit(0)

def sort_dict(d):
    if isinstance(d, dict):
        return {k: sort_dict(v) for k, v in sorted(d.items())}
    elif isinstance(d, list):
        return [sort_dict(i) for i in sorted(d)]
    elif isinstance(d, set):
        return sorted(d)
    else:
        return d

def getDecValueForFloatHex(hStr):
    return struct.unpack('!f', bytes.fromhex(hStr))[0]

def getSignedFromUnsignedValue(val, blen):
    return int.from_bytes(val.to_bytes(blen, byteorder='big', signed=False), byteorder='big', signed=True)

def printToHTML(obj,ene,cam,design):
    global fcontent 
    
    def generateHTMLFromDict(dictName, dict):
        global fcontent
        dict = sort_dict(dict)
        ignoredParams = ["ID", "X pos", "Y pos", "Z pos", "X rotation", "Y rotation", "Z rotation"]
        fcontent += f'<div class="nested-div">{dictName} Set Info'

        for ID in dict:
            fcontent += f'<div class="nested-div">ID (dec): {ID}'
            for PARAMETER in dict[ID]:
                if PARAMETER.replace("~","") in ignoredParams:
                    continue
                fcontent += f'<div class="nested-div">{PARAMETER.replace("~","")}'
                for VALUE,FILES in dict[ID][PARAMETER].items():
                    fcontent += f'<div class="nested-div">Value (dec): {VALUE}'
                    if not "Float" in PARAMETER:
                        
                        if "Byte" in PARAMETER:
                            t = getSignedFromUnsignedValue(VALUE,1)
                            if t != VALUE:
                                fcontent += f', Signed Value (dec): {t}'
                        elif "Int" in PARAMETER:
                            t = getSignedFromUnsignedValue(VALUE,4)
                            if t != VALUE:
                                fcontent += f', Signed Value (dec): {t}'
                    fcontent += f'<div class="nested-div">{FILES}</div></div>'
                fcontent += '</div>'
            fcontent += '</div>'
        fcontent += "</div>"
    
    generateHTMLFromDict("Object",obj)
    generateHTMLFromDict("Enemy",ene)
    generateHTMLFromDict("Design",design)
    generateHTMLFromDict("Cam",cam)
    fcontent += '''
    <script>
        let divs = document.getElementsByClassName('nested-div')
        console.log("Divs: ")
        console.log(divs)
        for (let i = 0; i < divs.length; i++) {
            console.log("Current Div: ")
            console.log(divs[i])
            divs[i].addEventListener('click', function() {
                event.stopPropagation();
                let children = this.children;
                console.log(children)
                for (let j = 0; j < children.length; j++) {
                    if (children[j].style.display === 'none') {
                        children[j].style.display = 'block';
                    } else {
                        children[j].style.display = 'none';
                    }
                }
            });
        }
    </script>
    </body>
    </html>'''
    with open("usage.html",'w',encoding='utf-8') as out:
        out.write(fcontent)


def getParameter(sizes, offset):
    total = 0
    ind = 0
    for ind in range(len(sizes)):
        total += sizes[ind][0]
        if total > offset:
            return sizes[ind][1]
    return "Out of Bounds"

##################################################################################
'''
Dictionary Structure:
dict {
    set id {
        Parameter {
            Value : [Levels]
            Value2 : [Levels]
        }
        Parameter2 {
            etc.
        }
    }
    ID2 {
        etc.
    }
}
'''

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
        struct_dict = ene
        struct_size = 80 # size in bytes of 1 enemy
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 ,'~ID'),
                (4 ,'~~X pos'),
                (4 ,'~~Y pos'),
                (4 ,'~~Z pos'),
                (1 ,'~~~Offset 0x10'),
                (1 ,'~~~Offset 0x11'),
                (1 ,'~~~Offset 0x12'),
                (1 ,'~~~Offset 0x13'),
                (1 ,'~~~Offset 0x14'),
                (1 ,'~~~Offset 0x15'),
                (1 ,'~~~Offset 0x16'),
                (1 ,'~~~Offset 0x17'),
                (1 ,'~~~Offset 0x18'),
                (1 ,'~~~Offset 0x19'),
                (1 ,'~~~Offset 0x1A'),
                (1 ,'~~~Offset 0x1B'),
                (1 ,'~~~Offset 0x1C'),
                (1 ,'~~~Offset 0x1D'),
                (1 ,'~~~Offset 0x1E'),
                (1 ,'~~~Offset 0x1F'),
                (1 ,'~~~Offset 0x20'),
                (1 ,'~~~Offset 0x21'),
                (1 ,'~~~Offset 0x22'),
                (1 ,'~~~Offset 0x23'),
                (1 ,'~~~Offset 0x24'),
                (1 ,'~~~Offset 0x25'),
                (1 ,'~~~Offset 0x26'),
                (1 ,'~~~Offset 0x27'),
                (1 ,'~~~Offset 0x28'),
                (1 ,'~~~Offset 0x29'),
                (1 ,'~~~Offset 0x2A'),
                (1 ,'~~~Offset 0x2B'),
                (1 ,'~~~Offset 0x2C'),
                (1 ,'~~~Offset 0x2D'),
                (1 ,'~~~Offset 0x2E'),
                (1 ,'~~~Offset 0x2F'),
                (1 ,'~~~Offset 0x30'),
                (1 ,'~~~Offset 0x31'),
                (1 ,'~~~Offset 0x32'),
                (1 ,'~~~Offset 0x33'),
                (1 ,'~~~Offset 0x34'),
                (1 ,'~~~Offset 0x35'),
                (1 ,'~~~Offset 0x36'),
                (1 ,'~~~Offset 0x37'),
                (1 ,'~~~Offset 0x38'),
                (1 ,'~~~Offset 0x39'),
                (1 ,'~~~Offset 0x3A'),
                (1 ,'~~~Offset 0x3B'),
                (1 ,'~~~Offset 0x3C'),
                (1 ,'~~~Offset 0x3D'),
                (1 ,'~~~Offset 0x3E'),
                (1 ,'~~~Offset 0x3F'),
                (1 ,'~~~Offset 0x40'),
                (1 ,'~~~Offset 0x41'),
                (1 ,'~~~Offset 0x42'),
                (1 ,'~~~Offset 0x43'),
                (1 ,'~~~Offset 0x44'),
                (1 ,'~~~Offset 0x45'),
                (1 ,'~~~Offset 0x46'),
                (1 ,'~~~Offset 0x47'),
                (1 ,'~~~Offset 0x48'),
                (1 ,'~~~Offset 0x49'),
                (1 ,'~~~Offset 0x4A'),
                (1 ,'~~~Offset 0x4B'),
                (1 ,'~~~Offset 0x4C'),
                (1 ,'~~~Offset 0x4D'),
                (1 ,'~~~Offset 0x4E'),
                (1 ,'~~~Offset 0x4F')
            ]
    elif 'obj' in filename:
        struct_type = 'object'
        struct_dict = obj
        struct_size = 64 # size in bytes of 1 object
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 ,'~ID'),
                (4 ,'~~X pos'),
                (4 ,'~~Y pos'),
                (4 ,'~~Z pos'),
                (4 ,'~~~X rotation'),
                (4 ,'~~~Y rotation'),
                (4 ,'~~~Z rotation'),
                (4 ,'~~~~Int Param 1'),
                (4 ,'~~~~Int Param 2'),
                (4 ,'~~~~Int Param 3'),
                (4 ,'~~~~Int Param 4'),
                (4 ,'~~~~~Float Param 1'),
                (4 ,'~~~~~Float Param 2'),
                (4 ,'~~~~~Float Param 3'),
                (4 ,'~~~~~Float Param 4'),
                (1 ,'~~~~~~Byte Param 1'),
                (1 ,'~~~~~~Byte Param 2'),
                (1 ,'~~~~~~Byte Param 3'),
                (1 ,'~~~~~~Byte Param 4')
            ]
    elif 'design' in filename:
        struct_type = 'design'
        struct_dict = design
        struct_size = 64 # size in bytes of 1 design
        struct_arg_sizes = \
            [ # could add these in a loop after?
                (4 ,'~ID'),
                (4 ,'~~X pos'),
                (4 ,'~~Y pos'),
                (4 ,'~~Z pos'),
                (1 ,'~~~Offset 0x10'),
                (1 ,'~~~Offset 0x11'),
                (1 ,'~~~Offset 0x12'),
                (1 ,'~~~Offset 0x13'),
                (1 ,'~~~Offset 0x14'),
                (1 ,'~~~Offset 0x15'),
                (1 ,'~~~Offset 0x16'),
                (1 ,'~~~Offset 0x17'),
                (1 ,'~~~Offset 0x18'),
                (1 ,'~~~Offset 0x19'),
                (1 ,'~~~Offset 0x1A'),
                (1 ,'~~~Offset 0x1B'),
                (1 ,'~~~Offset 0x1C'),
                (1 ,'~~~Offset 0x1D'),
                (1 ,'~~~Offset 0x1E'),
                (1 ,'~~~Offset 0x1F'),
                (1 ,'~~~Offset 0x20'),
                (1 ,'~~~Offset 0x21'),
                (1 ,'~~~Offset 0x22'),
                (1 ,'~~~Offset 0x23'),
                (1 ,'~~~Offset 0x24'),
                (1 ,'~~~Offset 0x25'),
                (1 ,'~~~Offset 0x26'),
                (1 ,'~~~Offset 0x27'),
                (1 ,'~~~Offset 0x28'),
                (1 ,'~~~Offset 0x29'),
                (1 ,'~~~Offset 0x2A'),
                (1 ,'~~~Offset 0x2B'),
                (1 ,'~~~Offset 0x2C'),
                (1 ,'~~~Offset 0x2D'),
                (1 ,'~~~Offset 0x2E'),
                (1 ,'~~~Offset 0x2F'),
                (1 ,'~~~Offset 0x30'),
                (1 ,'~~~Offset 0x31'),
                (1 ,'~~~Offset 0x32'),
                (1 ,'~~~Offset 0x33'),
                (1 ,'~~~Offset 0x34'),
                (1 ,'~~~Offset 0x35'),
                (1 ,'~~~Offset 0x36'),
                (1 ,'~~~Offset 0x37'),
                (1 ,'~~~Offset 0x38'),
                (1 ,'~~~Offset 0x39'),
                (1 ,'~~~Offset 0x3A'),
                (1 ,'~~~Offset 0x3B'),
                (1 ,'~~~Offset 0x3C'),
                (1 ,'~~~Offset 0x3D'),
                (1 ,'~~~Offset 0x3E'),
                (1 ,'~~~Offset 0x3F')
            ]
    else:
        struct_type = 'cam'
        struct_dict = cam
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
            
            hex_id = data[:8].lstrip('0')
            if hex_id == '':
                continue
            
            dec_id = int(hex_id,16)
            if dec_id not in struct_dict:
                struct_dict[dec_id] = {}

            byte = 0
            i = 0
            while byte < len(byteSplit):
                value = byteSplit[byte:byte+struct_arg_sizes[i][0]]
                value = "".join(value)
                dec_value = int(value,16)
                if dec_value != 0:
                    param = getParameter(struct_arg_sizes, byte % struct_size)
                    if "Float" in param:
                        dec_value = getDecValueForFloatHex(value)
                    if param not in struct_dict[dec_id]:
                        struct_dict[dec_id][param] = {}
                    if dec_value not in struct_dict[dec_id][param]:
                        struct_dict[dec_id][param][dec_value] = set()
                    struct_dict[dec_id][param][dec_value].add(filename)
                
                byte += struct_arg_sizes[i][0]
                i += 1

##################################################################################
printToHTML(obj,ene,cam,design)