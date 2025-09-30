import bpy
import os

# 设置导出目录
export_dir = "f:\\Downloads\\textdit\\tmp\\texture2"
os.makedirs(export_dir, exist_ok=True)

# 获取选中的对象和可见的对象[6](@ref)
selected_objects = bpy.context.selected_objects
visible_objects = bpy.context.visible_objects

# 合并选中的和可见的对象，并去重
all_objects = list(set(selected_objects) | set(visible_objects))

# 收集需要导出的图像（使用集合避免重复）
images_to_export = set()

# 遍历所有相关对象[6](@ref)
for obj in all_objects:
    # 只处理可能有材质的对象类型（网格、曲线等）
    if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
        # 检查对象是否真的有材质槽
        if hasattr(obj, 'material_slots') and obj.material_slots:
            # 遍历对象的材质槽[4](@ref)
            for material_slot in obj.material_slots:
                material = material_slot.material
                if material is not None:
                    # 检查材质是否使用节点系统[4](@ref)
                    if material.use_nodes:
                        # 遍历材质的所有节点
                        for node in material.node_tree.nodes:
                            # 只处理图像纹理节点[4](@ref)
                            if node.type == 'TEX_IMAGE':
                                image = node.image
                                # 确保图像有效且有名称为空
                                if image is not None and image.name:
                                    images_to_export.add(image)

# 导出收集到的图像
export_count = 0
for image in images_to_export:
    # 检查图像是否有有效数据[4](@ref)
    if image.has_data and image.name:
        # 构建完整的文件路径，使用PNG格式
        filepath = os.path.join(export_dir, image.name + ".png")
        try:
            # 保存图像
            image.save_render(filepath)
            print(f"成功导出: {filepath}")
            export_count += 1
        except Exception as e:
            print(f"导出失败 {image.name}: {e}")

print(f"导出完成！共成功导出 {export_count} 个纹理文件。")