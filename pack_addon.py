"""
生成可供 Blender “从磁盘安装插件” 使用的 ZIP 包。

用法：
1) 在仓库根目录运行：
   python pack_addon.py

2) 将生成的 ZIP：dist/texture_exporter.zip
   在 Blender 中打开 Edit > Preferences > Add-ons > Install...
   选择该 ZIP 安装即可。
"""

import os
import re
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
ADDON_DIR = os.path.join(ROOT, "texture_exporter")
DIST_DIR = os.path.join(ROOT, "dist")


def read_version():
    init_path = os.path.join(ADDON_DIR, "__init__.py")
    version = "1.0.0"
    if os.path.exists(init_path):
        text = open(init_path, "r", encoding="utf-8").read()
        m = re.search(r'"version"\s*:\s*\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\)', text)
        if m:
            version = ".".join(m.groups())
    return version


def make_zip(zip_name: str):
    os.makedirs(DIST_DIR, exist_ok=True)
    zip_path = os.path.join(DIST_DIR, zip_name)

    if not os.path.isdir(ADDON_DIR):
        raise RuntimeError(f"未找到插件目录：{ADDON_DIR}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ADDON_DIR):
            for fname in files:
                fpath = os.path.join(root, fname)
                # 在压缩包内保持以 texture_exporter/ 为根
                arcname = os.path.relpath(fpath, ROOT)
                zf.write(fpath, arcname)

    return zip_path


def main():
    version = read_version()
    # 固定文件名，确保 Blender 能正确识别安装（zip 根包含 texture_exporter/ 目录）
    zip_name = "texture_exporter.zip"
    zip_path = make_zip(zip_name)
    print(f"打包完成：{zip_path} (版本 {version})")
    print("现在可以在 Blender 中通过 Install... 选择该 ZIP 安装插件。")


if __name__ == "__main__":
    main()