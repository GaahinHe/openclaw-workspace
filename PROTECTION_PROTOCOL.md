# 保护协议 - OpenClaw 安全操作规范

> **创建日期**：2026-02-25
> **目的**：防止误操作导致服务中断，确保任务执行透明

---

## 一、任务执行透明度

### 1.1 进度汇报规则

| 任务时长 | 汇报频率 | 汇报内容 |
|---------|---------|---------|
| < 1 分钟 | 完成后一次性汇报 | 结果 + 关键步骤 |
| 1-5 分钟 | 开始 + 完成 | 预期时间 + 实际结果 |
| 5-30 分钟 | 每 25% 进度汇报 | 当前步骤 + 剩余估计 |
| > 30 分钟 | 每 10 分钟汇报 | 进度 + 是否有阻塞 |

### 1.2 阻塞检测

**定义**：任何操作超过预期时间 2 倍视为阻塞

**处理方式**：
1. 立即停止当前操作
2. 报告阻塞点和可能原因
3. 提供继续/跳过/回滚选项
4. 等待用户确认

### 1.3 汇报模板

```
【任务进度】{任务名称}
━━━━━━━━━━━━━━━━━━━━
📊 进度：{X}%
✅ 已完成：{步骤列表}
🔄 进行中：{当前步骤}
⏳ 等待中：{依赖项}
⚠️  风险：{潜在问题}
━━━━━━━━━━━━━━━━━━━━
预计完成：{时间}
```

---

## 二、配置文件保护

### 2.1 修改前必做

```bash
# 1. 创建带时间戳的备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d_%H%M%S)

# 2. 验证 JSON 语法
cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null

# 3. 记录修改日志
echo "[$(date)] 修改原因：XXX" >> ~/.openclaw/config-changes.log
```

### 2.2 禁止直接修改的文件

以下文件修改前**必须**获得用户明确确认：

| 文件 | 风险等级 | 影响 |
|------|---------|------|
| `~/.openclaw/openclaw.json` | 🔴 高 | 全局配置，影响所有功能 |
| `~/.openclaw/mcp-servers/*.js` | 🔴 高 | MCP 服务器，影响工具能力 |
| `~/.openclaw/skills/*/SKILL.md` | 🟡 中 | 技能定义，影响特定功能 |
| `~/.openclaw/extensions/*/index.ts` | 🔴 高 | 插件代码，可能破坏扩展 |

### 2.3 回滚程序

```bash
# 快速回滚到最近备份
alias openclaw-rollback='cp $(ls -t ~/.openclaw/openclaw.json.bak.* | head -1) ~/.openclaw/openclaw.json && openclaw gateway restart'
```

---

## 三、服务健康监控

### 3.1 健康检查脚本

创建 `~/.openclaw/scripts/healthcheck.sh`：

```bash
#!/bin/bash
set -e

LOG_FILE=~/.openclaw/logs/healthcheck.log
ALERT_FILE=~/.openclaw/logs/health-alerts.log

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

check_gateway_process() {
    if pgrep -f "openclaw-gateway" > /dev/null; then
        echo "[$(timestamp)] ✅ Gateway 进程正常" >> $LOG_FILE
        return 0
    else
        echo "[$(timestamp)] ❌ Gateway 进程不存在" >> $ALERT_FILE
        return 1
    fi
}

check_gateway_port() {
    if curl -s http://127.0.0.1:18789 > /dev/null 2>&1; then
        echo "[$(timestamp)] ✅ Gateway 端口响应正常" >> $LOG_FILE
        return 0
    else
        echo "[$(timestamp)] ❌ Gateway 端口无响应" >> $ALERT_FILE
        return 1
    fi
}

check_model_api() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        https://dashscope.aliyuncs.com/compatible-mode/v1/models 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "[$(timestamp)] ✅ 模型 API 连接正常 (HTTP $response)" >> $LOG_FILE
        return 0
    else
        echo "[$(timestamp)] ❌ 模型 API 连接失败 (HTTP $response)" >> $ALERT_FILE
        return 1
    fi
}

check_disk_space() {
    local usage=$(df -h ~/.openclaw | awk 'NR==2 {print $5}' | tr -d '%')
    if [ "$usage" -lt 90 ]; then
        echo "[$(timestamp)] ✅ 磁盘空间正常 (使用 ${usage}%)" >> $LOG_FILE
        return 0
    else
        echo "[$(timestamp)] ⚠️  磁盘空间紧张 (使用 ${usage}%)" >> $ALERT_FILE
        return 1
    fi
}

# 主检查流程
echo "=== 健康检查开始 $(timestamp) ===" >> $LOG_FILE

check_gateway_process
check_gateway_port
check_model_api
check_disk_space

echo "=== 健康检查完成 ===" >> $LOG_FILE
```

