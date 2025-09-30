import bpy
from bpy.props import StringProperty, CollectionProperty
from bpy.types import AddonPreferences, PropertyGroup

class ExportHistoryItem(PropertyGroup):
    """导出历史记录项"""
    path: StringProperty(
        name="Path",
        description="Export directory path",
        default=""
    )

class TextureExporterPreferences(AddonPreferences):
    """纹理导出器偏好设置"""
    bl_idname = __package__
    
    # 当前导出目录
    export_directory: StringProperty(
        name="Export Directory",
        description="Current export directory",
        default="",
        subtype='DIR_PATH'
    )
    
    # 导出历史记录
    export_history: CollectionProperty(
        type=ExportHistoryItem,
        name="Export History"
    )
    
    # 最大历史记录数量
    max_history_items: bpy.props.IntProperty(
        name="Max History Items",
        description="Maximum number of history items to keep",
        default=10,
        min=1,
        max=50
    )
    
    def draw(self, context):
        layout = self.layout
        
        # 当前导出目录
        layout.prop(self, "export_directory")
        
        # 最大历史记录数量
        layout.prop(self, "max_history_items")
        
        # 历史记录列表
        if self.export_history:
            box = layout.box()
            box.label(text="Export History:")
            for i, item in enumerate(self.export_history):
                row = box.row()
                row.label(text=f"{i+1}. {item.path}")
                op = row.operator("texture_exporter.remove_history", text="删除")
                op.index = i
    
    def add_to_history(self, path):
        """添加路径到历史记录"""
        # 检查是否已存在
        for item in self.export_history:
            if item.path == path:
                return
        
        # 添加新项目
        new_item = self.export_history.add()
        new_item.path = path
        
        # 限制历史记录数量
        while len(self.export_history) > self.max_history_items:
            self.export_history.remove(0)

def register():
    bpy.utils.register_class(ExportHistoryItem)
    bpy.utils.register_class(TextureExporterPreferences)

def unregister():
    bpy.utils.unregister_class(TextureExporterPreferences)
    bpy.utils.unregister_class(ExportHistoryItem)