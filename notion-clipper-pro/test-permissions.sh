#!/bin/bash
# 测试辅助功能权限

echo "🔍 测试辅助功能权限..."
echo ""

# 测试 1: AppleScript 控制
echo "测试 1: AppleScript 控制 Edge..."
osascript -e 'tell application "Microsoft Edge" to name' 2>&1
if [ $? -eq 0 ]; then
    echo "✅ AppleScript Edge 控制：正常"
else
    echo "❌ AppleScript Edge 控制：需要授权"
fi

# 测试 2: cliclick 鼠标控制
echo ""
echo "测试 2: cliclick 鼠标控制..."
cliclick c:0,0 2>&1
if [ $? -eq 0 ]; then
    echo "✅ cliclick 鼠标控制：正常"
else
    echo "❌ cliclick 鼠标控制：需要辅助功能权限"
fi

# 测试 3: System Events
echo ""
echo "测试 3: System Events 控制..."
osascript -e 'tell application "System Events" to keystroke "a" using command down' 2>&1
if [ $? -eq 0 ]; then
    echo "✅ System Events 控制：正常"
else
    echo "❌ System Events 控制：需要授权"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "如果以上有 ❌，请在系统设置中授权"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
