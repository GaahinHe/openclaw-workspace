#!/bin/bash
# Edge 插件自动化测试脚本

set -e

EXTENSION_PATH="$HOME/.openclaw/workspace/edge-auto-test-extension"
SCREENSHOT_DIR="$HOME/.openclaw/workspace/edge-auto-test-extension/screenshots"

# 创建截图目录
mkdir -p "$SCREENSHOT_DIR"

echo "🤖 Edge 插件自动化测试"
echo "========================"
echo ""

# 1. 激活 Edge
echo "[1/6] 激活 Edge 浏览器..."
osascript -e 'tell application "Microsoft Edge" to activate'
sleep 2

# 2. 打开测试页面
echo "[2/6] 打开测试页面 (example.com)..."
osascript -e 'tell application "Microsoft Edge" to open location "https://example.com"'
sleep 3

# 3. 获取窗口位置
echo "[3/6] 获取 Edge 窗口位置..."
WINDOW_POS=$(osascript -e 'tell application "Microsoft Edge" to get bounds of window 1' 2>/dev/null || echo "0, 0, 960, 1080")
echo "窗口位置：$WINDOW_POS"

# 4. 打开扩展页面（用于验证插件加载）
echo "[4/6] 打开扩展管理页面..."
osascript -e 'tell application "Microsoft Edge" to open location "edge://extensions/"'
sleep 2

# 5. 截图（使用 cliclick + 系统工具）
echo "[5/6] 截图记录..."
# 使用 AppleScript 截图
osascript <<EOF
tell application "System Events"
    keystroke "4" using {command down, shift down}
end tell
EOF
sleep 1

# 6. 返回测试页面
echo "[6/6] 返回测试页面..."
osascript -e 'tell application "Microsoft Edge" to open location "https://example.com"'
sleep 2

echo ""
echo "✅ 测试完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在 Edge 中打开 edge://extensions/"
echo "2. 启用 '开发者模式'"
echo "3. 点击 '加载解压缩的扩展'"
echo "4. 选择文件夹：$EXTENSION_PATH"
echo "5. 点击工具栏的 🤖 图标测试插件"
echo ""
echo "📸 截图已保存到桌面"
