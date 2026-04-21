# Gateway 启动钩子方案

> **创建日期**: 2026-03-01  
> **状态**: 📝 方案设计（待实施）  
> **优先级**: 中  
> **预计工时**: 2-3 小时

---

## 背景

在 OpenClaw 日常使用中，遇到以下问题：

1. **配置被意外修改** - OpenClaw 更新或误操作导致配置文件损坏
2. **启动失败无回滚** - Gateway 启动失败后需要手动排查和恢复
3. **缺乏启动前检查** - 没有预检机制，问题在启动后才暴露
4. **无启动日志追踪** - 启动过程缺乏详细记录

**解决方案**: 实现 Gateway 启动钩子，在启动前后自动执行保护、检查和回滚操作。

---

## 改进方案总览

| 改进编号 | 名称 | 优先级 | 状态 |
|---------|------|--------|------|
| 改进一 | 增强配置保护检查 | 🔴 高 | 📝 待实施 |
| 改进二 | 健康状态预检 | 🟡 中 | 📝 待实施 |
| 改进三 | 通知机制 | 🟢 低 | 📝 待实施 |
| 改进四 | 自动回滚机制 | 🔴 高 | 📝 待实施 |

---

## 改进一：增强配置保护检查

### 目标
在 Gateway 启动前自动检查和保护关键配置文件，防止配置损坏导致启动失败。

### 功能设计

#### 1.1 Vector Memory 配置保护
**功能**: 运行现有的 `protect-config.sh` 脚本

**检查项**:
- ✅ Vector Memory 核心文件完整性
- ✅ ChromaDB 记忆集合验证
- ✅ OpenClaw 版本变更检测
- ✅ 自动恢复被修改的文件

**实现方式**:
```bash
if [ -x "$OPENCLAW_BASE/skills/vector-memory/scripts/protect-config.sh" ]; then
    "$OPENCLAW_BASE/skills/vector-memory/scripts/protect-config.sh" >> "$LOG_FILE" 2>&1
fi
```

#### 1.2 关键配置文件语法验证
**功能**: 验证 JSON 配置文件语法正确性

**检查文件**:
- `~/.openclaw/openclaw.json` - 全局配置
- `~/.openclaw/agents/main/agent/config.json` - Agent 配置
- `~/.openclaw/agents/main/agent/channels.json` - 通道配置

**实现方式**:
```bash
for file in "${config_files[@]}"; do
    if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo "❌ 配置语法错误：$(basename "$file")"
        exit 1
    fi
done
```

#### 1.3 备份目录管理
**功能**: 确保备份目录存在并统计备份文件

**实现方式**:
```bash
BACKUP_DIR="$HOME/.openclaw/backups/gateway"
mkdir -p "$BACKUP_DIR"
backup_count=$(ls -1 "$BACKUP_DIR"/*.bak 2>/dev/null | wc -l)
echo "📦 可用备份数量：$backup_count"
```

### 代码实现

**文件**: `~/.openclaw/scripts/gateway-start-hook.sh`

