import bpy 
import math 
from pathlib import Path
import string

OUTPUT_PATH = Path("/Users/USER/Desktop/alphabet")
#DATA_FONT = bpy.data.fonts.load("//../../../Library/Fonts/iosevka-heavy.ttc")
DATA_FONT = bpy.data.fonts.load("//../../../Library/Fonts/iosevka-comfy-extrabold.ttf")


def clear_scene():
    context = bpy.context
    scene = context.scene
    viewlayer = context.view_layer

    obs = [o for o in scene.objects if o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')

    for ob in obs:
        viewlayer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.delete()

def save_obj(obj, filename):
    viewlayer = bpy.context.view_layer
    viewlayer.objects.active = obj
    obj.select_set(True)
    stl_path = OUTPUT_PATH / f"{filename}.stl"
    bpy.ops.wm.stl_export(
        filepath=str(stl_path),
        export_selected_objects=True
    )
    obj.select_set(False)


def create_letter_mesh(letter, offset):
    font_curve = bpy.data.curves.new(type="FONT", name="LetterCurve")
    font_curve.body = letter

    font_obj = bpy.data.objects.new(name=letter, object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.data.font = DATA_FONT

    solidify = font_obj.modifiers.new(type='SOLIDIFY', name="mysolidify")
    solidify.offset = offset
    solidify.thickness = 2
    
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    object_eval = font_obj.evaluated_get(depsgraph)
    mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)
    o = bpy.data.objects.new(f"{letter}mesh", mesh_from_eval.copy())
    bpy.context.scene.collection.objects.link(o)
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[letter].select_set(True) 
    bpy.ops.object.delete() 
    
    return o 


def cut(obj, cutter):
    bool = obj.modifiers.new(type="BOOLEAN", name="bool")
    bool.object = cutter
    bool.use_hole_tolerant = True
    bool.use_self = True
    bool.operation = 'INTERSECT'
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="bool")


def main():
    chars = string.ascii_uppercase + string.digits
    for L1 in chars:
        for L2 in chars:
            clear_scene()
            main = create_letter_mesh(L1, 1)
            cutter = create_letter_mesh(L2, -1)
            cutter.rotation_euler = [0, math.radians(270), 0]
            cut(main, cutter)
            cutter.select_set(True) 
            bpy.ops.object.delete()
            save_obj(main, f"{L1}{L2}")

def debug():
    clear_scene()
    main = create_letter_mesh("J", 1)
    cutter = create_letter_mesh("Q", -1)
    cutter.rotation_euler = [0, math.radians(270), 0]
    cut(main, cutter)    

#debug()
main()


