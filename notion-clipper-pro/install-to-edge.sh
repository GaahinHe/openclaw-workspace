#!/bin/bash
# Notion Clipper Pro - Edge 插件自动安装脚本
# 适用于 macOS

set -e

PLUGIN_DIR="$HOME/.openclaw/workspace/notion-clipper-pro"
EDGE_DATA_DIR="$HOME/Library/Application Support/com.microsoft.Edge"

echo "🚀 Notion Clipper Pro - Edge 插件自动安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Edge 是否运行
if pgrep -x "Microsoft Edge" > /dev/null; then
    echo "⚠️  Edge 正在运行，请先关闭 Edge 浏览器"
    echo "   按回车键继续（或 Ctrl+C 取消）"
    read
    osascript -e 'tell application "Microsoft Edge" to quit'
    sleep 2
fi

echo "✅ Edge 已关闭"
echo ""

# 检查插件目录
if [ ! -d "$PLUGIN_DIR" ]; then
    echo "❌ 插件目录不存在：$PLUGIN_DIR"
    exit 1
fi

echo "✅ 插件目录存在：$PLUGIN_DIR"
echo ""

# 检查 manifest.json
if [ ! -f "$PLUGIN_DIR/manifest.json" ]; then
    echo "❌ manifest.json 不存在"
    exit 1
fi

echo "✅ manifest.json 存在"
echo ""

# 检查图标文件
MISSING_ICONS=0
for size in 16 32 48 128; do
    if [ ! -f "$PLUGIN_DIR/icons/icon${size}.png" ]; then
        echo "⚠️  缺少图标：icons/icon${size}.png"
        MISSING_ICONS=1
    fi
done

if [ $MISSING_ICONS -eq 1 ]; then
    echo ""
    echo "❌ 图标文件缺失，请先运行图标生成"
    exit 1
fi

echo "✅ 所有图标文件存在"
echo ""

# 创建 Edge 开发者配置
PREFERENCES_FILE="$EDGE_DATA_DIR/Default/Preferences"

echo "📝 配置 Edge 开发者模式..."

# 使用 AppleScript 打开 Edge 并导航到扩展页面
osascript << EOF
tell application "Microsoft Edge"
    activate
    delay 2
    tell application "System Events"
        keystroke "d" using command down
        delay 0.5
        keystroke "l" using command down
        delay 0.5
        keystroke "edge://extensions/"
        keystroke return
    end tell
end tell
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 准备完成！"
echo ""
echo "📋 接下来请手动操作（30 秒）："
echo ""
echo "1. Edge 已打开到扩展页面"
echo "2. 开启右上角的【开发者模式】开关"
echo "3. 点击【加载已解压的扩展程序】"
echo "4. 选择文件夹：$PLUGIN_DIR"
echo "5. 看到插件图标出现即成功"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示：插件加载后"
echo "   - 打开任意网页测试"
echo "   - 点击插件图标 → 保存整页"
echo "   - 或选中文字右键 → 保存到 Notion"
echo ""