```bash
#!/bin/bash
# Gateway 启动钩子 - 改进一：增强配置保护

set -e

OPENCLAW_BASE="$HOME/.openclaw"
LOG_FILE="$OPENCLAW_BASE/logs/gateway-start.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

enhanced_config_check() {
    log "运行增强配置保护检查..."
    
    # 1. Vector Memory 配置保护
    if [ -x "$OPENCLAW_BASE/skills/vector-memory/scripts/protect-config.sh" ]; then
        log "运行 Vector Memory 配置保护..."
        "$OPENCLAW_BASE/skills/vector-memory/scripts/protect-config.sh" >> "$LOG_FILE" 2>&1
        log "✅ Vector Memory 配置检查完成"
    else
        log "⚠️  Vector Memory 保护脚本不存在"
    fi
    
    # 2. 关键配置文件语法验证
    log "检查关键配置文件..."
    local config_files=(
        "$OPENCLAW_BASE/openclaw.json"
        "$OPENCLAW_BASE/agents/main/agent/config.json"
        "$OPENCLAW_BASE/agents/main/agent/channels.json"
    )
    
    for file in "${config_files[@]}"; do
        if [ -f "$file" ]; then
            if python3 -m json.tool "$file" > /dev/null 2>&1; then
                log "✅ 配置语法正常：$(basename "$file")"
            else
                log "❌ 配置语法错误：$(basename "$file")"
                return 1
            fi
        else
            log "⚠️  配置文件不存在：$(basename "$file")"
        fi
    done
    
    # 3. 备份目录检查
    local BACKUP_DIR="$OPENCLAW_BASE/backups/gateway"
    if [ -d "$BACKUP_DIR" ]; then
        local backup_count=$(ls -1 "$BACKUP_DIR"/*.bak 2>/dev/null | wc -l)
        log "✅ 备份目录存在 ($backup_count 个备份文件)"
    else
        log "⚠️  备份目录不存在，创建中..."
        mkdir -p "$BACKUP_DIR"
    fi
    
    return 0
}

# 主流程
if enhanced_config_check; then
    log "✅ 配置检查通过"
else
    log "❌ 配置检查失败，中止启动"
    exit 1
fi
```

### 测试步骤

```bash
# 1. 创建测试脚本
cat > ~/.openclaw/scripts/test-gateway-hook.sh << 'EOF'
#!/bin/bash
~/.openclaw/scripts/gateway-start-hook.sh --check-only
EOF
chmod +x ~/.openclaw/scripts/test-gateway-hook.sh

# 2. 运行测试
~/.openclaw/scripts/test-gateway-hook.sh

# 3. 查看日志
tail -50 ~/.openclaw/logs/gateway-start.log
```

---

## 改进四：自动回滚机制

### 目标
当 Gateway 启动失败时，自动回滚到最近的可用配置，减少人工干预。

### 功能设计

#### 4.1 启动状态追踪
**功能**: 记录每次启动的成功/失败状态

**实现方式**:
```bash
STATE_FILE="$BACKUP_DIR/.last_success"

# 启动成功时记录
date +%s > "$STATE_FILE"

# 检查上次启动时间
if [ -f "$STATE_FILE" ]; then
    last_success=$(cat "$STATE_FILE")
    now=$(date +%s)
    diff=$((now - last_success))
    
    if [ $diff -lt 300 ]; then  # 5 分钟内
        echo "✅ 上次启动成功 ($(date -r "$last_success" '+%H:%M:%S'))"
    fi
fi
```

#### 4.2 错误检测
**功能**: 分析启动日志，检测异常模式

**实现方式**:
```bash
# 检查最近的错误日志
if [ -f "$LOG_FILE" ]; then
    recent_errors=$(tail -100 "$LOG_FILE" | grep -c "ERROR\|❌" || true)
    if [ "$recent_errors" -gt 5 ]; then
        log "⚠️  检测到 $recent_errors 个错误，可能需要回滚"
        echo "$(date +%s)" > "$BACKUP_DIR/.need_rollback"
    fi
fi
```

#### 4.3 启动前备份
**功能**: 每次启动前自动创建备份

**实现方式**:
```bash
# 创建启动前备份
backup_file="$BACKUP_DIR/openclaw.json.bak.$(date +%Y%m%d_%H%M%S)"
if [ -f "$OPENCLAW_BASE/openclaw.json" ]; then
    cp "$OPENCLAW_BASE/openclaw.json" "$backup_file"
    log "已创建备份：$backup_file"
fi
```

#### 4.4 自动回滚流程
**功能**: 检测到启动失败时自动回滚

