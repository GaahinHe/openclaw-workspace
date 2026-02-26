# 能力配置状态

**更新时间**: 2026-02-26 04:15 PST

---

## ✅ 已就绪能力

### 1. GitHub 同步
- **状态**: ✅ 已认证
- **账户**: GaahinHe
- **Token 范围**: repo, workflow, read:org, project, audit_log, write:packages
- **Remote 配置**: 
  - origin: https://github.com/GaahinHe/openclaw-workspace.git
  - gitee: https://gitee.com/GaahinHe/openclaw-workspace.git
- **测试**: `gh auth status` ✓

### 2. Gitee 同步
- **状态**: ✅ Git Remote 已配置
- **Remote**: https://gitee.com/GaahinHe/openclaw-workspace.git
- **注意**: Gitee CLI 未安装，但 git push/pull 可正常工作

### 3. 模型配置
- **状态**: ✅ 已配置
- **提供商**: Bailian (阿里云)
- **可用模型**: qwen3.5-plus, qwen3-max, glm-5, kimi-k2.5 等 8 个模型
- **上下文窗口**: 最高 1,000,000 tokens

### 4. 飞书集成
- **状态**: ✅ 已启用
- **连接模式**: WebSocket
- **AppID**: cli_a9f5a86d79f9dcd1

### 5. 系统工具
- **状态**: ✅ 可用
- **exec**: Shell 命令执行
- **文件操作**: read/write/edit
- **屏幕控制**: screenshot, cliclick (已安装)

---

## ⏳ 待配置能力

### 1. Brave Search API (web_search / web_fetch)
- **状态**: ⏳ 需要 API Key
- **免费额度**: 2,000 次查询/月
- **用途**: 网络搜索、网页内容提取

#### 获取步骤 (2 分钟):
1. 访问 https://brave.com/search/api/
2. 点击 "Get Started" 或 "Sign Up"
3. 注册账户（支持 Google/GitHub 快捷登录）
4. 进入 Dashboard → API Keys
5. 创建新 Key，复制保存

#### 配置命令 (获取 Key 后执行):
```bash
openclaw configure --section web
# 按提示粘贴 API Key
```

**影响**: 配置后可使用 `web_search` 和 `web_fetch` 工具

---

## 📋 配置优先级

| 优先级 | 能力 | 依赖 | 预计时间 |
|--------|------|------|---------|
| P0 | Brave Search API | 用户获取 Key | 2 分钟 |
| P1 | 浏览器控制 (browser) | Chrome 扩展 | 5 分钟 (可选) |
| P2 | Node 配对 (nodes) | OpenClaw 桌面应用 | 10 分钟 (可选) |

---

## 下一步行动

1. **立即**: 获取 Brave Search API Key (用户操作)
2. **自动**: 配置完成后测试 web_search / web_fetch
3. **可选**: 根据需要配置浏览器控制

---

## 验证命令

```bash
# GitHub 状态
gh auth status

# Git Remote
cd ~/.openclaw/workspace && git remote -v

# OpenClaw 状态
openclaw status

# 测试 web_search (配置后)
# 在对话中说："搜索一下今天的人工智能新闻"
```
