#!/bin/bash
# 项目管理系统 - 本地启动脚本（无需 Docker）

set -e

echo "=============================================="
echo "  项目管理系统 - 本地启动（无需 Docker）"
echo "=============================================="
echo ""
echo "📋 注意事项:"
echo "  - 使用 H2 内存数据库（无需安装数据库）"
echo "  - 首次启动会自动创建示例数据"
echo "  - 数据仅保存在内存中，重启会丢失"
echo ""

# 检查 Java
if ! command -v java &> /dev/null; then
    echo "❌ 错误: Java 未安装"
    echo "请安装 Java 21: brew install openjdk@21"
    exit 1
fi

echo "✅ Java 版本: $(java -version 2>&1 | head -1)"

# 检查 Maven
if ! command -v mvn &> /dev/null; then
    echo "❌ 错误: Maven 未安装"
    exit 1
fi

echo "✅ Maven 版本: $(mvn -version 2>&1 | head -1)"

# 切换到后端目录
cd "$(dirname "$0")/backend"

echo ""
echo "=============================================="
echo "  启动后端服务..."
echo "=============================================="
echo ""
echo "访问地址:"
echo "  - 应用: http://localhost:8080"
echo "  - Swagger: http://localhost:8080/doc.html"
echo "  - H2 控制台: http://localhost:8080/h2-console"
echo ""
echo "登录账号:"
echo "  - admin / 123456"
echo "  - test / 123456"
echo ""
echo "=============================================="

# 使用本地配置文件启动
mvn spring-boot:run -Dspring-boot.run.profiles=local
