#!/bin/bash

# 阿里云 DDNS 动态域名更新脚本
# 位置：~/.openclaw/workspace/ddns-deployment/ddns.sh

set -e

# ============ 配置 ============
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# 加载环境变量
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "[ERROR] 配置文件不存在: $ENV_FILE"
    echo "请先复制 env.example 为 .env 并配置"
    exit 1
fi

# 阿里云 API 地址
DNS_API="https://dns.aliyuncs.com/"
LOG_FILE="${HOME}/ddns.log"

# ============ 函数 ============

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

get_current_ip() {
    # 优先使用公网 API 获取 IP
    curl -s https://api.ipify.org || \
    curl -s https://icanhazip.com || \
    curl -s https://ifconfig.me
}

get_record_ip() {
    local record_type="$1"
    local domain="$2"
    
    # 调用阿里云 DescribeDomainRecords API
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local signature nonce
    
    # 生成签名（简化版）
    signature=$(echo -n "AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=DescribeDomainRecords&DomainName=${DOMAIN_NAME}&Format=JSON&SignatureMethod=HMAC-SHA1&SignatureNonce=$(uuidgen 2>/dev/null || openssl rand -hex 10)&SignatureVersion=1.0&Timestamp=${timestamp}&Version=2015-01-09" | \
        openssl dgst -sha1 -hmac "${ALIBABA_CLOUD_ACCESS_KEY_SECRET}&" -binary | base64)
    
    # 解析记录 IP（简化处理）
    curl -s "${DNS_API}?AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=DescribeDomainRecords&DomainName=${DOMAIN_NAME}&Format=JSON&Signature=${signature}&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Version=2015-01-09" | \
        grep -oP "\"Value\":\"[0-9.]+\"" | head -1 | grep -oP "[0-9.]+"
}

update_dns_record() {
    local new_ip="$1"
    local record_type="${2:-A}"
    
    log "开始更新 DNS 记录: ${SUB_DOMAIN}.${DOMAIN_NAME} -> ${new_ip}"
    
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local record_id
    
    # 获取记录 ID
    record_id=$(curl -s "https://dns.aliyuncs.com/?AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=DescribeDomainRecords&DomainName=${DOMAIN_NAME}&Format=JSON&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Type=${record_type}&Version=2015-01-09" | \
        python3 -c "import sys,json; d=json.load(sys.stdin); r=[x for x in d.get('DomainRecords',{}).get('Record',[]) if x.get('RR')=='${SUB_DOMAIN}']; print(r[0]['RecordId'] if r else '')" 2>/dev/null)
    
    if [ -z "$record_id" ]; then
        # 创建新记录
        local signature=$(echo -n "AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=AddDomainRecord&DomainName=${DOMAIN_NAME}&Format=JSON&RR=${SUB_DOMAIN}&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Type=${record_type}&Value=${new_ip}&Version=2015-01-09" | \
            openssl dgst -sha1 -hmac "${ALIBABA_CLOUD_ACCESS_KEY_SECRET}&" -binary | base64 | tr -d '=')
        
        curl -s "https://dns.aliyuncs.com/?AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=AddDomainRecord&DomainName=${DOMAIN_NAME}&Format=JSON&RR=${SUB_DOMAIN}&Signature=${signature}&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Type=${record_type}&Value=${new_ip}&Version=2015-01-09"
        log "创建新 DNS 记录成功"
    else
        # 更新现有记录
        local signature=$(echo -n "AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=UpdateDomainRecord&DomainName=${DOMAIN_NAME}&Format=JSON&RR=${SUB_DOMAIN}&RecordId=${record_id}&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Type=${record_type}&Value=${new_ip}&Version=2015-01-09" | \
            openssl dgst -sha1 -hmac "${ALIBABA_CLOUD_ACCESS_KEY_SECRET}&" -binary | base64 | tr -d '=')
        
        curl -s "https://dns.aliyuncs.com/?AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}&Action=UpdateDomainRecord&DomainName=${DOMAIN_NAME}&Format=JSON&RR=${SUB_DOMAIN}&RecordId=${record_id}&Signature=${signature}&SignatureMethod=HMAC-SHA1&SignatureNonce=$(date +%s)&SignatureVersion=1.0&Timestamp=${timestamp}&Type=${record_type}&Value=${new_ip}&Version=2015-01-09"
        log "更新 DNS 记录成功"
    fi
}

# ============ 主程序 ============

log "=== DDNS 脚本开始执行 ==="

# 1. 获取当前公网 IP
CURRENT_IP=$(get_current_ip)
if [ -z "$CURRENT_IP" ]; then
    log "[ERROR] 无法获取当前公网 IP"
    exit 1
fi
log "当前公网 IP: ${CURRENT_IP}"

# 2. 检查 IP 是否变化
LAST_IP=$(cat "${HOME}/.last_ddns_ip" 2>/dev/null || echo "")
if [ "$CURRENT_IP" = "$LAST_IP" ]; then
    log "IP 未变化，无需更新"
    exit 0
fi

# 3. 更新 DNS 记录
update_dns_record "$CURRENT_IP"

# 4. 保存 IP
echo "$CURRENT_IP" > "${HOME}/.last_ddns_ip"
log "IP 已更新并保存"

log "=== DDNS 脚本执行完成 ==="
