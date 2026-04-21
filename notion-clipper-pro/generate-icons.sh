#!/bin/bash
# 生成插件图标
# 使用 macOS 自带的 sips 命令

cd "$(dirname "$0")"

echo "🎨 正在生成图标..."

# 如果系统有 sips（macOS 自带）
if command -v sips &> /dev/null; then
    # 先创建一个临时的 PNG（使用 base64 解码）
    # 这里使用一个简单的黑色正方形作为占位符
    
    # 128x128
    sips -z 128 128 icons/icon.svg --out icons/icon128.png 2>/dev/null || \
    echo "⚠️  SVG 转 PNG 失败，请使用在线工具转换"
    
    # 缩放其他尺寸
    if [ -f icons/icon128.png ]; then
        sips -z 48 48 icons/icon128.png --out icons/icon48.png
        sips -z 32 32 icons/icon128.png --out icons/icon32.png
        sips -z 16 16 icons/icon128.png --out icons/icon16.png
        echo "✅ 图标生成完成"
    else
        echo "⚠️  请手动创建 PNG 图标文件"
        echo "   1. 访问 https://cloudconvert.com/svg-to-png"
        echo "   2. 上传 icons/icon.svg"
        echo "   3. 下载并保存为 icon128.png"
    fi
else
    echo "❌ 未找到 sips 命令"
    echo "请使用在线工具转换 SVG 到 PNG"
fi

echo ""
echo "📁 图标文件位置：$(pwd)/icons/"
