bl_info = {
    "name": "Vertex Color Tools",
    "author": "Akhura Mazda",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > Property Panel > Mesh Edit | Obj Data Properties > Vertex Colors",
    "description": "Assigns Vertex Color and Alpha Value to Faces Edit Mode and changes order of Vertex Color Layers in Object Data Properties",
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

def vert_color_assign(self,context):
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
        vert_color_assign(self, context)        
        return {'FINISHED'}

class MESH_OT_MoveVertexColUp(bpy.types.Operator):
    bl_idname = "mesh.vertex_color_move_up"
    bl_label = "Move Layer Up"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        #start_time = time.time()
        mode_change = False
        
        if context.active_object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode="OBJECT")
            mode_change = True
        
        active_obj = bpy.context.active_object
        vertex_colors = active_obj.data.vertex_colors
        active_layer = vertex_colors.active
        active_index = vertex_colors.active_index
        
        if active_index != 0:            
            orig_name = str(active_layer.name)
            total_colors = len(active_obj.data.loops)

            previous_layer = vertex_colors[active_index - 1]        
            for color_index in range(total_colors):
                color_active = list(active_layer.data[color_index].color)
                color_previous = list(previous_layer.data[color_index].color)
                previous_layer.data[color_index].color = color_active
                active_layer.data[color_index].color = color_previous
                
            swapped_name = str(previous_layer.name)
            previous_layer.name = orig_name
            active_layer.name = swapped_name
            previous_layer.name = orig_name
            previous_layer.active = True
        
        if mode_change:
            bpy.ops.object.mode_set(mode="EDIT")
        
#        print("--- %s seconds ---" % (time.time() - start_time))
            
        return {'FINISHED'}

class MESH_OT_MoveVertexColDown(bpy.types.Operator):
    bl_idname = "mesh.vertex_color_move_down"
    bl_label = "Move Layer Down"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        #start_time = time.time()
        mode_change = False
        
        if context.active_object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode="OBJECT")
            mode_change = True
        
        active_obj = bpy.context.active_object
        vertex_colors = active_obj.data.vertex_colors
        active_layer = vertex_colors.active
        active_index = vertex_colors.active_index
        
        if active_layer != vertex_colors[-1]:            
            orig_name = str(active_layer.name)
            total_colors = len(active_obj.data.loops)

            next_layer = vertex_colors[active_index + 1]
            for color_index in range(total_colors):
                color_active = list(active_layer.data[color_index].color)
                color_next = list(next_layer.data[color_index].color)
                next_layer.data[color_index].color = color_active
                active_layer.data[color_index].color = color_next
            swapped_name = str(next_layer.name)
            next_layer.name = orig_name
            active_layer.name = swapped_name
            next_layer.name = orig_name
            next_layer.active = True
        
        if mode_change:
            bpy.ops.object.mode_set(mode="EDIT")
        
#        print("--- %s seconds ---" % (time.time() - start_time))
            
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

def vertex_colors_order_change(self, context):
    layout = self.layout
    row = layout.row()
    col = row.column()
    
    col.operator("mesh.vertex_color_move_up", icon='TRIA_UP')
    col.operator("mesh.vertex_color_move_down", icon='TRIA_DOWN')

def register():
    bpy.utils.register_class(PG_VertexColorSettings)
    bpy.utils.register_class(MESH_OT_VertexColorAssign)
    bpy.utils.register_class(MY_PT_VertexColorAssign)
    bpy.utils.register_class(MESH_OT_MoveVertexColUp)
    bpy.utils.register_class(MESH_OT_MoveVertexColDown)    
    bpy.types.DATA_PT_vertex_colors.append(vertex_colors_order_change)
    bpy.types.Scene.vertex_color = bpy.props.PointerProperty(type=PG_VertexColorSettings)

def unregister():
    bpy.utils.unregister_class(MESH_OT_MoveVertexColDown)
    bpy.utils.unregister_class(MESH_OT_MoveVertexColUp)
    bpy.utils.unregister_class(MY_PT_VertexColorAssign)
    bpy.utils.unregister_class(MESH_OT_VertexColorAssign)
    bpy.utils.unregister_class(PG_VertexColorSettings)    
    bpy.types.DATA_PT_vertex_colors.remove(vertex_colors_order_change)
    del bpy.types.Scene.vertex_color

if __name__ == "__main__":
    register()