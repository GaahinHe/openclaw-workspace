#!/bin/bash
# Notion Clipper Pro - 完全自动安装脚本
# 需要辅助功能权限

set -e

PLUGIN_DIR="$HOME/.openclaw/workspace/notion-clipper-pro"

echo "🚀 Notion Clipper Pro - 完全自动安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 激活 Edge
echo "📱 激活 Edge 浏览器..."
osascript -e 'tell application "Microsoft Edge" to activate'
sleep 2

# 2. 导航到扩展页面
echo "🔗 导航到 edge://extensions/..."
osascript -e 'tell application "System Events"' \
          -e 'keystroke "l" using command down' \
          -e 'delay 0.5' \
          -e 'keystroke "edge://extensions/"' \
          -e 'delay 0.5' \
          -e 'keystroke return' \
          -e 'end tell'
sleep 3

# 3. 点击开发者模式开关（右上角）
echo "🔓 开启开发者模式..."
cliclick c:1750,80
sleep 2

# 4. 点击加载已解压的扩展程序
echo "📦 点击加载已解压的扩展程序..."
cliclick c:200,200
sleep 2

# 5. 输入插件目录路径
echo "📁 选择插件目录..."
osascript -e 'tell application "System Events"' \
          -e 'keystroke "'"$PLUGIN_DIR"'"' \
          -e 'delay 1' \
          -e 'keystroke return' \
          -e 'end tell'
sleep 3

# 6. 验证安装
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 安装完成！"
echo ""
echo "📋 验证步骤："
echo "1. 检查 Edge 工具栏是否有 📋 图标"
echo "2. 点击图标测试弹出界面"
echo "3. 打开任意网页测试保存功能"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
