import bpy
from bpy.types import Panel

class TEXTURE_EXPORTER_PT_main_panel(Panel):
    """纹理导出器主面板"""
    bl_label = "Texture Exporter"
    bl_idname = "TEXTURE_EXPORTER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Export"
    
    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences
        
        # 主要导出按钮
        col = layout.column(align=True)
        col.operator("texture_exporter.export_textures", text="选择目录并导出")
        
        # 快速导出按钮（如果有上次目录）
        if prefs.export_directory:
            col.operator("texture_exporter.quick_export", text="快速导出到上次目录")
            
            # 显示当前目录
            box = layout.box()
            box.label(text="当前导出目录:")
            box.label(text=prefs.export_directory)
        
        # 历史记录部分
        if prefs.export_history:
            layout.separator()
            box = layout.box()
            box.label(text="导出历史:")
            
            for i, item in enumerate(prefs.export_history):
                row = box.row(align=True)
                # 使用历史目录按钮
                op = row.operator("texture_exporter.use_history", text=f"使用: {item.path[-30:]}")
                op.index = i
                # 删除按钮
                op_remove = row.operator("texture_exporter.remove_history", text="删除")
                op_remove.index = i

class TEXTURE_EXPORTER_PT_info_panel(Panel):
    """信息面板"""
    bl_label = "Export Info"
    bl_idname = "TEXTURE_EXPORTER_PT_info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Export"
    bl_parent_id = "TEXTURE_EXPORTER_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # 统计信息
        selected_count = len(context.selected_objects)
        visible_count = len(context.visible_objects)
        
        col = layout.column(align=True)
        col.label(text=f"选中对象: {selected_count}")
        col.label(text=f"可见对象: {visible_count}")
        
        # 预览将要导出的纹理数量
        images_count = self.count_exportable_images(context)
        col.label(text=f"可导出纹理: {images_count}")
        
        # 说明文本
        layout.separator()
        box = layout.box()
        box.label(text="说明:")
        box.label(text="• 导出选中和可见对象的纹理")
        box.label(text="• 支持网格、曲线等对象类型")
        box.label(text="• 只导出图像纹理节点")
        box.label(text="• 格式为PNG")
    
    def count_exportable_images(self, context):
        """计算可导出的图像数量"""
        selected_objects = context.selected_objects
        visible_objects = context.visible_objects
        all_objects = list(set(selected_objects) | set(visible_objects))
        
        images_to_export = set()
        
        for obj in all_objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                if hasattr(obj, 'material_slots') and obj.material_slots:
                    for material_slot in obj.material_slots:
                        material = material_slot.material
                        if material is not None and material.use_nodes:
                            for node in material.node_tree.nodes:
                                if node.type == 'TEX_IMAGE':
                                    image = node.image
                                    if image is not None and image.name and image.has_data:
                                        images_to_export.add(image)
        
        return len(images_to_export)

def register():
    bpy.utils.register_class(TEXTURE_EXPORTER_PT_main_panel)
    bpy.utils.register_class(TEXTURE_EXPORTER_PT_info_panel)

def unregister():
    bpy.utils.unregister_class(TEXTURE_EXPORTER_PT_info_panel)
    bpy.utils.unregister_class(TEXTURE_EXPORTER_PT_main_panel)