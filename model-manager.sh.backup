#!/bin/bash
# Model Manager - 鲁棒的大模型选择与健康检查工具

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"

echo -e "${BLUE}🤖 Model Manager - 大模型管理${NC}"
echo "================================"

# 1. 检查 LM Studio 状态
check_lmstudio() {
    echo -e "\n${BLUE}📍 检查 LM Studio 本地模型...${NC}"

    if lsof -i :1234 &>/dev/null; then
        echo -e "${GREEN}✅ LM Studio 服务器运行中${NC}"

        # 获取模型列表
        MODELS=$(curl -s "http://localhost:1234/v1/models" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(', '.join([m['id'] for m in d.get('data',[])]))" 2>/dev/null || echo "无法获取模型列表")

        if [ -n "$MODELS" ]; then
            echo -e "${GREEN}   可用模型: $MODELS${NC}"
        else
            echo -e "${YELLOW}   ⚠️  服务器运行但无法获取模型列表${NC}"
        fi
    else
        echo -e "${RED}❌ LM Studio 服务器未运行${NC}"
        echo -e "${YELLOW}   请在 LM Studio 应用中点击 'Start Server'${NC}"
    fi
}

# 2. 检查 Minimax API
check_minimax() {
    echo -e "\n${BLUE}☁️ 检查 MiniMax API...${NC}"

    API_KEY=$(grep -A2 '"minimax:default"' "$AUTH_FILE" 2>/dev/null | grep '"key"' | sed 's/.*"key": *"\([^"]*\)".*/\1/' || echo "")

    if [ -z "$API_KEY" ]; then
        echo -e "${RED}❌ 未找到 MiniMax API Key${NC}"
        return 1
    fi

    # 测试连接
    echo "   测试连接..."

    RESPONSE=$(curl -s -w "\n%{http_code}" "https://api.minimax.io/v1/models" \
        -H "Authorization: Bearer $API_KEY" \
        --max-time 15 2>/dev/null || echo "")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "401" ]; then
        echo -e "${GREEN}✅ MiniMax API 可达 (HTTP $HTTP_CODE)${NC}"
        return 0
    elif [ "$HTTP_CODE" = "404" ]; then
        echo -e "${YELLOW}⚠️  MiniMax API 返回 404，可能 endpoint 错误${NC}"
        echo "   尝试其他 endpoint..."
        return 1
    else
        echo -e "${RED}❌ MiniMax API 不可达 (HTTP $HTTP_CODE)${NC}"
        return 1
    fi
}

# 3. 健康检查
health_check() {
    echo -e "\n${BLUE}🩺 健康检查...${NC}"

    PASS=0
    FAIL=0

    if lsof -i :1234 &>/dev/null; then
        echo -e "${GREEN}✅ lm-studio: 健康${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ lm-studio: 离线${NC}"
        ((FAIL++))
    fi

    if check_minimax &>/dev/null; then
        echo -e "${GREEN}✅ minimax: 健康${NC}"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠️  minimax: 可能离线${NC}"
        ((FAIL++))
    fi

    echo -e "\n${BLUE}状态: $PASS 通过, $FAIL 失败${NC}"
}

# 4. 显示当前配置
show_config() {
    echo -e "\n${BLUE}📋 当前模型配置...${NC}"

    PRIMARY=$(grep -A3 '"model":' "$CONFIG_FILE" | grep '"primary"' | sed 's/.*: *"\([^"]*\)".*/\1/')
    FALLBACKS=$(grep -A10 '"fallbacks":' "$CONFIG_FILE" | grep '"' | grep -v 'fallbacks' | sed 's/.*"\([^"]*\)".*/\1/' | tr '\n' ' ')

    echo -e "   Primary:  ${GREEN}$PRIMARY${NC}"
    echo -e "   Fallbacks: ${YELLOW}$FALLBACKS${NC}"
}

# 5. 智能路由建议
suggest_routing() {
    echo -e "\n${BLUE}💡 智能路由建议...${NC}"

    LM_RUNNING=false
    MM_HEALTHY=false

    lsof -i :1234 &>/dev/null && LM_RUNNING=true
    check_minimax &>/dev/null && MM_HEALTHY=true

    if $LM_RUNNING && $MM_HEALTHY; then
        echo -e "   推荐: ${GREEN}优先使用本地 (快)，复杂任务用 MiniMax${NC}"
    elif $LM_RUNNING; then
        echo -e "   推荐: ${YELLOW}仅使用本地模型${NC}"
    elif $MM_HEALTHY; then
        echo -e "   推荐: ${YELLOW}仅使用 MiniMax (本地离线)${NC}"
    else
        echo -e "   推荐: ${RED}⚠️  所有模型离线，请检查网络和 LM Studio${NC}"
    fi
}

# 6. 重启 OpenClaw Gateway
restart_gateway() {
    echo -e "\n${BLUE}🔄 重启 OpenClaw Gateway...${NC}"
    openclaw gateway restart
    echo -e "${GREEN}✅ Gateway 已重启${NC}"
}

# 主菜单
main() {
    case "${1:-menu}" in
        check-lm)
            check_lmstudio
            ;;
        check-mm)
            check_minimax
            ;;
        health)
            health_check
            ;;
        config)
            show_config
            suggest_routing
            ;;
        restart)
            restart_gateway
            ;;
        all)
            check_lmstudio
            check_minimax
            health_check
            show_config
            suggest_routing
            ;;
        menu|*)
            echo -e "\n用法: $0 <命令>"
            echo ""
            echo "命令:"
            echo "  check-lm   检查 LM Studio"
            echo "  check-mm   检查 MiniMax API"
            echo "  health     综合健康检查"
            echo "  config     显示配置"
            echo "  restart    重启 Gateway"
            echo "  all        全部检查"
            ;;
    esac
}

main "$@"
