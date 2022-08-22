bl_info={
    "name": "快速轉檔工具",
    "author": "Druid Ting",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "這是一個可以將一整個資料夾中的，文件全部轉換為指定格式，不用擔心有上百個檔案，彈指之間就完成",
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

    my_sourceURL: StringProperty(
        name="Source",
        description=":",
        default="選擇輸入路徑",
        maxlen=1024,
        subtype='DIR_PATH',
        )
    my_outURL: StringProperty(
        name="Output",
        description=":",
        default="選擇輸出路徑",
        maxlen=1024,
        subtype='DIR_PATH',
        )
    

    my_enum_inType: EnumProperty(
        name="格式:",
        description="選擇需要的格式.",
        items=[ ('.obj', ".obj", "選擇OBJ格式"),
                ('.fbx', ".fbx", "選擇FBX格式"),
                ('.gltf', ".gltf", "選擇GLTF格式"),
                ('.x3d', ".x3d", "選擇X3D格式"),
               ]
        )

    my_enum_outType: EnumProperty(
        name="格式:",
        description="選擇需要的格式.",
        items=[ ('.obj', "OBJ", "輸出OBJ格式"),
                ('.fbx', "FBX", "輸出FBX格式"),
                ('.gltf', "GLTF", "輸出GLTF格式"),
                ('.x3d', "X3D", "選擇X3D格式"),
               ]
        )


class FileConvertsPlane(Panel):
    bl_label = "快速轉檔工具"
    bl_idname = "TOOLS_PT_1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "快速轉檔工具"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tftool = scene.tf_tool

        row = layout.row()
        row.label(text="轉檔類型：OBJ/FBX/GLTF/X3D")
        row = layout.row()
        layout.prop(tftool,"my_sourceURL")
        row = layout.row()
        layout.prop(tftool,"my_outURL")
        row = layout.row()
        layout.prop(tftool,"my_enum_inType")
        row = layout.row()
        layout.prop(tftool,"my_enum_outType")
        row = layout.row()
        row.operator("d.file_transform",text="開始轉檔")


class FileOperator(Operator):
    bl_label = "File Transform Operator"
    bl_idname = "d.file_transform"

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
                    if tftool.my_enum_inType == '.gltf':
                        bpy.ops.import_scene.gltf(filepath = lopath)
                        file_names,ext =  os.path.splitext(a)
                    if tftool.my_enum_inType == '.x3d':
                        bpy.ops.import_scene.x3d(filepath = lopath)
                        file_names,ext =  os.path.splitext(a)


                    if tftool.my_enum_outType == '.obj':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.obj(filepath = outURL)
                    if tftool.my_enum_outType == '.fbx':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.fbx(filepath = outURL)
                    if tftool.my_enum_outType == '.gltf':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.gltf(filepath = outURL)
                    if tftool.my_enum_outType == '.x3d':
                        outURL = tftool.my_outURL+ file_names + tftool.my_enum_outType 
                        bpy.ops.export_scene.x3d(filepath = outURL)
                        

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
