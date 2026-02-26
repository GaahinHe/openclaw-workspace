# 能力监控任务

**机制**: OpenClaw HEARTBEAT（原生心跳检查）
**频率**: 系统心跳间隔（约 30-60 分钟）
**触发**: 系统自动心跳 poll 时

---

## 📋 检查清单

### 1. Brave Search API 状态
- [ ] 检查环境变量 `BRAVE_API_KEY`
- [ ] 检查钥匙串 `brave-search-api`
- [ ] 状态变化时 → 通知用户

### 2. 新工具检测
- [ ] 检查常用工具：`remindctl`, `cliclick`, `gh`, `node`, `npm`
- [ ] 对比 `~/.openclaw/logs/known-tools.json`
- [ ] 发现新工具 → 通知用户 + 更新清单

### 3. 技能状态
- [ ] 执行 `openclaw skills list`
- [ ] 对比上次 ready 技能列表
- [ ] 发现新技能 → 通知用户 + 说明用途

### 4. 任务系统
- [ ] 检查待完成任务数
- [ ] 检查是否有超时任务（>24h）
- [ ] 有阻塞 → 提醒用户

### 5. 系统权限
- [ ] 测试 remindctl 是否能运行
- [ ] 测试 Apple Notes 脚本
- [ ] 权限变化 → 通知用户

---

## 📬 通知策略

### 有变化时（主动通知）
在心跳回复中直接说：

```
📦 **发现新能力**

**名称**: {tool_name}
**功能**: {description}
**状态**: ✅ 已就绪

**示例用法**:
"{example_command}"

需要我演示一下吗？
```

### 无变化时（静默）
回复：`HEARTBEAT_OK`

### 有阻塞时（请求确认）
```
⚠️ **需要确认**

**任务**: {task_name}
**阻塞**: {blocker}

**建议方案**:
1. {option_1}
2. {option_2}

请告诉我如何继续。
```

---

## 🕐 深度检查（每天一次）

**时间**: 凌晨 03:00-04:00 之间的心跳

**额外检查**:
- [ ] 生成能力日报
- [ ] 对比昨天状态
- [ ] 更新能力路线图进度
- [ ] 记录到审计日志

**触发条件**:
```bash
if [ "$(date +%H)" = "03" ] && [ ! -f ~/.openclaw/logs/daily-check-done-$(date +%Y%m%d) ]; then
  # 执行深度检查
  ~/.openclaw/scripts/capability-watch.sh deep
  touch ~/.openclaw/logs/daily-check-done-$(date +%Y%m%d)
fi
```

---

## 📊 状态记录

**文件**: `~/.openclaw/logs/capability-state.json`

```json
{
  "last_check": "2026-02-26T04:45:00Z",
  "brave_api": "missing",
  "tools": ["remindctl", "cliclick", "gh", "node", "npm"],
  "skills_ready": ["github", "gh-issues", "feishu-doc", ...],
  "task_count": 1,
  "check_count": 1
}
```

---

## 🎯 用户触发命令

用户可以随时说：

```
"检查新能力"          → 立即执行能力检查
"有什么新功能？"      → 列出最近新增的能力
"能力进度如何？"      → 显示总体进度报告
"下一步增强什么？"    → 获取建议的下一个能力
"启用{能力名称}"      → 开始配置指定能力
```

---

## ⚠️ 注意事项

1. **不要频繁打扰**: 只在有实质变化时通知
2. **简洁汇报**: 通知要简短，包含关键信息
3. **提供下一步**: 每次通知都要有明确的建议
4. **记录审计**: 所有检查都要记录到 audit-log.md

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `HEARTBEAT.md` | 本文档 - 心跳检查指南 |
| `scripts/capability-watch.sh` | 检查脚本 |
| `logs/capability-state.json` | 状态记录 |
| `logs/known-tools.json` | 已知工具清单 |
| `logs/audit-log.md` | 审计日志 |
| `workspace/CAPABILITY_ROADMAP.md` | 能力路线图 |

---

**最后更新**: 2026-02-26 04:45 PST
**下次检查**: 系统下次心跳时
