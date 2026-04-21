# OpenCode 安装与配置记录

**日期**: 2026-03-14
**状态**: ✅ 已完成安装和配置

---

## ✅ 已完成

### 1. 安装 OpenCode
```bash
brew install opencode
```

**版本**: 1.2.10
**安装位置**: `/opt/homebrew/Cellar/opencode/1.2.10`

### 2. API Key 配置
**来源**: 从 `~/.openclaw/openclaw.json` 找到
**Key**: `sk-sp-7ef346ba2ea54f34ba471c2a2270af37`

### 3. 配置文件
**位置**: `~/.opencode/config.json`
```json
{
  "$schema": "https://opencode.ai/config.json",
  "env": {
    "OPENAI_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "OPENAI_API_KEY": "sk-sp-7ef346ba2ea54f34ba4f34ba471c2a2270af37"
  }
}
```

---

## 📊 当前状态

### ✅ 可用功能
- OpenCode TUI 界面
- 单条命令执行 (`opencode run`)
- 使用免费模型 (opencode/big-pickle 等)

### ⚠️ 限制说明
OpenCode 的模型列表来自 Models.dev 预定义列表，**不支持直接调用阿里云百炼的 Qwen 模型**。

当前配置下：
- 环境变量已设置阿里云百炼 API Key
- 但 OpenCode 只允许使用其预定义模型（如 `opencode/big-pickle`, `openai/gpt-4o` 等）

### 💡 替代方案
如需使用阿里云百炼的 Qwen 模型，建议：
1. 使用 OpenClaw 内置的 bailian 提供者（已配置）
2. 使用 LM Studio 本地部署
3. 直接使用 curl/API 调用

---

## 🚀 使用方式

### 启动 TUI
```bash
opencode
```

### 运行单条命令
```bash
opencode run "解释一下这个项目"
```

### 查看可用模型
```bash
opencode models
```

### 指定模型
```bash
opencode run -m openai/gpt-4o "帮我写代码"
```

---

## 🔗 相关文档

- OpenCode 文档：https://opencode.ai/docs
- 配置文件：~/.opencode/config.json
- 认证存储：~/.local/share/opencode/auth.json