### 3.2 定时任务

```bash
# 添加到 crontab (crontab -e)
# 每 15 分钟检查一次健康状态
*/15 * * * * ~/.openclaw/scripts/healthcheck.sh

# 每天早上 8 点发送健康报告
0 8 * * * cat ~/.openclaw/logs/healthcheck.log | tail -50
```

### 3.3 自动恢复

创建 `~/.openclaw/scripts/auto-recover.sh`：

```bash
#!/bin/bash

# 如果 Gateway 挂了，自动重启
if ! pgrep -f "openclaw-gateway" > /dev/null; then
    echo "[$(date)] 检测到 Gateway 停止，尝试重启..." >> ~/.openclaw/logs/auto-recover.log
    openclaw gateway restart
    sleep 5
    
    if pgrep -f "openclaw-gateway" > /dev/null; then
        echo "[$(date)] ✅ 自动重启成功" >> ~/.openclaw/logs/auto-recover.log
    else
        echo "[$(date)] ❌ 自动重启失败，需要人工干预" >> ~/.openclaw/logs/auto-recover.log
        # 这里可以添加通知逻辑
    fi
fi
```

---

## 四、操作审计日志

### 4.1 审计日志格式

在 `memory/audit-log.md` 记录：

```markdown
## 2026-02-25

### [14:30] 配置文件修改
- **操作**：修改 `openclaw.json` 的模型配置
- **原因**：添加新的 API 提供商
- **变更**：
  ```diff
  + "bailian": { "baseUrl": "..." }
  ```
- **影响**：所有会话使用新模型
- **回滚**：使用备份 `openclaw.json.bak.20260225_143000`
- **状态**：✅ 已验证

### [15:45] 服务重启
- **操作**：`openclaw gateway restart`
- **原因**：配置更新后需要重载
- **影响**：约 10 秒服务不可用
- **状态**：✅ 重启成功
```

### 4.2 高风险操作确认清单

执行以下操作前必须逐项确认：

- [ ] 已创建配置文件备份
- [ ] 已告知用户操作内容和影响
- [ ] 已准备回滚方案
- [ ] 已确认当前无关键任务在执行
- [ ] 已记录到审计日志

---

## 五、紧急联系人机制

### 5.1 紧急停止命令

```bash
# 一键停止所有 OpenClaw 进程
alias openclaw-emergency-stop='pkill -f openclaw && launchctl bootout gui/$UID/ai.openclaw.gateway'

# 一键恢复
alias openclaw-emergency-recover='openclaw gateway start && sleep 3 && openclaw status'
```

### 5.2 故障排查清单

当服务异常时按顺序检查：

1. **进程状态**：`ps aux | grep openclaw`
2. **端口占用**：`lsof -i :18789`
3. **日志检查**：`tail -100 /tmp/openclaw/openclaw-*.log`
4. **配置语法**：`cat ~/.openclaw/openclaw.json | python3 -m json.tool`
5. **网络连通**：`curl -I https://dashscope.aliyuncs.com`

---

## 六、定期维护

### 6.1 每周检查

- [ ] 清理旧备份文件（保留最近 7 天）
- [ ] 检查日志文件大小
- [ ] 验证健康检查脚本运行正常
- [ ] 审查审计日志中的高风险操作

### 6.2 每月检查

- [ ] 更新 OpenClaw 到最新稳定版
- [ ] 检查技能/插件更新
- [ ] 审查并更新保护协议
- [ ] 测试回滚程序是否有效

---

## 协议生效

**本协议自创建之日起生效**

所有后续操作必须遵守上述规范。如有特殊情况需要突破协议，必须：
1. 说明紧急原因
2. 获得用户明确同意
3. 事后补充完整记录

**最后更新**：2026-02-25
**下次审查**：2026-03-25
