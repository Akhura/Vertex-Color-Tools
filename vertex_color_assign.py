bl_info = {
    "name": "Assign Vertex Color to Selected Faces",
    "author": "Akhura Mazda",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Property Panel > Mesh Edit",
    "description": "Assigns Vertex Color and Alpha Value to Selected Faces in Edit Mode",
    "category": "3D View"
}

import bpy
import bmesh
#import time # Timer for debugging

class PG_VertexColorSettings(bpy.types.PropertyGroup):
    color_value: bpy.props.FloatVectorProperty(
        name="Vertex Color", 
        description="Main Vertex Color to be assigned", 
        default=(0.4, 0.4, 0.65), 
        min = 0.0, 
        max = 1.0, 
        subtype = 'COLOR_GAMMA'
        )
    
    alpha_value: bpy.props.FloatProperty(
        name="Alpha Value", 
        description="Alpha Value to be Assigned", 
        default=1.0, 
        min=0.0, 
        max = 1.0, 
        step=2, 
        precision=3
        )

def main(self,context):
#    start_time = time.time()
    active_obj = bpy.context.active_object
    mesh = active_obj.data
    bm = bmesh.from_edit_mesh(mesh)
    
    r, g, b = self.color_value[0], self.color_value[1], self.color_value[2]
    alpha = self.alpha_value
    loop_indices = []

    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                loop_indices.append(loop.index)

    bpy.ops.object.mode_set(mode="VERTEX_PAINT")

    active_layer = active_obj.data.vertex_colors.active
    for index in loop_indices:
        active_layer.data[index].color = [r, g, b, alpha]

    bpy.ops.object.mode_set(mode="EDIT")
#    print("--- %s seconds ---" % (time.time() - start_time))


class MESH_OT_VertexColorAssign(bpy.types.Operator):
    """Assign Vertex Color to selected faces"""
    bl_idname = "mesh.vertex_color_assign"
    bl_label = "Vertex Color Assign"
    bl_options = {'REGISTER','UNDO'}
    color_value: bpy.props.FloatVectorProperty(
        name="Vertex Color", 
        description="Main Vertex Color to be assigned", 
        default=(0.4, 0.4, 0.65), 
        min = 0.0, 
        max = 1.0, 
        subtype = 'COLOR_GAMMA'
        )
    
    alpha_value: bpy.props.FloatProperty(
        name="Alpha Value", 
        description="Alpha Value to be Assigned", 
        default=1.0, 
        min=0.0, 
        max = 1.0, 
        step=2, 
        precision=3
        )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        main(self, context)        
        return {'FINISHED'}

class MY_PT_VertexColorAssign(bpy.types.Panel):
    """Creates a Sub-Panel in the Property Area of the 3D View"""
    bl_label = "Vertex Color Assign"  
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "mesh_edit"

    def draw(self, context):
        obj = context.object
        props = self.layout.operator('mesh.vertex_color_assign')
        
        scene = context.scene
        vertex_colors = scene.vertex_color

        layout = self.layout
        
        row_color = layout.row()
        row_color.prop( vertex_colors, "color_value", text="Vertex Color")
        props.color_value = vertex_colors.color_value
        
        row_color = layout.row()
        row_color.prop( vertex_colors, "alpha_value", text="Alpha")
        props.alpha_value = vertex_colors.alpha_value      

def register():
    bpy.utils.register_class(PG_VertexColorSettings)
    bpy.utils.register_class(MESH_OT_VertexColorAssign)
    bpy.utils.register_class(MY_PT_VertexColorAssign)
    bpy.types.Scene.vertex_color = bpy.props.PointerProperty(type=PG_VertexColorSettings)

def unregister():
    bpy.utils.unregister_class(MY_PT_VertexColorAssign)
    bpy.utils.unregister_class(MESH_OT_VertexColorAssign)
    bpy.utils.unregister_class(PG_VertexColorSettings)
    del bpy.context.Scene.vertex_color
if __name__ == "__main__":
    register()
