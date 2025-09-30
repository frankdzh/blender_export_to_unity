import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

class TEXTURE_EXPORTER_OT_export_textures(Operator, ExportHelper):
    """导出纹理操作符"""
    bl_idname = "texture_exporter.export_textures"
    bl_label = "Export Textures"
    bl_description = "Export textures from selected and visible objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    # 文件选择器属性
    filename_ext = ""
    use_filter_folder = True
    
    directory: StringProperty(
        name="Directory",
        description="Export directory",
        subtype='DIR_PATH'
    )
    
    def execute(self, context):
        """执行导出操作"""
        export_dir = self.directory
        
        if not export_dir:
            self.report({'ERROR'}, "请选择导出目录")
            return {'CANCELLED'}
        
        # 创建导出目录
        os.makedirs(export_dir, exist_ok=True)
        
        # 获取选中的对象和可见的对象
        selected_objects = context.selected_objects
        visible_objects = context.visible_objects
        
        # 合并选中的和可见的对象，并去重
        all_objects = list(set(selected_objects) | set(visible_objects))
        
        # 收集需要导出的图像（使用集合避免重复）
        images_to_export = set()
        
        # 遍历所有相关对象
        for obj in all_objects:
            # 只处理可能有材质的对象类型（网格、曲线等）
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                # 检查对象是否真的有材质槽
                if hasattr(obj, 'material_slots') and obj.material_slots:
                    # 遍历对象的材质槽
                    for material_slot in obj.material_slots:
                        material = material_slot.material
                        if material is not None:
                            # 检查材质是否使用节点系统
                            if material.use_nodes:
                                # 遍历材质的所有节点
                                for node in material.node_tree.nodes:
                                    # 只处理图像纹理节点
                                    if node.type == 'TEX_IMAGE':
                                        image = node.image
                                        # 确保图像有效且有名称
                                        if image is not None and image.name:
                                            images_to_export.add(image)
        
        # 导出收集到的图像
        export_count = 0
        failed_count = 0
        
        for image in images_to_export:
            # 检查图像是否有有效数据
            if image.has_data and image.name:
                # 构建完整的文件路径，使用PNG格式
                filepath = os.path.join(export_dir, image.name + ".png")
                try:
                    # 保存图像
                    image.save_render(filepath)
                    export_count += 1
                except Exception as e:
                    print(f"导出失败 {image.name}: {e}")
                    failed_count += 1
        
        # 添加到历史记录
        prefs = context.preferences.addons[__package__].preferences
        prefs.add_to_history(export_dir)
        prefs.export_directory = export_dir
        
        # 报告结果
        if export_count > 0:
            message = f"成功导出 {export_count} 个纹理文件"
            if failed_count > 0:
                message += f"，{failed_count} 个失败"
            self.report({'INFO'}, message)
        else:
            self.report({'WARNING'}, "没有找到可导出的纹理")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        """调用文件选择器"""
        # 设置默认目录
        prefs = context.preferences.addons[__package__].preferences
        if prefs.export_directory:
            self.directory = prefs.export_directory
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class TEXTURE_EXPORTER_OT_quick_export(Operator):
    """快速导出到上次目录"""
    bl_idname = "texture_exporter.quick_export"
    bl_label = "Quick Export"
    bl_description = "Export textures to the last used directory"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """执行快速导出"""
        prefs = context.preferences.addons[__package__].preferences
        
        if not prefs.export_directory:
            self.report({'ERROR'}, "没有设置导出目录，请先使用普通导出")
            return {'CANCELLED'}
        
        # 使用导出操作符的逻辑
        export_op = TEXTURE_EXPORTER_OT_export_textures()
        export_op.directory = prefs.export_directory
        return export_op.execute(context)

class TEXTURE_EXPORTER_OT_use_history(Operator):
    """使用历史记录中的目录"""
    bl_idname = "texture_exporter.use_history"
    bl_label = "Use History Directory"
    bl_description = "Use a directory from export history"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        """执行使用历史目录"""
        prefs = context.preferences.addons[__package__].preferences
        
        if self.index < 0 or self.index >= len(prefs.export_history):
            self.report({'ERROR'}, "无效的历史记录索引")
            return {'CANCELLED'}
        
        # 设置导出目录并执行导出
        export_dir = prefs.export_history[self.index].path
        prefs.export_directory = export_dir
        
        # 使用导出操作符的逻辑
        export_op = TEXTURE_EXPORTER_OT_export_textures()
        export_op.directory = export_dir
        return export_op.execute(context)

class TEXTURE_EXPORTER_OT_remove_history(Operator):
    """删除历史记录项"""
    bl_idname = "texture_exporter.remove_history"
    bl_label = "Remove History Item"
    bl_description = "Remove an item from export history"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        """执行删除历史记录"""
        prefs = context.preferences.addons[__package__].preferences
        
        if self.index < 0 or self.index >= len(prefs.export_history):
            return {'CANCELLED'}
        
        prefs.export_history.remove(self.index)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(TEXTURE_EXPORTER_OT_export_textures)
    bpy.utils.register_class(TEXTURE_EXPORTER_OT_quick_export)
    bpy.utils.register_class(TEXTURE_EXPORTER_OT_use_history)
    bpy.utils.register_class(TEXTURE_EXPORTER_OT_remove_history)

def unregister():
    bpy.utils.unregister_class(TEXTURE_EXPORTER_OT_remove_history)
    bpy.utils.unregister_class(TEXTURE_EXPORTER_OT_use_history)
    bpy.utils.unregister_class(TEXTURE_EXPORTER_OT_quick_export)
    bpy.utils.unregister_class(TEXTURE_EXPORTER_OT_export_textures)