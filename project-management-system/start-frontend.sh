#!/bin/bash
# 前端启动脚本

cd "$(dirname "$0")/frontend"

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "正在安装前端依赖..."
    npm install
fi

echo ""
echo "=============================================="
echo "  启动前端开发服务器..."
echo "=============================================="
echo ""
echo "访问地址: http://localhost:3000"
echo ""

npm run dev
