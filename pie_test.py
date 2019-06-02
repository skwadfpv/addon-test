bl_info = {
    "name": "Skwad modifiers Pie",
    "description": "Quickly add modifiers in full screen",
    "author": "Skwad and Discord community",
    "version": (0, 0, 8),
    "blender": (2, 80, 0),
    "location": "",
    "warning": "Use with caution",
    "wiki_url": "",
    "category": "Pie Menu"
}

import bpy
from bpy.types import Operator
from bpy.types import Menu
from bpy.types import Panel


##---------------cursor----------------------------------##
class SK_OT_SmartCursor(Operator):
    bl_idname = "view3d.smart_cursor"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        try:
            if context.active_object.mode == 'EDIT':
                if  context.object.data.total_vert_sel > 0:
                    bpy.ops.view3d.snap_cursor_to_selected()
                else:
                    bpy.ops.view3d.snap_cursor_to_center()
            elif len(bpy.context.selected_objects) > 0:
                bpy.ops.view3d.snap_cursor_to_selected()
            else:
                bpy.ops.view3d.snap_cursor_to_center()
        except:
            bpy.ops.view3d.snap_cursor_to_center()
    
        return {'FINISHED'}

    
## ------------------------------- ADD AN ARRAY MODIFIER WITH AXIS ------------------------ ##
class AddArray(Operator):
    bl_idname = "object.add_array"
    bl_label = "Add Array"
    bl_description = "Add an Array on Axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: bpy.props.StringProperty(name="Axis")
    count: bpy.props.IntProperty(name="Count", default=3)
    offset: bpy.props.FloatProperty(name="Ro", default=2)
    
    def execute(self, context):
        ArrayMod = bpy.context.object.modifiers.new("Array", 'ARRAY')
        ArrayMod.show_expanded = False
        ArrayMod.count = self.count
        ArrayMod.use_relative_offset = True

        if self.axis == "X":
            ArrayMod.relative_offset_displace[0] = self.offset
            ArrayMod.relative_offset_displace[1] = 0
            ArrayMod.relative_offset_displace[2] = 0
            
        elif self.axis == "Y":
            ArrayMod.relative_offset_displace[0] = 0
            ArrayMod.relative_offset_displace[1] = self.offset
            ArrayMod.relative_offset_displace[2] = 0
            
        elif self.axis == "Z":
            ArrayMod.relative_offset_displace[0] = 0
            ArrayMod.relative_offset_displace[1] = 0
            ArrayMod.relative_offset_displace[2] = self.offset
              
        return {'FINISHED'}
    
     
## ---------------------------- ADD A MIRROR MODIFIER WITH AXIS --------------------------- ##
class OBJECT_OT_AddMirror(Operator):
    bl_idname = "view3d.add_mirror"
    bl_label = "Add Mirror"
    bl_description = "Add a mirror on Axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: bpy.props.StringProperty(name="Axis")
    
    def execute(self, context):
        C = bpy.context
        target = C.active_object
        
        for obj in C.selected_objects:
            if obj != target:
            
                if self.axis == "X":
                    already = obj.modifiers.get("Mirror")
                    
                    if already is None:
                        Mod = obj.modifiers.new("Mirror", 'MIRROR')
                        Mod.mirror_object = target
                        Mod.use_axis[0] = True
                    else:
                        already.mirror_object = target
                        already.use_axis[0] = True
                        already.use_bisect_flip_axis[0] = False
                        already.use_bisect_axis[0] = False
   
                if self.axis == "Y":
                    already = obj.modifiers.get("Mirror")

                    if already is None:
                        Mod = obj.modifiers.new("Mirror", 'MIRROR')
                        Mod.mirror_object = target
                        Mod.use_axis[0] = False
                        Mod.use_axis[1] = True  
                    else:
                        already.use_axis[1] = True   
                        already.use_bisect_flip_axis[1] = False
                        already.use_bisect_axis[1] = False
                       
                if self.axis == "Z":
                    already = obj.modifiers.get("Mirror")
                    
                    if already is None:
                        Mod = obj.modifiers.new("Mirror", 'MIRROR')
                        Mod.mirror_object = target
                        Mod.use_axis[0] = False
                        Mod.use_axis[2] = True  
                    else:
                        already.use_axis[2] = True   
                        already.use_bisect_flip_axis[1] = False
                        already.use_bisect_axis[1] = False
                    
            ## ----- deselect the target and keep select the mirrored object-----##      
            target.select_set(state=False)
            obj.select_set(state=True)
            bpy.context.view_layer.objects.active = obj
        
        return {'FINISHED'}

  
