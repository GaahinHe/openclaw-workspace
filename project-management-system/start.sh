#!/bin/bash
# 项目管理系统一键启动脚本

set -e

echo "=============================================="
echo "  项目管理系统 - 一键启动脚本"
echo "=============================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Java
check_java() {
    if ! command -v java &> /dev/null; then
        echo -e "${RED}❌ Java 未安装${NC}"
        echo "请安装 Java 21: brew install openjdk@21"
        exit 1
    fi
    echo -e "${GREEN}✅ Java 已安装${NC}"
}

# 检查 Node
check_node() {
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js 未安装${NC}"
        echo "请安装 Node.js: brew install node@20"
        exit 1
    fi
    echo -e "${GREEN}✅ Node.js 已安装${NC}"
}

# 检查 Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️ Docker 未安装${NC}"
        echo "请下载安装 Docker Desktop: https://www.docker.com/products/docker-desktop/"
        echo ""
        read -p "是否跳过 Docker 启动中间件? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        return 1
    fi
    echo -e "${GREEN}✅ Docker 已安装${NC}"
    return 0
}

# 启动中间件
start_infrastructure() {
    echo ""
    echo "=============================================="
    echo "  1. 启动中间件 (Docker)"
    echo "=============================================="
    
    cd "$(dirname "$0")"
    
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
    elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
        docker compose up -d
    else
        echo -e "${RED}Docker Compose 未安装${NC}"
        return 1
    fi
    
    echo ""
    echo "中间件启动完成:"
    echo "  - OceanBase: localhost:2881"
    echo "  - Kafka: localhost:9092"
    echo "  - Redis: localhost:6379"
}

# 启动后端
start_backend() {
    echo ""
    echo "=============================================="
    echo "  2. 启动后端服务"
    echo "=============================================="
    
    cd "$(dirname "$0")/backend"
    
    if [ ! -f "mvnw" ]; then
        echo "下载 Maven Wrapper..."
        mvn -N io.takari:maven:wrapper
    fi
    
    echo "启动后端服务..."
    ./mvnw spring-boot:run &
    BACKEND_PID=$!
    
    echo "后端服务 PID: $BACKEND_PID"
    echo "访问地址: http://localhost:8080"
    echo "Swagger 文档: http://localhost:8080/doc.html"
}

# 启动前端
start_frontend() {
    echo ""
    echo "=============================================="
    echo "  3. 启动前端服务"
    echo "=============================================="
    
    cd "$(dirname "$0")/frontend"
    
    echo "安装依赖..."
    npm install
    
    echo "启动前端服务..."
    npm run dev &
    FRONTEND_PID=$!
    
    echo "前端服务 PID: $FRONTEND_PID"
    echo "访问地址: http://localhost:3000"
}

# 主函数
main() {
    echo "检查环境..."
    check_java
    check_node
    has_docker=$(check_docker && echo "true" || echo "false")
    
    if [ "$has_docker" = "true" ]; then
        read -p "是否启动中间件 (Docker)? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            start_infrastructure
        fi
    fi
    
    read -p "是否启动后端服务? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_backend
    fi
    
    read -p "是否启动前端服务? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_frontend
    fi
    
    echo ""
    echo "=============================================="
    echo "  启动完成!"
    echo "=============================================="
    echo ""
    echo "服务状态:"
    echo "  - 前端: http://localhost:3000"
    echo "  - 后端: http://localhost:8080"
    echo "  - Swagger: http://localhost:8080/doc.html"
    echo ""
    echo "默认账号:"
    echo "  - admin / 123456 (管理员)"
    echo "  - test / 123456 (普通用户)"
    echo ""
}

main "$@"
