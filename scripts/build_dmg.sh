#!/bin/bash
# OxFlow DMG 构建脚本 (Shell 版本)

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  OxFlow macOS DMG 构建工具              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}[1/5]${NC} 检查依赖..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python3 已安装${NC}"
    
    # 检查 PyInstaller
    if ! python3 -m pip show pyinstaller > /dev/null; then
        echo -e "${YELLOW}⚠️  PyInstaller 未安装，正在安装...${NC}"
        python3 -m pip install pyinstaller -q
    fi
    echo -e "${GREEN}✅ PyInstaller 已安装${NC}"
    
    # 检查 hdiutil (macOS 内置)
    if ! command -v hdiutil &> /dev/null; then
        echo -e "${RED}❌ hdiutil 未找到 (仅限 macOS)${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ hdiutil 已安装${NC}"
    echo
}

# 安装依赖库
install_requirements() {
    echo -e "${BLUE}[2/5]${NC} 安装项目依赖..."
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -q -r requirements.txt
        echo -e "${GREEN}✅ 项目依赖已安装${NC}"
    fi
    echo
}

# 构建应用
build_app() {
    echo -e "${BLUE}[3/5]${NC} 使用 PyInstaller 构建应用..."
    
    python3 -m PyInstaller \
        --name OxFlow \
        --onefile \
        --windowed \
        --icon icon.png \
        --add-data "src/utils:utils" \
        --add-data "src/core:core" \
        --add-data "src/resources:resources" \
        --collect-all customtkinter \
        --collect-all yt_dlp \
        --hidden-import PIL \
        --hidden-import requests \
        --hidden-import psutil \
        --osx-bundle-identifier com.oxflow.app \
        --target-architecture universal2 \
        src/ui/main_window.py
    
    if [ -d "dist/OxFlow.app" ]; then
        echo -e "${GREEN}✅ 应用构建成功${NC}"
    else
        echo -e "${RED}❌ 应用构建失败${NC}"
        exit 1
    fi
    echo
}

# 创建 DMG
create_dmg() {
    echo -e "${BLUE}[4/5]${NC} 创建 DMG 安装文件..."
    
    DMG_TEMP="dmg_temp"
    DMG_NAME="OxFlow-2.1.0.dmg"
    
    # 创建临时目录
    rm -rf "$DMG_TEMP"
    mkdir -p "$DMG_TEMP"
    
    # 复制应用
    cp -r "dist/OxFlow.app" "$DMG_TEMP/"
    
    # 创建 Applications 快捷方式
    cd "$DMG_TEMP"
    ln -s /Applications Applications
    cd - > /dev/null
    
    # 使用 hdiutil 创建 DMG
    hdiutil create \
        -volname "OxFlow" \
        -srcfolder "$DMG_TEMP" \
        -ov \
        -format UDZO \
        "dist/$DMG_NAME"
    
    # 清理临时文件
    rm -rf "$DMG_TEMP"
    
    if [ -f "dist/$DMG_NAME" ]; then
        SIZE=$(du -h "dist/$DMG_NAME" | awk '{print $1}')
        echo -e "${GREEN}✅ DMG 文件已创建: dist/$DMG_NAME (大小: $SIZE)${NC}"
    else
        echo -e "${RED}❌ DMG 创建失败${NC}"
        exit 1
    fi
    echo
}

# 生成完成信息
finish() {
    echo -e "${BLUE}[5/5]${NC} 构建完成！"
    echo
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ DMG 安装文件已成功创建              ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo
    echo -e "${YELLOW}📦 输出文件:${NC}"
    echo "   dist/OxFlow-2.1.0.dmg"
    echo
    echo -e "${YELLOW}📝 使用说明:${NC}"
    echo "   1. 双击 DMG 文件以挂载"
    echo "   2. 拖拽 OxFlow 到 Applications 文件夹"
    echo "   3. 从 Launchpad 或 Applications 启动 OxFlow"
    echo
    echo -e "${YELLOW}🔗 相关文件:${NC}"
    echo "   • 源代码: dist/OxFlow.app"
    echo "   • 构建日志: build/"
    echo
}

# 主程序
main() {
    check_dependencies
    install_requirements
    build_app
    create_dmg
    finish
}

# 执行
main
