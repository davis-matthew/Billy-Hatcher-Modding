import json, bpy, bmesh

billy_path = r"C:\Users\exeloar\Documents\Billy Hatcher Modding\Billy-PC\\" # CHANGE ME

set_obj = json.loads(open(billy_path+"set_obj_last2.json").read()) #CHANGE ME TOO
id = 0x5 #CHANGE ME (object to display)
mesh = bpy.data.meshes.new(f"id_{hex(id)}_spheres")
ball = bpy.data.objects.new(hex(id) + "_sphere_obj", mesh)
bm = bmesh.new()
verts = bmesh.ops.create_icosphere(bm, subdivisions=4,radius=15)
        
bm.to_mesh(mesh)
bm.free()

for i, obj in enumerate(set_obj):
    if int(obj['id'],16) == id:
        x, z, y = obj['position']
        y *= -1
        adj_vals = (x,y,z)
        print(adj_vals)
        curr_sphere = ball.copy()
        bpy.context.collection.objects.link(curr_sphere)
        bpy.context.view_layer.objects.active = curr_sphere
        curr_sphere.select_set(True)
        curr_sphere.location = adj_vals