**实现方式**:
```bash
do_rollback() {
    log "执行回滚..."
    
    local latest_backup=$(ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | head -1)
    
    if [ -n "$latest_backup" ]; then
        log "回滚到：$latest_backup"
        cp "$latest_backup" "$OPENCLAW_BASE/openclaw.json"
        log "✅ 回滚完成"
        rm -f "$BACKUP_DIR/.need_rollback"
        return 0
    else
        log "❌ 无可用备份"
        return 1
    fi
}

start_gateway() {
    # 检查是否需要回滚
    if [ -f "$BACKUP_DIR/.need_rollback" ]; then
        log "⚠️  检测到回滚标记，执行自动回滚..."
        if do_rollback; then
            log "✅ 回滚成功，继续启动"
        else
            log "❌ 回滚失败，请手动干预"
            exit 1
        fi
    fi
    
    # 启动 Gateway
    if openclaw gateway start "$@" >> "$LOG_FILE" 2>&1; then
        log "✅ Gateway 启动成功"
        date +%s > "$STATE_FILE"
        return 0
    else
        log "❌ Gateway 启动失败"
        echo "$(date +%s)" > "$BACKUP_DIR/.need_rollback"
        return 1
    fi
}
```

### 代码实现

**文件**: `~/.openclaw/scripts/gateway-start-hook.sh` (完整版本)

```bash
#!/bin/bash
# Gateway 启动钩子 v2.0 - 完整实现
# 功能：启动前配置保护 + 健康检查 + 失败回滚

set -e

OPENCLAW_BASE="$HOME/.openclaw"
LOG_FILE="$OPENCLAW_BASE/logs/gateway-start.log"
BACKUP_DIR="$OPENCLAW_BASE/backups/gateway"
STATE_FILE="$BACKUP_DIR/.last_success"
MAX_LOG_SIZE=10485760  # 10MB

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 改进一：增强配置检查
enhanced_config_check() {
    # ... (见改进一代码)
    return 0
}

# 改进四：自动回滚
auto_rollback() {
    log "检查是否需要回滚..."
    
    # 检查上次启动是否成功
    if [ -f "$STATE_FILE" ]; then
        local last_success=$(cat "$STATE_FILE")
        local now=$(date +%s)
        local diff=$((now - last_success))
        
        if [ $diff -lt 300 ]; then
            log "✅ 上次启动成功 ($(date -r "$last_success" '+%H:%M:%S'))"
            return 0
        fi
    fi
    
    # 检查 Gateway 进程是否异常退出
    if pgrep -f "openclaw-gateway" > /dev/null; then
        log "⚠️  Gateway 已在运行，跳过回滚检查"
        return 0
    fi
    
    # 检查最近的错误日志
    if [ -f "$LOG_FILE" ]; then
        local recent_errors=$(tail -100 "$LOG_FILE" | grep -c "ERROR\|❌" || true)
        if [ "$recent_errors" -gt 5 ]; then
            log "⚠️  检测到 $recent_errors 个错误，可能需要回滚"
            offer_rollback
        fi
    fi
    
    return 0
}

do_rollback() {
    log "执行回滚..."
    
    local latest_backup=$(ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | head -1)
    
    if [ -n "$latest_backup" ]; then
        log "回滚到：$latest_backup"
        cp "$latest_backup" "$OPENCLAW_BASE/openclaw.json"
        log "✅ 回滚完成"
        rm -f "$BACKUP_DIR/.need_rollback"
        return 0
    else
        log "❌ 无可用备份"
        return 1
    fi
}

start_gateway() {
    log "启动 Gateway..."
    
    # 检查是否需要回滚
    if [ -f "$BACKUP_DIR/.need_rollback" ]; then
        log "⚠️  检测到回滚标记，执行自动回滚..."
        if do_rollback; then
            log "✅ 回滚成功，继续启动"
        else
            log "❌ 回滚失败，请手动干预"
            exit 1
        fi
    fi
    
    # 创建启动前备份
    local backup_file="$BACKUP_DIR/openclaw.json.bak.$(date +%Y%m%d_%H%M%S)"
    if [ -f "$OPENCLAW_BASE/openclaw.json" ]; then
        cp "$OPENCLAW_BASE/openclaw.json" "$backup_file"
        log "已创建备份：$backup_file"
    fi
    
    # 清理旧日志（如果过大）
    if [ -f "$LOG_FILE" ]; then
        local log_size=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ "$log_size" -gt "$MAX_LOG_SIZE" ]; then
            log "日志文件过大，轮换中..."
            mv "$LOG_FILE" "${LOG_FILE}.old"
        fi
    fi
    
    # 启动 Gateway
    if openclaw gateway start "$@" >> "$LOG_FILE" 2>&1; then
        log "✅ Gateway 启动成功"
        date +%s > "$STATE_FILE"
        return 0
    else
        log "❌ Gateway 启动失败"
        log "查看日志：tail -100 $LOG_FILE"
        echo "$(date +%s)" > "$BACKUP_DIR/.need_rollback"
        return 1
    fi
}

# 主流程
main() {
    log "========================================"
    log "  Gateway 启动钩子 v2.0"
    log "  $(date '+%Y-%m-%d %H:%M:%S')"
    log "========================================"
    
    # 改进一：增强配置检查
    if ! enhanced_config_check; then
        log "❌ 配置检查失败，中止启动"
        exit 1
    fi
    
    # 改进四：回滚检查
    auto_rollback
    
    # 启动 Gateway
    if start_gateway "$@"; then
        log "✅ 启动流程完成"
        exit 0
    else
        log "❌ 启动流程失败"
        exit 1
    fi
}

main "$@"
```

