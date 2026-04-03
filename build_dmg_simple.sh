#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "🔨 开始构建 OxFlow DMG..."
echo

# 激活虚拟环境
if [ -d "dmg_build_env" ]; then
    source dmg_build_env/bin/activate
fi

# 清理旧文件
echo "清理旧文件..."
rm -rf build dist dmg_temp
echo "✅ 旧文件已清理"
echo

# 构建应用
echo "构建应用..."
python3 -m PyInstaller \
    --name OxFlow \
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
    src/ui/main_window.py

if [ -d "dist/OxFlow.app" ]; then
    echo "✅ 应用构建成功"
else
    echo "❌ 应用构建失败"
    exit 1
fi
echo

# 创建 DMG
echo "创建 DMG 文件..."
mkdir -p dmg_temp
cp -r dist/OxFlow.app dmg_temp/
cd dmg_temp && ln -s /Applications Applications && cd ..

hdiutil create \
    -volname "OxFlow" \
    -srcfolder dmg_temp \
    -ov \
    -format UDZO \
    dist/OxFlow-2.1.0.dmg

rm -rf dmg_temp

if [ -f "dist/OxFlow-2.1.0.dmg" ]; then
    SIZE=$(du -h dist/OxFlow-2.1.0.dmg | awk '{print $1}')
    echo "✅ DMG 文件已创建"
    echo
    echo "════════════════════════════════════"
    echo "📦 文件信息:"
    echo "════════════════════════════════════"
    echo "位置: dist/OxFlow-2.1.0.dmg"
    echo "大小: $SIZE"
    ls -lh dist/OxFlow-2.1.0.dmg
    echo
    echo "📝 下一步:"
    echo "  1. 复制或上传 DMG 文件"
    echo "  2. 用户双击打开 DMG"
    echo "  3. 拖拽 OxFlow.app 到 Applications"
else
    echo "❌ DMG 创建失败"
    exit 1
fi
