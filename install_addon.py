#!/usr/bin/env python3
"""
Blender Texture Exporter 网络安装脚本
使用方法：
1. 在Blender的脚本编辑器中运行此脚本
2. 或者在命令行中运行：python install_addon.py
"""

import bpy
import os
import sys
import zipfile
import tempfile
import shutil
from urllib.request import urlretrieve
from urllib.error import URLError

# 插件信息
ADDON_NAME = "texture_exporter"
ADDON_VERSION = "1.0.0"
GITHUB_REPO = "your-username/blender-texture-exporter"  # 替换为实际的GitHub仓库
DOWNLOAD_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"

class TextureExporterInstaller:
    """纹理导出器安装器"""
    
    def __init__(self):
        self.addon_name = ADDON_NAME
        self.temp_dir = None
        
    def get_addon_directory(self):
        """获取Blender插件目录"""
        # 获取Blender用户脚本目录
        scripts_path = bpy.utils.script_path_user()
        if not scripts_path:
            # 如果没有用户脚本目录，使用默认位置
            import platform
            system = platform.system()
            if system == "Windows":
                scripts_path = os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender")
            elif system == "Darwin":  # macOS
                scripts_path = os.path.expanduser("~/Library/Application Support/Blender")
            else:  # Linux
                scripts_path = os.path.expanduser("~/.config/blender")
            
            # 添加版本号
            version = bpy.app.version
            version_str = f"{version[0]}.{version[1]}"
            scripts_path = os.path.join(scripts_path, version_str, "scripts")
        
        addons_path = os.path.join(scripts_path, "addons")
        return addons_path
    
    def download_addon(self, url):
        """从网络下载插件"""
        print(f"正在从 {url} 下载插件...")
        
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(self.temp_dir, "addon.zip")
        
        try:
            urlretrieve(url, zip_path)
            print("下载完成！")
            return zip_path
        except URLError as e:
            print(f"下载失败: {e}")
            return None
    
    def extract_addon(self, zip_path):
        """解压插件"""
        print("正在解压插件...")
        
        extract_path = os.path.join(self.temp_dir, "extracted")
        os.makedirs(extract_path, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # 查找插件目录
            for item in os.listdir(extract_path):
                item_path = os.path.join(extract_path, item)
                if os.path.isdir(item_path):
                    # 查找包含__init__.py的目录
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isdir(subitem_path) and subitem == self.addon_name:
                            return subitem_path
                        elif subitem == "__init__.py":
                            return item_path
            
            print("未找到有效的插件目录")
            return None
            
        except Exception as e:
            print(f"解压失败: {e}")
            return None
    
    def install_addon(self, addon_source_path):
        """安装插件到Blender"""
        print("正在安装插件...")
        
        addons_dir = self.get_addon_directory()
        os.makedirs(addons_dir, exist_ok=True)
        
        addon_target_path = os.path.join(addons_dir, self.addon_name)
        
        try:
            # 如果目标目录已存在，先删除
            if os.path.exists(addon_target_path):
                shutil.rmtree(addon_target_path)
            
            # 复制插件文件
            shutil.copytree(addon_source_path, addon_target_path)
            print(f"插件已安装到: {addon_target_path}")
            return True
            
        except Exception as e:
            print(f"安装失败: {e}")
            return False
    
    def enable_addon(self):
        """启用插件"""
        try:
            # 刷新插件列表
            bpy.ops.preferences.addon_refresh()
            
            # 启用插件
            bpy.ops.preferences.addon_enable(module=self.addon_name)
            print("插件已启用！")
            return True
            
        except Exception as e:
            print(f"启用插件失败: {e}")
            return False
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("临时文件已清理")
    
    def install_from_url(self, url):
        """从URL安装插件"""
        try:
            # 下载插件
            zip_path = self.download_addon(url)
            if not zip_path:
                return False
            
            # 解压插件
            addon_path = self.extract_addon(zip_path)
            if not addon_path:
                return False
            
            # 安装插件
            if not self.install_addon(addon_path):
                return False
            
            # 启用插件
            if not self.enable_addon():
                return False
            
            print("插件安装成功！")
            return True
            
        finally:
            self.cleanup()
    
    def install_from_local(self, local_path):
        """从本地路径安装插件"""
        try:
            if not os.path.exists(local_path):
                print(f"本地路径不存在: {local_path}")
                return False
            
            # 安装插件
            if not self.install_addon(local_path):
                return False
            
            # 启用插件
            if not self.enable_addon():
                return False
            
            print("插件安装成功！")
            return True
            
        except Exception as e:
            print(f"安装失败: {e}")
            return False

def main():
    """主函数"""
    installer = TextureExporterInstaller()
    
    print("=== Blender Texture Exporter 安装器 ===")
    print(f"插件名称: {ADDON_NAME}")
    print(f"版本: {ADDON_VERSION}")
    
    # 检查是否在Blender环境中运行
    try:
        import bpy
        print("检测到Blender环境")
        
        # 尝试从网络安装
        print("正在尝试从网络安装...")
        if installer.install_from_url(DOWNLOAD_URL):
            print("网络安装成功！")
        else:
            print("网络安装失败，请检查网络连接或手动安装")
            
            # 提供本地安装选项
            current_dir = os.path.dirname(os.path.abspath(__file__))
            local_addon_path = os.path.join(current_dir, ADDON_NAME)
            
            if os.path.exists(local_addon_path):
                print(f"发现本地插件目录: {local_addon_path}")
                if installer.install_from_local(local_addon_path):
                    print("本地安装成功！")
                else:
                    print("本地安装也失败了")
            else:
                print("未找到本地插件目录")
        
    except ImportError:
        print("错误: 此脚本需要在Blender环境中运行")
        print("请在Blender的脚本编辑器中运行此脚本")

if __name__ == "__main__":
    main()