## ----------------------------- ADD A BOOLEAN MODIFIER WITH TYPE ------------------------ ##
class OBJECT_OT_AddBool(Operator):
    bl_idname = "object.add_bool"
    bl_label = "BOOLEAN"
    bl_description = "choose a boolean operation"
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.IntProperty(name="Type")
    
    def execute(self, context):
        C = bpy.context
        O = bpy.ops.object
        bool_target = C.active_object
        
##------------------------------  S U B T R A C T ----------------------------------------##
        if self.type == 1:
            Boolmod = C.object.modifiers.new("Boo_sub_" + bool_target.name, 'BOOLEAN')
            Boolmod.operation = 'DIFFERENCE'
                         
            for obj in C.selected_objects:
                if obj != bool_target:
                    Boolmod.object = obj
                    obj.display_type = 'WIRE'
                    obj.name = "cutter"
                    obj.show_name = False
                    
            for md in C.object.modifiers.keys():
                if md.startswith("Weighted Normal"):
                    O.modifier_move_up(modifier= Boolmod.name)
                if md.startswith("angbev"):
                    O.modifier_move_up(modifier= Boolmod.name)
                                           
##---------------------------------- U N I O N -------------------------------------------##       
        elif self.type == 2:
            Boolmod = C.object.modifiers.new("Boo_add", 'BOOLEAN')
            Boolmod.operation = 'UNION'
            for boolobj in C.selected_objects:
                if boolobj != bool_target:
                    Boolmod.object = boolobj 

                              
##------------------------------- I N T E R S E C T -------------------------------------##
        elif self.type == 3:
            Boolmod = C.object.modifiers.new("Boo_inter", 'BOOLEAN')
            Boolmod.operation = 'INTERSECT'
            
            for boolobj in C.selected_objects:
                if boolobj != bool_target:
                    Boolmod.object = boolobj
 
                             
##---------------------------------- S L I C E --------------------------------------------##
        elif self.type == 4:
                 
            diffMod = bool_target.modifiers.new("Boo_diff_" + bool_target.name, "BOOLEAN")  # add mod to obj
            diffMod.operation = 'DIFFERENCE'
            for md in bool_target.modifiers.keys():
                        if md.startswith("angbev"):
                            O.modifier_move_up(modifier = diffMod.name)
            clone = bool_target.copy()
            context.collection.objects.link(clone)
            clMod = clone.modifiers.get(diffMod.name)
            clMod.name = "Boo_int_" + bool_target.name  # add mod to clone obj
            clMod.operation = 'INTERSECT' 
            
            for obj in C.selected_objects:
                if obj != bool_target and obj != clone:
                    obj.display_type = 'WIRE'
                    obj.name = "slicer"
                    obj.show_name = True
                    obj.select_set(True)
                    clMod.object = obj
                    diffMod.object = obj
                
                elif obj == bool_target:
                    obj.name = "target"
                    obj.show_name = True
                    obj.select_set(False)
                    
                elif obj == clone:
                    obj.name = "CLONE"
                    obj.show_name = True
                    obj.select_set(False)
                               
        return {'FINISHED'}


##-------------------------------PARenting booleans------------------------------##
class OBJECT_OT_AutoParent(Operator):
    bl_idname = "object.autoparent"
    bl_label = "PARENTING"
    bl_description = "" 
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,context):
        
        C = bpy.context
        O = bpy.ops.object
        parent_obj = C.active_object
        
        for obj in C.selected_objects:
            if obj != parent_obj:
                O.parent_set(type='OBJECT', keep_transform=True)
                    
        return {'FINISHED'}
    

##-------------select cutters--------------##
class OBJECT_OT_CutSelect(Operator):
    bl_idname = "object.cutselect"
    bl_label = "select cutters"
    bl_description = "" 
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.IntProperty(name="Type")
           
    def execute(self,context):
        
        C = bpy.context
        D = bpy.data
        
        if self.type == 1:
            for obj in D.objects:
                if obj.name.startswith("cutter"):
                    obj.select_set(True)
                else:
                    obj.select_set(False)
                     
        elif self.type == 2:
            for obj in D.objects:
                if obj.name.startswith("slicer"):
                    obj.select_set(True)
                else:
                    obj.select_set(False)
                    

        return {'FINISHED'} 


