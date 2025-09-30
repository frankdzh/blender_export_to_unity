bl_info = {
    "name": "Texture Exporter",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Texture Export",
    "description": "Export textures from selected and visible objects with UI and history",
    "warning": "",
    "doc_url": "https://github.com/frankdzh/blender_export_to_unity#readme",
    "category": "Import-Export",
}

import bpy
from . import operators
from . import panels
from . import preferences

def register():
    """注册插件"""
    preferences.register()
    operators.register()
    panels.register()

def unregister():
    """注销插件"""
    panels.unregister()
    operators.unregister()
    preferences.unregister()

if __name__ == "__main__":
    register()