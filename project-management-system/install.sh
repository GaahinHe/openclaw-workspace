#!/bin/bash
# 项目管理系统 - 环境安装脚本

set -e

echo "=========================================="
echo "项目管理系统 - 环境安装"
echo "=========================================="

# 安装 Java 21
echo "安装 Java 21..."
brew install openjdk@21

# 配置 Java 环境变量
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zshrc
echo 'export JAVA_HOME=/opt/homebrew/opt/openjdk@21' >> ~/.zshrc

# 安装 Node.js 20
echo "安装 Node.js 20..."
brew install node@20
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc

# 安装 Maven
echo "安装 Maven..."
brew install maven

echo ""
echo "=========================================="
echo "✅ 环境安装完成！"
echo "=========================================="
echo ""
echo "请手动安装 Docker Desktop:"
echo "1. 下载: https://www.docker.com/products/docker-desktop/"
echo "2. 安装后运行 Docker Desktop"
echo "3. 执行 ./start.sh 启动项目"
echo ""
echo "或在 ~/.zshrc 中执行: source ~/.zshrc"
