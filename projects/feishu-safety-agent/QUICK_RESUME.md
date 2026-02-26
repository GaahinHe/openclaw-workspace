# 飞书安全员配置 - 快速恢复指南

> **一句话总结**：等待用户在飞书后台配置两个应用的事件订阅和 verifyToken

---

## 下次开始时执行

```bash
# 1. 查看项目状态
cat ~/.openclaw/workspace/projects/feishu-safety-agent/PROJECT.md

# 2. 检查当前配置
cat ~/.openclaw/agents/safety-guard-01/agent/channels.json | grep verifyToken
cat ~/.openclaw/agents/safety-guard-02/agent/channels.json | grep verifyToken

# 3. 如果已有 verifyToken，重启并测试
openclaw gateway restart
~/.openclaw/agents/safety-guard-01/scripts/safety-agent.sh test-notify
~/.openclaw/agents/safety-guard-02/scripts/safety-agent.sh test-notify
```

---

## 用户需要做什么

1. 登录飞书开发者后台
2. 配置两个应用的事件订阅
3. 获取 verifyToken
4. 发送给 Hans TheBot

---

## 配置模板

收到 verifyToken 后，更新这两个文件：

**安全员甲**: `~/.openclaw/agents/safety-guard-01/agent/channels.json`
```json
{
  "verifyToken": "用户提供的令牌甲"
}
```

**安全员乙**: `~/.openclaw/agents/safety-guard-02/agent/channels.json`
```json
{
  "verifyToken": "用户提供的令牌乙"
}
```

---

**项目状态**: 🟡 等待用户配置飞书后台
