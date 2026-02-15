#!/bin/bash

# 项目管理系统 - 一键部署脚本
# 位置：~/.openclaw/workspace/ddns-deployment/deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/../project-management-system"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ============ 检查依赖 ============

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker Desktop"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_warn "docker-compose 未找到，尝试使用 docker compose..."
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker 未运行，请启动 Docker Desktop"
        exit 1
    fi
    
    log_info "Docker 检查通过"
}

check_project() {
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "项目目录不存在: $PROJECT_DIR"
        exit 1
    fi
    
    if [ ! -f "$PROJECT_DIR/docker-compose.yml" ]; then
        log_error "docker-compose.yml 不存在"
        exit 1
    fi
    
    log_info "项目目录检查通过"
}

# ============ 部署步骤 ============

start_services() {
    log_info "启动 Docker 服务..."
    
    cd "$PROJECT_DIR"
    
    # 拉取最新镜像
    docker-compose pull
    
    # 启动服务
    docker-compose up -d
    
    log_info "服务启动中..."
    sleep 10
    
    # 检查状态
    docker-compose ps
}

check_services() {
    log_info "检查服务状态..."
    
    local services=("frontend" "backend" "oceanbase" "kafka")
    local failed=0
    
    for svc in "${services[@]}"; do
        status=$(docker inspect -f '{{.State.Running}}' "${PROJECT_DIR//\//\/}-${svc}-1" 2>/dev/null || echo "false")
        if [ "$status" = "true" ]; then
            log_info "  ✓ $svc 运行正常"
        else
            log_warn "  ✗ $svc 可能异常，请检查日志"
            failed=1
        fi
    done
    
    return $failed
}

show_access_info() {
    local domain="${1:-your-domain.com}"
    
    echo ""
    echo "========================================"
    echo "     部署完成！访问信息如下："
    echo "========================================"
    echo ""
    echo "  🌐 前端界面: http://pm.${domain}:3000"
    echo "  🔌 后端 API:  http://api.${domain}:8080"
    echo "  📚 Swagger:   http://api.${domain}:8080/doc.html"
    echo ""
    echo "========================================"
    echo ""
    echo "常用命令："
    echo "  查看日志: cd $PROJECT_DIR && docker-compose logs -f"
    echo "  重启服务: cd $PROJECT_DIR && docker-compose restart"
    echo "  停止服务: cd $PROJECT_DIR && docker-compose down"
    echo ""
}

# ============ 主程序 ============

main() {
    echo "========================================"
    echo "     项目管理系统 - 部署脚本"
    echo "========================================"
    echo ""
    
    check_docker
    check_project
    start_services
    
    if check_services; then
        show_access_info
    else
        log_warn "部分服务可能需要更多时间启动，请稍后查看日志"
        echo ""
        docker-compose logs
    fi
}

# ============ 参数处理 ============

case "$1" in
    -h|--help)
        echo "用法: $0 [命令]"
        echo ""
        echo "命令:"
        echo "  start     启动所有服务"
        echo "  stop      停止所有服务"
        echo "  restart   重启所有服务"
        echo "  logs      查看日志"
        echo "  status    检查状态"
        echo ""
        exit 0
        ;;
    stop)
        cd "$PROJECT_DIR" && docker-compose down
        log_info "服务已停止"
        ;;
    restart)
        cd "$PROJECT_DIR" && docker-compose restart
        log_info "服务已重启"
        ;;
    logs)
        cd "$PROJECT_DIR" && docker-compose logs -f
        ;;
    status)
        cd "$PROJECT_DIR" && docker-compose ps
        ;;
    *)
        main
        ;;
esac
