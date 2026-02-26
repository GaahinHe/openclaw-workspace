# OpenClaw 能力增强计划 - 精简优化版

> **创建日期**: 2026-02-26
> **优化原则**: 最快捷、最有效、最低成本
> **移除项目**: ❌ Tushare 金融数据（用户不需要）

---

## 🎯 核心目标

**以最小成本实现最大能力提升**

| 维度 | 当前 | 目标 | 优先级 |
|------|------|------|--------|
| 网络搜索 | ❌ 不可用 | ✅ 可用 | P0 |
| 截图能力 | ❌ 权限问题 | ✅ 可用 | P0 |
| 基础工具 | 17/58 | ✅ 30+ | P1 |
| 沟通渠道 | 1 (飞书) | ✅ 2-3 | P1 |
| 自动化 | 基础 | ✅ 工作流 | P2 |
| 数据源 | 无 | ✅ 天气+RSS | P2 |

---

## 📋 精简工具链（只装最有用的）

### P0 - 立即配置（今天完成）

#### 1. 网络搜索 ⭐⭐⭐⭐⭐
**为什么必须**：没有网络搜索我就是"睁眼瞎"

```bash
# 1. 获取 API Key（免费，5 分钟）
# 访问：https://brave.com/search/api/

# 2. 配置（1 分钟）
openclaw configure --section web

# 3. 测试
web_search "OpenClaw 最新功能"
```

**成本**：$3/月（约¥22）
**效果**：✅ 可以查最新资料、新闻、文档

---

#### 2. 屏幕录制权限 ⭐⭐⭐⭐⭐
**为什么必须**：无法截图=无法帮你操作电脑

```bash
# 1. 系统设置（2 分钟）
系统设置 → 隐私与安全性 → 屏幕录制

# 2. 添加以下项
✅ Terminal.app
✅ /System/Library/CoreServices/screencaptureui.app

# 3. 重启 OpenClaw
openclaw gateway restart

# 4. 测试
~/.openclaw/skills/screen-automation/scripts/screenshot.sh
```

**成本**：免费
**效果**：✅ 可以截图、屏幕内容分析、UI 自动化

---

#### 3. 基础 CLI 工具 ⭐⭐⭐⭐
**为什么需要**：扩展我的操作能力

```bash
# 1Password（密码管理）
brew install 1password-cli
op signin

# GitHub CLI（代码管理）
brew install gh
gh auth login

# 可选：邮件客户端
brew install himalaya
```

**成本**：免费
**效果**：✅ 管理密码、操作 GitHub、收发邮件

---

### P1 - 高优先级（本周内）

#### 4. 沟通渠道扩展 ⭐⭐⭐⭐

**方案 A：Telegram（推荐）**
```bash
# 完全免费，10 分钟搞定
# 1. 找 @BotFather 创建 Bot
# 2. 获取 Token
# 3. 配置到 OpenClaw
```

**方案 B：微信（复杂，不推荐）**
- 需要 WeChaty，配置复杂
- 容易封号
- **建议跳过**

**成本**：免费
**效果**：✅ 多一个联系渠道，Telegram 更稳定

---

#### 5. 语音合成 TTS ⭐⭐⭐

**方案：Edge TTS（免费）**
```bash
# 使用微软 Edge 的免费 TTS
pip3 install edge-tts

# 测试
edge-tts --text "你好" --write-media test.mp3
```

**替代方案**：ElevenLabs（$5/月，质量好）

**成本**：免费（Edge TTS）或 $5/月
**效果**：✅ 可以用语音回复，更自然

---

#### 6. 缺失 Skills 修复 ⭐⭐⭐

**只装最有用的**：

| Skill | 用途 | 安装 | 必要性 |
|-------|------|------|--------|
| GitHub | 代码管理 | `brew install gh` | ⭐⭐⭐⭐⭐ |
| Weather | 天气查询 | 已安装，配置即可 | ⭐⭐⭐⭐ |
| 1Password | 密码管理 | `brew install 1password-cli` | ⭐⭐⭐⭐ |
| Apple Notes | 笔记管理 | 系统自带 | ⭐⭐⭐ |
| Apple Reminders | 提醒事项 | 系统自带 | ⭐⭐⭐ |

**跳过这些**（性价比低）：
- ❌ Himalaya（邮件，用飞书即可）
- ❌ 其他低频技能

**成本**：免费
**效果**：✅ 核心能力补齐

---

### P2 - 中优先级（按需）

#### 7. 数据源集成 ⭐⭐⭐

**只配置免费的**：

```bash
# 天气 API（和风天气 - 免费）
# https://dev.qweather.com/

# RSS 订阅（Feedly - 免费）
# https://feedly.com/

# 新闻（知乎热榜 - 免费 API）
# https://www.zhihu.com/api/v3/feed/topstory/hot
```

**跳过**：
- ❌ Tushare（你不需要）
- ❌ 付费新闻 API
- ❌ 专业数据库

**成本**：免费
**效果**：✅ 天气推送、资讯聚合

---

#### 8. 自动化工作流 ⭐⭐⭐

**简单方案**：
```bash
# 使用系统 cron + Shell 脚本
# 示例：每天早上 8 点发送天气和日程

# 1. 创建脚本
cat > ~/.openclaw/scripts/morning-brief.sh << 'EOF'
#!/bin/bash
# 获取天气
curl wttr.in/Beijing?format=3
# 获取日程（如果有日历集成）
# 发送飞书消息
EOF

# 2. 设置定时任务
crontab -e
# 添加：0 8 * * * ~/.openclaw/scripts/morning-brief.sh
```