### 测试步骤

```bash
# 1. 测试正常启动
~/.openclaw/scripts/gateway-start-hook.sh

# 2. 测试回滚机制
# 2.1 创建回滚标记
touch ~/.openclaw/backups/gateway/.need_rollback

# 2.2 运行启动钩子（应自动回滚）
~/.openclaw/scripts/gateway-start-hook.sh

# 3. 查看备份
ls -lt ~/.openclaw/backups/gateway/

# 4. 查看日志
tail -100 ~/.openclaw/logs/gateway-start.log
```

---

## 文件结构

```
~/.openclaw/
├── scripts/
│   ├── gateway-start-hook.sh    # 启动钩子主脚本
│   └── test-gateway-hook.sh     # 测试脚本
├── backups/gateway/
│   ├── openclaw.json.bak.*      # 配置文件备份（带时间戳）
│   ├── .last_success            # 上次成功启动时间戳
│   └── .need_rollback           # 回滚标记（需要时创建）
├── logs/
│   ├── gateway-start.log        # 启动日志
│   └── config-protect.log       # 配置保护日志
└── workspace/
    └── GATEWAY_HOOK_SCHEME.md   # 本文档
```

---

## 实施计划

### 阶段一：改进一（配置保护）
**工时**: 1 小时

1. [ ] 创建 `gateway-start-hook.sh` 基础框架
2. [ ] 集成 Vector Memory 配置保护
3. [ ] 添加 JSON 语法验证
4. [ ] 创建备份目录
5. [ ] 测试配置检查功能

### 阶段二：改进四（自动回滚）
**工时**: 1-2 小时

1. [ ] 添加启动状态追踪
2. [ ] 实现错误检测逻辑
3. [ ] 实现启动前备份
4. [ ] 实现自动回滚流程
5. [ ] 测试回滚机制

### 阶段三：集成测试
**工时**: 30 分钟

1. [ ] 正常启动测试
2. [ ] 配置错误测试
3. [ ] 启动失败回滚测试
4. [ ] 日志验证

### 阶段四：文档和培训
**工时**: 30 分钟

1. [ ] 编写用户文档
2. [ ] 编写故障排查指南
3. [ ] 更新保护协议

---

## 紧急命令（实施后）

