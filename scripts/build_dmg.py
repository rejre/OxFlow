#!/usr/bin/env python3
"""
OxFlow DMG 构建脚本
为 macOS 创建专业的 DMG 安装文件
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 配置
PROJECT_NAME = "OxFlow"
PROJECT_VERSION = "2.1.0"
APP_NAME = "OxFlow"
MAIN_SCRIPT = "src/ui/main_window.py"
ICON_FILE = "icon.png"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
DMG_DIR = "dmg_temp"

class DMGBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / OUTPUT_DIR
        self.build_dir = self.project_root / BUILD_DIR
        self.dmg_dir = self.project_root / DMG_DIR
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log(self, message: str, level: str = "INFO"):
        """打印日志消息"""
        colors = {
            "INFO": "\033[92m",    # 绿色
            "WARN": "\033[93m",    # 黄色
            "ERROR": "\033[91m",   # 红色
            "SUCCESS": "\033[94m", # 蓝色
        }
        reset = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{level}]{reset} {message}")
    
    def run_command(self, cmd: list, description: str = None) -> bool:
        """运行系统命令"""
        if description:
            self.log(description, "INFO")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=False,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"命令失败: {' '.join(cmd)}", "ERROR")
            return False
    
    def clean(self):
        """清理旧的构建文件"""
        self.log("清理旧的构建文件...", "INFO")
        for directory in [self.dist_dir, self.build_dir, self.dmg_dir]:
            if directory.exists():
                shutil.rmtree(directory)
                self.log(f"已删除: {directory}", "INFO")
    
    def build_app(self) -> bool:
        """使用 PyInstaller 构建应用"""
        self.log(f"构建 {PROJECT_NAME} 应用...", "INFO")
        
        # PyInstaller 命令
        cmd = [
            "pyinstaller",
            "--name", APP_NAME,
            "--onefile",
            "--windowed",
            "--icon", ICON_FILE,
            "--add-data", "src/utils:utils",
            "--add-data", "src/core:core",
            "--add-data", "src/resources:resources",
            "--collect-all", "customtkinter",
            "--collect-all", "yt_dlp",
            "--hidden-import", "PIL",
            "--hidden-import", "requests",
            "--hidden-import", "psutil",
            "--osx-bundle-identifier", "com.oxflow.app",
            "--target-architecture", "universal2",  # Intel + Apple Silicon
            MAIN_SCRIPT
        ]
        
        return self.run_command(cmd, f"编译 {PROJECT_NAME}...")
    
    def create_dmg(self) -> bool:
        """创建 DMG 文件"""
        self.log("创建 DMG 文件...", "INFO")
        
        app_path = self.dist_dir / f"{APP_NAME}.app"
        dmg_name = f"{PROJECT_NAME}-{PROJECT_VERSION}.dmg"
        dmg_path = self.dist_dir / dmg_name
        
        # 检查应用是否构建成功
        if not app_path.exists():
            self.log(f"应用未找到: {app_path}", "ERROR")
            return False
        
        # 创建临时 DMG 目录
        self.dmg_dir.mkdir(exist_ok=True)
        
        # 复制应用到临时目录
        dmg_app_path = self.dmg_dir / f"{APP_NAME}.app"
        if dmg_app_path.exists():
            shutil.rmtree(dmg_app_path)
        shutil.copytree(app_path, dmg_app_path)
        self.log(f"应用已复制到临时目录", "INFO")
        
        # 创建应用文件夹快捷方式
        applications_path = self.dmg_dir / "Applications"
        if not applications_path.exists():
            try:
                os.symlink("/Applications", applications_path)
                self.log("Applications 快捷方式已创建", "INFO")
            except OSError:
                self.log("无法创建 Applications 快捷方式", "WARN")
        
        # 创建背景图片
        self._create_background()
        
        # 使用 hdiutil 创建 DMG
        cmd = [
            "hdiutil",
            "create",
            "-volname", PROJECT_NAME,
            "-srcfolder", str(self.dmg_dir),
            "-ov",
            "-format", "UDZO",
            str(dmg_path)
        ]
        
        if not self.run_command(cmd, "使用 hdiutil 创建 DMG..."):
            return False
        
        self.log(f"DMG 文件已创建: {dmg_path}", "SUCCESS")
        
        # 检查文件大小
        if dmg_path.exists():
            size_mb = dmg_path.stat().st_size / (1024 * 1024)
            self.log(f"DMG 文件大小: {size_mb:.2f} MB", "INFO")
        
        return True
    
    def _create_background(self):
        """创建 DMG 背景图片"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 创建背景图片 (1200x800)
            width, height = 1200, 800
            img = Image.new("RGB", (width, height), color=(15, 15, 15))
            draw = ImageDraw.Draw(img)
            
            # 添加文本
            text = "OxFlow 安装程序"
            try:
                # 尝试使用系统字体
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            except:
                font = ImageFont.load_default()
            
            # 获取文本大小并居中
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            text_y = height // 2 - 50
            
            draw.text((text_x, text_y), text, fill=(0, 229, 255), font=font)
            
            # 保存背景图片
            bg_path = self.dmg_dir / ".background.png"
            img.save(bg_path)
            self.log(f"背景图片已创建: {bg_path}", "INFO")
            
        except ImportError:
            self.log("PIL 未安装，跳过背景图片创建", "WARN")
    
    def create_install_script(self) -> bool:
        """创建安装后脚本（可选）"""
        self.log("创建安装配置...", "INFO")
        
        # 创建 DS_Store 配置以美化 DMG 外观
        # 这需要专门的工具或手动配置
        
        return True
    
    def build(self) -> bool:
        """执行完整的构建流程"""
        self.log(f"开始构建 {PROJECT_NAME} DMG", "SUCCESS")
        self.log(f"版本: {PROJECT_VERSION}", "INFO")
        
        # 清理
        self.clean()
        
        # 构建应用
        if not self.build_app():
            self.log("应用构建失败", "ERROR")
            return False
        
        # 创建 DMG
        if not self.create_dmg():
            self.log("DMG 创建失败", "ERROR")
            return False
        
        # 清理临时文件
        if self.dmg_dir.exists():
            shutil.rmtree(self.dmg_dir)
            self.log("临时文件已清理", "INFO")
        
        self.log(f"构建完成！DMG 文件在: {self.dist_dir}", "SUCCESS")
        return True


def main():
    """主函数"""
    builder = DMGBuilder()
    
    try:
        if builder.build():
            print("\n" + "="*60)
            print("✅ DMG 安装文件构建成功！")
            print("="*60)
            print(f"\n📦 输出位置: dist/{PROJECT_NAME}-{PROJECT_VERSION}.dmg")
            print("\n📝 发行说明:")
            print("  1. 双击 DMG 文件以挂载")
            print("  2. 拖拽 OxFlow.app 到 Applications 文件夹")
            print("  3. 从 Applications 中启动 OxFlow")
            return 0
        else:
            print("\n" + "="*60)
            print("❌ DMG 构建失败")
            print("="*60)
            return 1
    except Exception as e:
        print(f"\n❌ 构建过程中出错: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
