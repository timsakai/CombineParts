bl_info = {
    "name": "CombineParts",
    "blender": (4, 2, 0),
    "category": "Interface",
    "version": (1, 0),
    "author": "TeimuSakai",
    "description": "Runs an Pre-Export Combine script from a button in the N panel.",
}

import bpy
import os
import importlib

# ボタン押下で外部スクリプトを実行するオペレーター
class EXTERNAL_OT_RunScript(bpy.types.Operator):
    bl_idname = "external.run_script"
    bl_label = "Run External Script"
    bl_description = "Runs an external script"

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        script_path = os.path.join(addon_dir, "Combine.py")

        # 外部スクリプトをインポートして実行
        try:
            if os.path.exists(script_path):
                spec = importlib.util.spec_from_file_location("combine", script_path)
                external_script = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(external_script)
                external_script.CombineParts()
                self.report({'INFO'}, "External script executed successfully.")
            else:
                self.report({'ERROR'}, "External script not found.")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {e}")
        return {'FINISHED'}

# コレクションセットアップ
class EXTERNAL_OT_SetupCollection(bpy.types.Operator):
    bl_idname = "external.setup_collection"
    bl_label = "SetupCollection"
    bl_description = "Setup Collection for Combining. Put Meshes to Parts Collection,its will be Combined on Run Combine pressed"

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        script_path = os.path.join(addon_dir, "Combine.py")

        # 外部スクリプトをインポートして実行
        try:
            if os.path.exists(script_path):
                spec = importlib.util.spec_from_file_location("combine", script_path)
                external_script = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(external_script)
                external_script.SetupCollection()
                self.report({'INFO'}, "External script executed successfully.")
                print("CombineParts has Create some Collections")
            else:
                self.report({'ERROR'}, "External script not found.")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {e}")
        return {'FINISHED'}
    

# Nパネルにボタンを配置するパネル
class EXTERNAL_PT_Panel(bpy.types.Panel):
    bl_label = "CombineParts"
    bl_idname = "COMBINEPARTS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CombineParts"

    def draw(self, context):
        layout = self.layout
        layout.operator(EXTERNAL_OT_SetupCollection.bl_idname, text="Setup Collection")
        layout.operator(EXTERNAL_OT_RunScript.bl_idname, text="Run Combine")

# アドオン登録/解除
def register():
    bpy.utils.register_class(EXTERNAL_OT_RunScript)
    bpy.utils.register_class(EXTERNAL_OT_SetupCollection)
    bpy.utils.register_class(EXTERNAL_PT_Panel)

def unregister():
    bpy.utils.unregister_class(EXTERNAL_PT_Panel)
    bpy.utils.unregister_class(EXTERNAL_OT_RunScript)
    bpy.utils.unregister_class(EXTERNAL_OT_SetupCollection)

if __name__ == "__main__":
    register()