```bash
# 手动回滚
alias openclaw-rollback='cp $(ls -t ~/.openclaw/backups/gateway/openclaw.json.bak.* | head -1) ~/.openclaw/openclaw.json && openclaw gateway restart'

# 查看启动状态
cat ~/.openclaw/backups/gateway/.last_success | xargs -I{} date -r{} '+%Y-%m-%d %H:%M:%S'

# 查看回滚标记
if [ -f ~/.openclaw/backups/gateway/.need_rollback ]; then echo "需要回滚"; else echo "正常"; fi

# 查看备份数量
ls -1 ~/.openclaw/backups/gateway/*.bak 2>/dev/null | wc -l
```

---

## 日志示例

### 成功启动流程
```
[2026-03-01 21:00:00] ========================================
[2026-03-01 21:00:00]   Gateway 启动钩子 v2.0
[2026-03-01 21:00:00] ========================================
[2026-03-01 21:00:00] 运行增强配置保护检查...
[2026-03-01 21:00:01] ✅ Vector Memory 配置检查完成
[2026-03-01 21:00:01] ✅ 配置语法正常：openclaw.json
[2026-03-01 21:00:01] ✅ 备份目录存在 (5 个备份文件)
[2026-03-01 21:00:01] 检查是否需要回滚...
[2026-03-01 21:00:01] ✅ 上次启动成功 (20:55:00)
[2026-03-01 21:00:01] 启动 Gateway...
[2026-03-01 21:00:02] 已创建备份：openclaw.json.bak.20260301_210001
[2026-03-01 21:00:10] ✅ Gateway 启动成功
[2026-03-01 21:00:10] ✅ 启动流程完成
```

### 失败回滚流程
```
[2026-03-01 21:00:00] 启动 Gateway...
[2026-03-01 21:00:01] ⚠️  检测到回滚标记，执行自动回滚...
[2026-03-01 21:00:01] 回滚到：openclaw.json.bak.20260301_205500
[2026-03-01 21:00:02] ✅ 回滚完成
[2026-03-01 21:00:02] ✅ 回滚成功，继续启动
[2026-03-01 21:00:10] ✅ Gateway 启动成功
```

---

## 风险与注意事项

### 风险
1. **回滚到旧配置** - 可能丢失最新的有效配置
2. **备份占用空间** - 长期运行可能积累大量备份
3. **误判启动失败** - 网络延迟等临时问题可能触发回滚

### 缓解措施
1. **保留修改版本** - 回滚前保存当前版本为 `.modified` 后缀
2. **定期清理备份** - 保留最近 7 天的备份
3. **错误阈值调整** - 根据实际运行情况调整错误检测阈值

### 注意事项
1. **首次运行** - 首次运行前手动创建初始备份
2. **权限问题** - 确保脚本有执行权限
3. **日志监控** - 定期检查启动日志，及时发现潜在问题

---

## 后续改进（可选）

### 改进二：健康状态预检
- [ ] 检查磁盘空间（<90% 使用率）
- [ ] 检查端口占用（18789）
- [ ] 检查模型 API 连通性
- [ ] 检查 Gateway 进程状态

### 改进三：通知机制
- [ ] 启动失败时发送飞书通知
- [ ] 回滚发生时发送告警
- [ ] 定期发送健康报告（每日/每周）
- [ ] 集成到安全员系统

---

## 相关文件

| 文件 | 状态 | 用途 |
|------|------|------|
| `~/.openclaw/workspace/PROTECTION_PROTOCOL.md` | ✅ 已存在 | 保护协议总纲 |
| `~/.openclaw/skills/vector-memory/scripts/protect-config.sh` | ✅ 已存在 | Vector Memory 配置保护 |
| `~/.openclaw/scripts/gateway-start-hook.sh` | 📝 待创建 | 启动钩子主脚本 |
| `~/.openclaw/scripts/test-gateway-hook.sh` | 📝 待创建 | 测试脚本 |
| `~/.openclaw/workspace/GATEWAY_HOOK_SCHEME.md` | ✅ 本文档 | 方案设计 |

---

**下次实施时**:
1. 阅读本文档了解设计方案
2. 按实施计划逐步执行
3. 每阶段完成后运行测试
4. 更新本文档记录实施情况

**最后更新**: 2026-03-01 21:22 PST