##------------- H I D E   B O O L E A N S  --------------##
class CutHide(Operator):
    bl_idname = "object.cuthide"
    bl_label = "hide cutters"
    bl_description = "" 
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.IntProperty(name="Type")
            
    def execute(self,context):
        C = bpy.context
        O = bpy.ops.object
        D = bpy.data
        
        if self.type == 1:
            for obj in D.objects():
                if obj.name.startswith("cutter"):
                    O.hide_view_set(unselected=False)
                    
        if self.type == 2:
            for obj in D.objects():
                if obj.name.startswith("slicer"):
                    O.hide_view_set(unselected=False)

        return {'FINISHED'}
    
      
##------------------------------------- ADD BEVEL -----------------------------##    
class OBJECT_OT_AddBevel(Operator):
    bl_idname = "object.add_bevel"
    bl_label = "BEVEL"
    bl_description = "choose a bevel" 
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.IntProperty(name="Type")
    bwidth: bpy.props.FloatProperty(name="Bwidth",min = 0.001, default=0.006)
    segments = bpy.props.IntProperty(name="segments",min = 1, default = 4)
    
    def execute(self, context):
        
        C=bpy.context
        target=C.active_object
        O = bpy.ops.object
        
        if self.type == 1:
            bevMod = target.modifiers.new("angbev",'BEVEL')
            bevMod.harden_normals = True
            bevMod.width = self.bwidth
            bevMod.segments = self.segments
            bevMod.limit_method = 'ANGLE'
            bevMod.angle_limit = 0.523599
            bevMod.offset_type = 'WIDTH'
            bevMod.show_expanded = False
            
            for md in C.object.modifiers.keys():
                if md.startswith("wbev"):
                    O.modifier_move_down(modifier = bevMod.name)
                elif md.startswith("Boo_int"):
                    O.modifier_move_down(modifier = bevMod.name)
        
        if self.type == 2:
            bevMod = target.modifiers.new("wbev",'BEVEL')
            bevMod.segments = 1
            bevMod.limit_method = 'WEIGHT'
            bevMod.offset_type = 'OFFSET'
            bevMod.show_expanded = False
            O.mode_set(mode='EDIT',toggle=True)
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            
            for md in C.object.modifiers.keys():
                if md.startswith("angbev"):
                    O.modifier_move_up(modifier = bevMod.name)
                elif md.startswith("Boo_int"):
                    O.modifier_move_up(modifier = bevMod.name)
                    
        if self.type == 3:
            bevMod = target.modifiers.new("vertbev",'BEVEL')
            bevMod.use_only_vertices = True
            bevMod.segments = 1
            bevMod.limit_method = 'VGROUP'
            bevMod.offset_type = 'OFFSET'   
            bevMod.show_expanded = False        
            O.mode_set(mode='EDIT',toggle=True)
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            
            for md in C.object.modifiers.keys():   
                if md.startswith("angbev"):
                    O.modifier_move_up(modifier = bevMod.name)
                elif md.startswith("wbev"):
                    O.modifier_move_up(modifier = bevMod.name)
                elif md.startswith("Boo_"):
                    O.modifier_move_up(modifier = bevMod.name)
        
        return {'FINISHED'}

    
##-------------------------------------TOGGLE WIRE DISPLAY-----------------------------##
class WireDisplay(Operator):
    bl_idname = "view3d.wire_dis"
    bl_label = "Wire mode"
    bl_description = "Toggle the wire display of the object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        obj = bpy.context.object
        
        if obj.display_type != 'WIRE': 
            obj.display_type = 'WIRE'
        else:
            obj.display_type = 'SOLID'
      
        return {'FINISHED'}


##-----------------------------APPLY SMOOTSHADING AND AUTOSMOOTH AT 30°---------------------## 
class Autosmooth(Operator):
    bl_idname = "view3d.smooth_dis"
    bl_label = "QuickShading"
    bl_description = "Apply shade smooth and Autosmooth"
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
       
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 0.523599

        return {'FINISHED'}
  
  
##------------------ S O L I D I F Y --------------------------##
class OBJECT_OT_AddSolidify(Operator):
    bl_idname = "object.add_solidify"
    bl_label = "solidify"
    bl_description = "apply solidify modifier"
    bl_options = {'REGISTER', 'UNDO'}
    type: bpy.props.IntProperty(name="Type")
    
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        
        if self.type == 1:
            bpy.context.object.modifiers["Solidify"].offset = 0
        
        elif self.type == 2:
            bpy.context.object.modifiers["Solidify"].offset = 1
            
        elif self.type == 3:
            bpy.context.object.modifiers["Solidify"].offset = -1
        
        bpy.context.object.modifiers["Solidify"].use_even_offset = True
        bpy.context.object.modifiers["Solidify"].use_quality_normals = True
        
        return {'FINISHED'}


