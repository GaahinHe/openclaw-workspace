#!/bin/bash
# Notion Clipper Pro - 完全自动安装（需要辅助功能权限）

PLUGIN_DIR="$HOME/.openclaw/workspace/notion-clipper-pro"

echo "🚀 开始自动安装 Notion Clipper Pro 到 Edge"
echo ""

# 1. 打开 Edge
echo "📱 打开 Edge 浏览器..."
open -a "Microsoft Edge"
sleep 2

# 2. 导航到扩展页面
echo "🔗 导航到扩展页面..."
osascript -e 'tell application "Microsoft Edge" to set URL of front window to "edge://extensions/"'
sleep 2

# 3. 显示通知
echo "📬 发送系统通知..."
osascript -e 'display notification "请点击：\n1. 右上角\"开发者模式\"开关\n2. \"加载已解压的扩展程序\"\n3. 选择 notion-clipper-pro 文件夹" with title "Notion Clipper Pro 安装指引"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Edge 已打开到扩展页面"
echo ""
echo "⚠️  由于 macOS 安全限制，需要您手动完成最后 3 步："
echo ""
echo "1️⃣  点击右上角【开发者模式】开关"
echo "2️⃣  点击【加载已解压的扩展程序】按钮"
echo "3️⃣  选择文件夹：$PLUGIN_DIR"
echo ""
echo "📁 或直接在 Finder 中选中此文件夹后拖拽到 Edge："
echo "   $PLUGIN_DIR"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示：加载成功后会看到 📋 图标"
echo ""

# 4. 打开 Finder 并定位到插件目录（方便拖拽）
echo "📂 打开 Finder 定位到插件目录..."
open -R "$PLUGIN_DIR/manifest.json"

echo ""
echo "✅ 准备完成！现在可以手动加载或拖拽 manifest.json 到 Edge"
