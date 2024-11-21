import bpy

# コレクションを確認または作成する関数
def ensure_collection_exists(name):
    if name not in bpy.data.collections:
        # 指定した名前のコレクションが存在しない場合、新規作成
        new_collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_collection)
        print(f"Collection '{name}' was created.")
    else:
        print(f"Collection '{name}' already exists.")

def SetupCollection():
    # "Combine"と"Parts"のコレクションを確認または作成
    ensure_collection_exists("Combined")
    ensure_collection_exists("Parts")

def get_all_objects_in_collection(collection):
    objects = []

    # コレクション内の全てのオブジェクトを追加
    objects.extend(collection.objects)

    # サブコレクションも再帰的に探索
    for sub_collection in collection.children:
        objects.extend(get_all_objects_in_collection(sub_collection))

    return objects

def CombineParts():
    # delete combined
    combined_collection = bpy.data.collections.get("Combined")
    combeds = [obj for obj in combined_collection.all_objects]
    if combined_collection is not None:
        for comb_obj in combeds:
            bpy.data.objects.remove(comb_obj, do_unlink=True)
    
    # 指定したコレクション内のメッシュオブジェクトを取得
    collection_name = "Parts"
    collection = bpy.data.collections[collection_name]
    mesh_objects = get_all_objects_in_collection(collection)
    mesh_objects = [obj for obj in mesh_objects if obj.type == 'MESH']
    mesh_objects = [obj for obj in mesh_objects if not obj.hide_get()] 
    
    # Mirrorモディファイアがついていたオブジェクトとついていなかったオブジェクトに分ける
    mirror_objects = [obj for obj in mesh_objects if obj.modifiers.get("Mirror")]
    no_mirror_objects = [obj for obj in mesh_objects if obj not in mirror_objects]
    
    # tempオブジェクトをtempコレクションに挿入
    temp_collection = bpy.data.collections.get("Temp")
    if temp_collection is None:
        temp_collection = bpy.data.collections.new("Temp")
        bpy.context.scene.collection.children.link(temp_collection)
    
    # 結合前メッシュオブジェクトを一時オブジェクトにコピー
    temp_objects = []
    for obj in mesh_objects:
        temp_obj = obj.copy()
        temp_obj.data = obj.data.copy()
        temp_collection.objects.link(temp_obj)
        temp_objects.append(temp_obj)
        
    temp_objects_mirror = [obj for obj in temp_objects if obj.modifiers.get("Mirror")]
    temp_objects_no_mirror = [obj for obj in temp_objects if obj not in temp_objects_mirror]
    
    temp_objects_arrays = [temp_objects_mirror,temp_objects_no_mirror]
    
    # 結合前メッシュオブジェクトについて、AutoSmoothAngle以上の角度を条件に辺をシャープにする
    # 3.x4.xでSmoothで仕様が違うので対応
    bpy.ops.object.select_all(action='DESELECT')
    for obj in temp_objects:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        if bpy.context.object.modifiers.get("Auto Smooth"):
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=obj.modifiers["Auto Smooth"]["Socket_2"])
            bpy.ops.mesh.mark_sharp()
        else:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
        if bpy.context.object.modifiers.get("Smooth by Angle"):
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=obj.modifiers["Smooth by Angle"]["Input_1"])
            bpy.ops.mesh.mark_sharp()
        bpy.ops.object.editmode_toggle()
    
    # 結合前メッシュオブジェクトについて、移動・回転・拡縮の値を適用
    bpy.ops.object.select_all(action='DESELECT')
    for obj in temp_objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # 結合前メッシュオブジェクトについて、Armature,Mirror以外のモディファイアを適用
    for obj in temp_objects:
        for mod in obj.modifiers:
            if mod.type not in {"ARMATURE"}:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=mod.name)
    
    # 結合(Mirrorモディファイアがついていたオブジェクト、ついていなかったオブジェクト
    # Mirrorモディファイアがついていたオブジェクトを結合
    obj_copy_mirror = []
    if temp_objects_mirror:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in temp_objects_mirror:
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()
            bpy.context.scene.collection.objects.link(obj_copy)
            obj_copy.select_set(True)
            obj_copy_mirror.append(obj_copy)
        bpy.context.view_layer.objects.active = obj_copy_mirror[0]
        bpy.ops.object.join()
        bpy.ops.object.modifier_add_node_group(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle")
        bpy.context.object.modifiers["Smooth by Angle"]["Input_1"] = 3.14159
        
        # 結合後のオブジェクトを設定
        combined_obj = bpy.context.view_layer.objects.active
        combined_obj.name = collection_name + "_mirror_combined"
    
        # 結合後のオブジェクトをCombinedコレクションに挿入
        combined_collection = bpy.data.collections.get("Combined")
        if combined_collection is None:
            combined_collection = bpy.data.collections.new("Combined")
            bpy.context.scene.collection.children.link(combined_collection)
        combined_collection.objects.link(combined_obj)
        bpy.context.scene.collection.objects.unlink(combined_obj)
    
    # NoMirrorモディファイアオブジェクトを結合
    obj_copy_no_mirror = []
    if temp_objects_no_mirror:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in temp_objects_no_mirror:
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()
            bpy.context.scene.collection.objects.link(obj_copy)
            obj_copy.select_set(True)
            obj_copy_no_mirror.append(obj_copy)
        bpy.context.view_layer.objects.active = obj_copy_no_mirror[0]
        bpy.ops.object.join()
        
    # 結合後のオブジェクトを設定
    combined_obj = bpy.context.view_layer.objects.active
    combined_obj.name = collection_name + "_combined"
    
    # 結合後のオブジェクトをCombinedコレクションに挿入
    combined_collection = bpy.data.collections.get("Combined")
    if combined_collection is None:
        combined_collection = bpy.data.collections.new("Combined")
        bpy.context.scene.collection.children.link(combined_collection)
    combined_collection.objects.link(combined_obj)
    bpy.context.scene.collection.objects.unlink(combined_obj)
    
    # Mirror,NoMirror を結合
    collection_name = "Combined"
    collection = bpy.data.collections[collection_name]
    combined_objects = [obj for obj in collection.all_objects if obj.type == 'MESH']
    
    armature = "Armature" in bpy.data.objects
    if armature :
        bpy.ops.object.select_all(action='DESELECT')
        for obj in combined_objects:
            obj.select_set(True)
        bpy.ops.object.join()
        bpy.ops.object.modifier_add(type='ARMATURE')
        bpy.context.object.modifiers["Armature"].object = bpy.data.objects["Armature"]
        bpy.ops.object.modifier_remove(modifier="Armature.001")
    
    # 一時オブジェクトを削除
    for temp_obj in temp_objects:
        print("unko")
        bpy.data.objects.remove(temp_obj, do_unlink=True)
        