"""
一键打包脚本
使用方式: python build.py
"""

import os
import sys
import shutil
import subprocess


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(base, "..")
    frontend_dir = os.path.join(project_root, "frontend")
    dist_dir = os.path.join(frontend_dir, "dist")

    print("=" * 50)

    print("Gnothi 打包工具")
    print("=" * 50)

    # ─── Step 1: 检查依赖 ───
    print("\n[1/5] 检查 Python 依赖...")
    required = ["flask", "flask_cors", "flask_sqlalchemy", "webview", "pyinstaller"]
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_").lower())
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} 未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)

    # ─── Step 2: 构建前端 ───
    print("\n[2/5] 构建前端...")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    # 检查 npm
    try:
        subprocess.run(
            ["npm", "--version"], capture_output=True, check=True, shell=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ✗ npm 未安装，请先安装 Node.js")
        sys.exit(1)

    # 检查 node_modules
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("  安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)

    print("  执行 npm run build...")
    subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, shell=True)

    if not os.path.exists(dist_dir):
        print("  ✗ 前端构建失败，dist 目录不存在")
        sys.exit(1)
    print(f"  ✓ 前端构建完成: {dist_dir}")

    # ─── Step 3: 清理旧构建 ───
    print("\n[3/5] 清理旧构建...")
    for d in ["build"]:
        p = os.path.join(base, d)
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"  ✓ 已清理 {d}/")
    # dist 只清理 exe，保留 data 目录
    dist_dir_build = os.path.join(base, "dist")
    if os.path.exists(dist_dir_build):
        for item in os.listdir(dist_dir_build):
            item_path = os.path.join(dist_dir_build, item)
            if item == "gnothi_data":
                continue  # 保留数据库
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print("  ✓ 已清理 dist/（保留 data/）")

    # ─── Step 4: PyInstaller 打包 ───
    print("\n[4/5] PyInstaller 打包中（可能需要几分钟）...")

    icon_path = os.path.join(base, "assets", "k5vkm-g92oy-001.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(project_root, "assets", "k5vkm-g92oy-001.ico")
    has_icon = os.path.exists(icon_path)
    
    if has_icon:
        print(f"  ✓ 使用图标: {icon_path}")
    else:
        print("  ⚠ 未找到 k5vkm-g92oy-001.ico，使用默认图标")
    
    # 收集所有需要的模块
    hidden_imports = [
        "flask",
        "flask.json",
        "flask_cors",
        "flask_sqlalchemy",
        "sqlalchemy",
        "sqlalchemy.sql.default_comparator",
        "sqlalchemy.ext.baked",
        "werkzeug",
        "werkzeug.serving",
        "werkzeug.debug",
        "webview",
        "webview.platforms.edgechromium",
        "webview.platforms.mshtml",
        "webview.platforms.winforms",
        "clr_loader",
        "pythonnet",
    ]

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Gnothi",
        "--clean",
        f"--add-data={dist_dir}{os.pathsep}frontend/dist",
    ]

    # 添加图标
    if has_icon:
        cmd.append(f"--icon={icon_path}")
    
    # 收集 models、routes、utils
    for module in ["models", "routes", "utils"]:
        module_dir = os.path.join(base, module)
        if os.path.exists(module_dir):
            cmd.append(f"--add-data={module_dir}{os.pathsep}{module}")

    # config.py
    config_file = os.path.join(base, "config.py")
    if os.path.exists(config_file):
        cmd.append(f"--add-data={config_file}{os.pathsep}.")

    for h in hidden_imports:
        cmd.append(f"--hidden-import={h}")

    cmd.append(os.path.join(base, "desktop.py"))

    print(f"  执行命令:")
    print(f"  {' '.join(cmd[:8])} ...")
    result = subprocess.run(cmd, cwd=base)

    if result.returncode != 0:
        print("  ✗ 打包失败")
        sys.exit(1)

    # ─── Step 5: 完成 ───
    output = os.path.join(base, "dist", "Gnothi.exe")
    print(f"\n[5/5] 打包完成！")
    print("=" * 50)
    print(f"  输出文件: {output}")

    if os.path.exists(output):
        size_mb = os.path.getsize(output) / 1024 / 1024
        print(f"  文件大小: {size_mb:.1f} MB")
    print("=" * 50)
    print("\n使用方式:")
    print("  1. 将 Gnothi.exe 复制到任意目录")
    print("  2. 双击运行")
    print("  3. 数据库和日志会自动创建在 exe 同级目录")


if __name__ == "__main__":
    main()
