# 🤖 自动能力监控系统 v2

**设计时间**: 2026-02-26 04:45 PST
**机制**: HEARTBEAT + sessions_spawn（不用 cron）

---

## 🎯 为什么不用 cron

| 方案 | 优点 | 缺点 |
|------|------|------|
| **cron** | 简单、成熟 | 独立进程、无上下文、通知复杂 |
| **HEARTBEAT** | ✅ 内置、有上下文、可对话 | 需要心跳触发 |
| **sessions_spawn** | ✅ 独立会话、不阻塞主会话 | 需要配置子代理 |
| **hooks** | ✅ 事件驱动 | 适合特定事件，不适合定时 |

**最佳方案**: **HEARTBEAT 机制** + **主动会话检查**

---

## 📋 方案 A: HEARTBEAT 机制（推荐）

### 原理
OpenClaw 内置心跳检查，定期询问「有需要注意的吗？」

### 配置
**文件**: `~/.openclaw/workspace/HEARTBEAT.md`

```markdown
# HEARTBEAT 检查清单

## 定期检查项（每次心跳执行）

### 1. 能力监控
- [ ] 检查 Brave API 配置
- [ ] 检查新工具安装
- [ ] 检查新技能就绪
- [ ] 对比上次状态

### 2. 任务追踪
- [ ] 查看待完成任务
- [ ] 检查超时任务

### 3. 主动汇报
- [ ] 如果有新能力 → 主动通知用户
- [ ] 如果有阻塞 → 请求用户确认
- [ ] 如果一切正常 → 回复 HEARTBEAT_OK

## 检查频率
- 默认：系统心跳间隔（可配置）
- 深度检查：每天一次（通过日期判断）
```

### 优点
- ✅ OpenClaw 原生支持
- ✅ 有对话上下文
- ✅ 可以直接发消息给用户
- ✅ 不需要额外进程

### 实现
```bash
# 心跳触发时自动执行
~/.openclaw/scripts/capability-watch.sh check

# 如果有变化，在心跳回复中通知用户
```

---

## 📋 方案 B: sessions_spawn 定时子代理

### 原理
创建一个持久监控子代理，独立运行并定期检查

### 配置
**文件**: `~/.openclaw/agents/capability-monitor/agent.json`

```json
{
  "id": "capability-monitor",
  "name": "能力监控员",
  "mode": "session",
  "task": "每 4 小时检查一次能力状态，发现变化时通知主会话",
  "model": "bailian/qwen3.5-plus",
  "thinking": "low"
}
```

### 启动命令
```bash
# 主会话中启动监控子代理
openclaw sessions spawn \
  --agent capability-monitor \
  --mode session \
  --task "监控能力变化，每 4 小时检查一次，发现变化时通知主会话"
```

### 优点
- ✅ 独立会话，不阻塞主会话
- ✅ 可以持续运行
- ✅ 有专门的记忆和上下文

### 缺点
- ⚠️ 需要额外配置子代理
- ⚠️ 增加资源占用

---

## 📋 方案 C: 混合方案（最佳）

### 设计
1. **日常检查**: HEARTBEAT 机制（轻量）
2. **深度检查**: sessions_spawn 子代理（每天一次）
3. **事件触发**: hooks（配置变更时）

### 配置

#### 1. HEARTBEAT.md（日常检查）
```markdown
# 能力监控检查清单

## 快速检查（每次心跳）
- [ ] Brave API 状态
- [ ] 新工具检测（which 命令）
- [ ] 任务系统状态

## 如果有变化
→ 主动通知用户 + 记录审计日志

## 如果无变化
→ 回复 HEARTBEAT_OK
```

#### 2. 深度检查子代理（每天一次）
```bash
# 在心跳中触发
if [ "$(date +%H)" = "03" ]; then
  sessions spawn --mode run --task "深度能力检查"
fi
```

#### 3. Hook 监听配置变更
```javascript
// hooks/capability-change.js
watch('~/.openclaw/openclaw.json', () => {
  // 配置变更时触发检查
  capability_watch();
});
```

---

## 🚀 推荐实现：HEARTBEAT 方案

### 步骤 1: 更新 HEARTBEAT.md

```markdown
# 能力监控任务

**检查频率**: 每次心跳（系统默认间隔）

## 检查清单

### 1. Brave Search API
- 状态：⏳ 待配置
- 检查：钥匙串或环境变量
- 如果已配置 → 更新状态 + 通知用户

### 2. 新工具检测
- 检查命令：which remindctl/cliclick/gh
- 对比：~/.openclaw/logs/known-tools.json
- 如果有新工具 → 通知用户 + 更新清单

### 3. 技能状态
- 检查：openclaw skills list
- 对比：上次记录的 ready 技能
- 如果有新技能 → 通知用户 + 说明用途

### 4. 任务系统
- 检查待完成任务
- 如果有超时任务 → 提醒用户

## 通知策略

### 立即通知（有变化时）
在心跳回复中直接说：
```
📦 发现新能力！

名称：remindctl
功能：Apple Reminders CLI
建议：可以用"remindctl add 任务 --date 日期"设置提醒

需要我帮你设置第一个提醒吗？
```

### 静默（无变化时）
回复：`HEARTBEAT_OK`

## 深度检查（每天 03:00）
如果当前时间是凌晨 3 点，执行：
```bash
~/.openclaw/scripts/capability-watch.sh deep
```
并生成日报。
```

### 步骤 2: 简化监控脚本

```bash
#!/bin/bash
# capability-watch.sh - 简化版，供 HEARTBEAT 调用

# 检查逻辑...
# 如果有变化，输出 JSON 格式的变化报告
# 如果无变化，输出 HEARTBEAT_OK
```

### 步骤 3: 心跳触发

用户可以在心跳提示中配置：
```
Read HEARTBEAT.md if it exists. Follow it strictly. 
If nothing needs attention, reply HEARTBEAT_OK.
```

系统会自动定期触发心跳检查。

---

## 📊 对比总结

| 特性 | HEARTBEAT | sessions_spawn | 混合方案 |
|------|-----------|----------------|----------|
| 复杂度 | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| 资源占用 | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| 灵活性 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 推荐度 | ✅ | ⚠️ | ✅✅ |

**推荐**: 先用 **HEARTBEAT 方案**，如果需要再扩展混合方案。

---

## 🎯 下一步

### 立即实现（HEARTBEAT 方案）
1. ✅ 更新 HEARTBEAT.md
2. ✅ 简化 capability-watch.sh
3. ⏳ 测试心跳触发
4. ⏳ 验证通知机制

### 配置命令
```bash
# 1. 更新 HEARTBEAT.md
cat > ~/.openclaw/workspace/HEARTBEAT.md << 'EOF'
# 能力监控任务
...
EOF

# 2. 测试心跳
# 在对话中等待系统心跳，或手动触发

# 3. 验证通知
# 检查是否能主动发消息
```

---

**不用 cron，用 OpenClaw 原生的 HEARTBEAT 机制！** ✅