## -------------------------- PIE MENU ----------------------------##
class VIEW3D_PIE_addmod(Menu):
    bl_label = "Add Modifiers"
    
    def draw(self, context):
        
        layout = self.layout
        pie = layout.menu_pie()
        
        box = pie.box()
        box.label(text="SPECIALS")
        col = box.column(align=True)
        col.operator("view3d.smart_cursor", text="Smartcursor")
        col.operator("view3d.wire_dis", text="Wire display Toggle")
        col.operator("view3d.smooth_dis", text="QuickShading")
        
        box = pie.box()
        box.label(text="BEVEL")
        col = box.column(align=True)
        prop = col.operator("object.add_bevel", text="Angle", icon='MOD_BEVEL')
        prop.type = 1
        prop = col.operator("object.add_bevel", text="Weight", icon='MOD_BEVEL')
        prop.type = 2
        prop = col.operator("object.add_bevel", text="VG", icon='MOD_BEVEL')
        prop.type = 3
        prop.bwidth = 0.02
        
        box.label(text="ARRAYS")
        col = box.column(align=True)
        prop = col.operator("object.add_array", text="+X", icon='MOD_ARRAY')
        prop.axis = 'X'
        prop.count = 3
        prop = col.operator("object.add_array", text="+Y", icon='MOD_ARRAY')
        prop.axis = 'Y'
        prop.count = 3
        prop = col.operator("object.add_array", text="+Z", icon='MOD_ARRAY')
        prop.axis = 'Z'
        prop.count = 3
        
        box.label(text="MIRROR")
        col = box.column(align=True)
        col.operator("view3d.add_mirror", text="+X", icon='MOD_MIRROR').axis = 'X'
        col.operator("view3d.add_mirror", text="+Y", icon='MOD_MIRROR').axis = 'Y'
        col.operator("view3d.add_mirror", text="+Z", icon='MOD_MIRROR').axis = 'Z'
        
        box.label(text="SOLIDIFY")
        col = box.column(align=True)
        prop = col.operator("object.add_solidify", text="Offset 0", icon='MOD_SOLIDIFY')
        prop.type = 1
        prop = col.operator("object.add_solidify", text="Offset 1", icon='MOD_SOLIDIFY')
        prop.type = 2
        prop = col.operator("object.add_solidify", text="Offset 1", icon='MOD_SOLIDIFY')
        prop.type = 3
    
        box = pie.box()
        box.label(text="PARENTING")
        col = box.column(align=True)
        col.operator("object.autoparent", text="parenting")
        
        prop = col.operator("object.cutselect", text="select Cutters")
        prop.type = 1
        prop = col.operator("object.cutselect", text="select Slicers")
        prop.type = 2
        
        prop = col.operator("object.cuthide", text="hide cutters")
        prop.type = 1
        prop = col.operator("object.cuthide", text="hide slicers")
        prop.type = 2
        
        box = pie.box()
        box.label(text="BOOLEANS")
        col = box.column(align=True)
        row= col.row()
        col.operator("object.add_bool", text="Subtract", icon='MOD_BOOLEAN').type = 1
        col.operator("object.add_bool", text="Add", icon='MOD_BOOLEAN' ).type = 2
        row= col.row()
        row.operator("object.add_bool", text="Intersect", icon='MOD_BOOLEAN').type = 3
        row.operator("object.add_bool", text="Slice mf", icon='MOD_BOOLEAN').type = 4


##------------------------- REGISTER------------------------- ##
classes = (
    SK_OT_SmartCursor,
    AddArray,
    OBJECT_OT_AddMirror,
    OBJECT_OT_AddBool,
    OBJECT_OT_AddBevel,
    OBJECT_OT_AutoParent,
    OBJECT_OT_CutSelect,
    CutHide,
    WireDisplay,
    Autosmooth,
    OBJECT_OT_AddSolidify,
    VIEW3D_PIE_addmod,
    
)

register, unregister = bpy.utils.register_classes_factory(classes)
    
        
if __name__ == '__main__':
    register()
    bpy.ops.wm.call_menu_pie(name='VIEW3D_PIE_addmod')