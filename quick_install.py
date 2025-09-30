"""
Blender Texture Exporter 一键安装脚本
在Blender脚本编辑器中运行此代码即可自动安装插件

使用方法：
1. 打开Blender
2. 切换到Scripting工作区
3. 复制并粘贴此代码到脚本编辑器
4. 点击运行按钮
"""

import bpy
import os
import sys
import tempfile
import shutil
from urllib.request import urlretrieve

# 插件下载URL（指向目标仓库）
DOWNLOAD_URL = "https://github.com/frankdzh/blender_export_to_unity/archive/refs/heads/main.zip"
ADDON_NAME = "texture_exporter"

def install_texture_exporter():
    """一键安装纹理导出器"""
    print("=== 开始安装 Texture Exporter 插件 ===")
    
    try:
        # 获取插件目录
        scripts_path = bpy.utils.script_path_user()
        if not scripts_path:
            version = bpy.app.version
            version_str = f"{version[0]}.{version[1]}"
            if sys.platform == "win32":
                scripts_path = os.path.expanduser(f"~/AppData/Roaming/Blender Foundation/Blender/{version_str}/scripts")
            elif sys.platform == "darwin":
                scripts_path = os.path.expanduser(f"~/Library/Application Support/Blender/{version_str}/scripts")
            else:
                scripts_path = os.path.expanduser(f"~/.config/blender/{version_str}/scripts")
        
        addons_path = os.path.join(scripts_path, "addons")
        os.makedirs(addons_path, exist_ok=True)
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "addon.zip")
        
        print("正在下载插件...")
        try:
            urlretrieve(DOWNLOAD_URL, zip_path)
            print("下载完成！")
        except Exception as e:
            print(f"下载失败: {e}")
            print("请检查网络连接或手动下载安装")
            return False
        
        # 解压并安装
        print("正在解压和安装...")
        import zipfile
        
        extract_path = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_path, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # 查找插件目录
        addon_source = None
        for root, dirs, files in os.walk(extract_path):
            if ADDON_NAME in dirs:
                addon_source = os.path.join(root, ADDON_NAME)
                break
            elif "__init__.py" in files and "bl_info" in open(os.path.join(root, "__init__.py")).read():
                addon_source = root
                break
        
        if not addon_source:
            print("未找到有效的插件目录")
            return False
        
        # 安装插件
        addon_target = os.path.join(addons_path, ADDON_NAME)
        if os.path.exists(addon_target):
            shutil.rmtree(addon_target)
        
        shutil.copytree(addon_source, addon_target)
        print(f"插件已安装到: {addon_target}")
        
        # 清理临时文件
        shutil.rmtree(temp_dir)
        
        # 刷新并启用插件
        print("正在启用插件...")
        bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_enable(module=ADDON_NAME)
        
        print("=== 安装完成！===")
        print("插件已成功安装并启用")
        print("您可以在3D视图的侧边栏中找到 'Texture Export' 面板")
        
        return True
        
    except Exception as e:
        print(f"安装过程中出现错误: {e}")
        return False

# 运行安装
if __name__ == "__main__":
    install_texture_exporter()
else:
    # 如果是通过exec()运行的，也执行安装
    install_texture_exporter()