**成本**：免费
**效果**：✅ 自动推送晨间简报

---

## 💰 最终成本（优化后）

| 项目 | 月费 | 年费 | 必要性 |
|------|------|------|--------|
| Brave Search | ¥22 | ¥264 | ⭐⭐⭐⭐⭐ **必须** |
| Edge TTS | 免费 | 免费 | ⭐⭐⭐⭐ 推荐 |
| Telegram | 免费 | 免费 | ⭐⭐⭐⭐ 推荐 |
| 天气 API | 免费 | 免费 | ⭐⭐⭐ 可选 |
| RSS | 免费 | 免费 | ⭐⭐⭐ 可选 |
| **总计** | **¥22** | **¥264** | |

**对比原方案**：从¥300-500/月 降至 **¥22/月** 🎉

---

## 📅 实施时间表（精简版）

### Day 1（今天）- 基础能力
- [ ] 配置 Brave Search API（5 分钟）
- [ ] 设置屏幕录制权限（5 分钟）
- [ ] 安装 1Password CLI（5 分钟）
- [ ] 安装 GitHub CLI（5 分钟）

**耗时**：20 分钟
**效果**：可以上网、截图、管理密码和代码

---

### Day 2-3 - 沟通增强
- [ ] 配置 Telegram Bot（10 分钟）
- [ ] 安装 Edge TTS（5 分钟）
- [ ] 测试语音消息（5 分钟）

**耗时**：20 分钟
**效果**：多一个联系渠道，可以语音回复

---

### Day 4-7 - 自动化
- [ ] 配置天气 API（10 分钟）
- [ ] 设置晨间简报脚本（30 分钟）
- [ ] 配置定时任务（5 分钟）

**耗时**：45 分钟
**效果**：自动推送天气和提醒

---

### Week 2 - 按需扩展
- [ ] 其他 MCP Servers（按需）
- [ ] 更多数据源（按需）
- [ ] 高级自动化（按需）

---

## ✅ 验证清单

配置完成后逐项测试：

```bash
# 1. 网络搜索
web_search "今天北京天气"

# 2. 截图
~/.openclaw/skills/screen-automation/scripts/screenshot.sh
ls -lh /tmp/Screenshot_*.png

# 3. 1Password
op whoami

# 4. GitHub
gh auth status

# 5. 天气
curl wttr.in/Beijing?format=3

# 6. TTS
edge-tts --text "测试语音" --write-media /tmp/test.mp3
```

---

## 🚨 避坑指南

### 不要装的（性价比低）
- ❌ Himalaya 邮件客户端（用飞书足够）
- ❌ Apple Notes/Reminders（除非你深度使用）
- ❌ 付费 TTS（Edge TTS 免费够用）
- ❌ 复杂的工作流引擎（先用 cron）

### 不要做的（浪费时间）
- ❌ 微信集成（容易封号，配置复杂）
- ❌ 付费数据源（免费替代足够）
- ❌ 一次性技能（使用频率低的）

### 最佳实践
- ✅ 优先用免费方案
- ✅ 优先用系统自带工具
- ✅ 优先用简单方案（cron > 复杂引擎）
- ✅ 按需扩展，不要一次性装太多

---

## 📊 效果对比

| 能力 | 优化前方案 | 优化后方案 | 差异 |
|------|-----------|-----------|------|
| 网络搜索 | ✅ Brave | ✅ Brave | 相同 |
| 截图 | ✅ 权限修复 | ✅ 权限修复 | 相同 |
| TTS | $5/月 | 免费 (Edge) | 省¥36/月 |
| 沟通渠道 | Telegram+ 微信 | Telegram | 省时间 |
| 数据源 | Tushare+ 天气+ 新闻 | 天气+RSS | 省¥200/月 |
| 自动化 | 工作流引擎 | cron 脚本 | 更简单 |
| **总成本** | **¥300-500/月** | **¥22/月** | **省 93%** |
| **配置时间** | **3-4 小时** | **1 小时** | **省 75%** |

---

## 🎯 立即执行

### 现在就做（5 分钟内）

**步骤 1**：获取 Brave API Key
```
1. 打开 https://brave.com/search/api/
2. 点击 "Get Started"
3. 注册账号（免费）
4. 创建 API Key
5. 复制 Key
```

**步骤 2**：配置到 OpenClaw
```bash
openclaw configure --section web
# 粘贴你的 API Key
```

**步骤 3**：测试
```
告诉我：web_search "今天有什么科技新闻"
```

---

### 接下来（回家后）

**步骤 4**：屏幕录制权限
```
系统设置 → 隐私与安全性 → 屏幕录制
添加 Terminal.app 和 screencaptureui.app
```

**步骤 5**：安装工具
```bash
brew install 1password-cli gh
op signin
gh auth login
```

---

## ❓ 确认问题

**请确认**：

1. ✅ **Brave Search API** - 现在就可以配置，你给我 API Key
2. ✅ **屏幕录制权限** - 回家后设置，5 分钟
3. ✅ **1Password + GitHub** - 是否需要？（密码管理和代码）
4. ✅ **Telegram** - 是否需要？（多一个联系渠道）
5. ✅ **TTS 语音** - 用免费的 Edge TTS 可以吗？

**如果以上都确认，我立即开始配置！** 🚀

---

**最后更新**: 2026-02-26 03:55
**优化原则**: 最快捷、最有效、最低成本
**维护者**: Hans TheBot
