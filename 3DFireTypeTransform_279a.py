bl_info={
    "name": "3D File Type Transform",
    "author": "Druid Ting",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > N",
    "description": "This is a program that converts an entire folder of 3D files to a specified 3D format.",
    "warning": "",
    "doc_url": "https://sites.google.com/view/blendertw/",
    "category": "3D View",
}

import bpy,os
from bpy.props import (StringProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )
from bpy.utils import register_class,unregister_class

class FilePropertyGroup(PropertyGroup):

    my_sourceURL= StringProperty(
        name="Source",
        description=":",
        default="input path",
        maxlen=1024,
        subtype='DIR_PATH',
        )
    my_outURL = StringProperty(
        name="Output",
        description=":",
        default="output path",
        maxlen=1024,
        subtype='DIR_PATH',
        )
    

    my_enum_inType = EnumProperty(
        name="Format",
        description="Select format.",
        items=[ ('.obj', ".obj", "Select OBJ format"),
                ('.fbx', ".fbx", "Select FBX format"),
                ('.x3d', ".x3d", "Select X3D format"),
                ('.3ds', ".3ds", "Select 3DS format"), #2.79
               ]
        )

    my_enum_outType = EnumProperty(
        name="Format",
        description="Select format.",
        items=[ ('.obj', "OBJ", "Output OBJ format"),
                ('.fbx', "FBX", "Output FBX format"),
                ('.x3d', "X3D", "Output X3D format"),
                ('.3ds', "3DS", "Output 3DS format"), #2.79
               ]
        )


class FileConvertsPlane(Panel):
    bl_label = "3D File Type Transform"
    bl_idname = "TOOLS_PT_1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "3D File Type Transform"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tftool = scene.tf_tool

        row = layout.row()
        row.label(text="File Type OBJ.FBX.3DS.X3D")
        row = layout.row()
        layout.prop(tftool,"my_sourceURL")
        row = layout.row()
        layout.prop(tftool,"my_outURL")
        row = layout.row()
        layout.prop(tftool,"my_enum_inType")
        row = layout.row()
        layout.prop(tftool,"my_enum_outType")
        row = layout.row()
        row.operator("wm.file_transform",text="File Transf")


class FileOperator(Operator):
    bl_label = "File Transform Operator"
    bl_idname = "wm.file_transform"

    def execute(self, context):
        scene = context.scene
        tftool = scene.tf_tool

        for i,j,k in os.walk(tftool.my_sourceURL):
            for a in k:
                if a.endswith(tftool.my_enum_inType):
                    bpy.ops.object.select_all(action='SELECT')
                    bpy.ops.object.delete()
                    lopath = tftool.my_sourceURL + "/"+a

                    if tftool.my_enum_inType == '.obj':
                        bpy.ops.import_scene.obj(filepath = lopath)
                        file_names,ext =  os.path.splitext(a)
                    if tftool.my_enum_inType == '.fbx':
                        bpy.ops.import_scene.fbx(filepath = lopath)
                        file_names,ext =  os.path.splitext(a)
                    if tftool.my_enum_inType == '.x3d':
                        bpy.ops.import_scene.x3d(filepath = lopath)
                        file_names,ext =  os.path.splitext(a)
                    if tftool.my_enum_inType == '.3ds':
                        bpy.ops.import_scene.autodesk_3ds(filepath = lopath) #2.79
                        file_names,ext =  os.path.splitext(a)


                    if tftool.my_enum_outType == '.obj':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.obj(filepath = outURL)
                    if tftool.my_enum_outType == '.fbx':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.fbx(filepath = outURL)
                    if tftool.my_enum_outType == '.x3d':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.x3d(filepath = outURL)
                    if tftool.my_enum_outType == '.3ds':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType #2.79
                        bpy.ops.export_scene.autodesk_3ds(filepath = outURL)

        return {'FINISHED'}


classes = [
    FileConvertsPlane,
    FileOperator,
    FilePropertyGroup
]

def register():
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.tf_tool = PointerProperty(type = FilePropertyGroup)
   

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.tf_tool

if __name__ == "__main__":
    register()
