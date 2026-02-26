# 系统工具能力提升计划

**更新时间**: 2026-02-26 04:20 PST
**目标**: 围绕四个学习领域增强能力

---

## 🎯 四个核心目标

1. **AI 开发**（AI Development）
2. **金融投资**（Financial Investment）
3. **具身智能开发**（Embodied AI Development）
4. **AI 产品经理**（AI Product Management）

---

## ✅ 已就绪能力（17/58）

### 通用工具
| 工具 | 用途 | 关联目标 |
|------|------|---------|
| `exec` | Shell 命令执行 | 全部 |
| `github` | GitHub 操作（issues/PR/CI） | AI 开发 |
| `gh-issues` | 自动修复 GitHub issues | AI 开发 |
| `feishu-*` | 飞书文档/云盘/权限/知识库 | AI 产品 |
| `message` | 消息发送 | 全部 |
| `sessions_*` | 会话管理/子代理 | 全部 |

### 系统控制
| 工具 | 用途 | 关联目标 |
|------|------|---------|
| `media-downloader` | qBittorrent 下载管理 | 全部 |
| `screen-automation` | 屏幕截图/UI 自动化 | 具身智能 |
| `system-manager` | 系统监控/进程管理 | 全部 |
| `computer-control` (MCP) | 鼠标/键盘/屏幕控制 | 具身智能 |

### 内容处理
| 工具 | 用途 | 关联目标 |
|------|------|---------|
| `summarize` | URL/播客/文件摘要 | 全部 |
| `video-frames` | 视频帧提取 | 具身智能 |
| `weather` | 天气预报 | 全部 |
| `openai-whisper` | 本地语音转文字 | 全部 |

### 通信
| 工具 | 用途 | 关联目标 |
|------|------|---------|
| `himalaya` | IMAP/SMTP 邮件管理 | AI 产品 |

---

## ⏳ 可快速启用的能力（无需 API Key）

### 优先级 P0 - 立即启用（5 分钟内）

#### 1. Apple Notes (`apple-notes`)
- **用途**: 快速记录学习笔记、灵感
- **依赖**: AppleScript 脚本（已创建）
- **关联目标**: 全部（知识管理）
- **状态**: ✅ 脚本已创建 `~/.openclaw/scripts/apple-notes.sh`
- **注意**: 首次使用需要授予 Notes 访问权限

#### 2. Apple Reminders (`apple-reminders`)
- **用途**: 学习任务提醒、复习计划
- **依赖**: `remindctl` CLI
- **关联目标**: 全部（学习管理）
- **状态**: ✅ 已安装 (`brew install steipete/tap/remindctl`)
- **注意**: 需要在 系统设置 > 隐私与安全性 > 提醒事项 中授权

#### 3. Blog Watcher (`blogwatcher`)
- **用途**: 监控 AI/技术博客更新
- **依赖**: 需要找到替代方案（npm 包不存在）
- **关联目标**: AI 开发、AI 产品
- **状态**: ⏳ 暂缓（使用 RSS + 现有工具替代）
- **替代方案**: 使用 `media-downloader` 技能的 RSS 功能

#### 4. Coding Agent (`coding-agent`)
- **用途**: 委托编码任务给 Codex/Claude
- **依赖**: 无（使用现有 API）
- **关联目标**: AI 开发
- **状态**: ⏳ 需要配置（技能 missing）

### 优先级 P1 - 按需启用

#### 5. Gemini CLI (`gemini`)
- **用途**: 快速问答、摘要、生成
- **依赖**: Google API Key（免费额度充足）
- **关联目标**: AI 开发、AI 产品
- **成本**: 免费额度 60 次/分钟

#### 6. Nano PDF (`nano-pdf`)
- **用途**: PDF 文档编辑（论文、报告）
- **依赖**: 无
- **关联目标**: 全部（文献处理）

#### 7. Model Usage (`model-usage`)
- **用途**: 追踪模型使用成本
- **依赖**: 无
- **关联目标**: 全部（成本优化）

---

## 🚫 暂不启用的能力（低优先级）

| 工具 | 原因 |
|------|------|
| 1password | 已有钥匙串，无需额外密码管理器 |
| Bear Notes | 已有 Apple Notes，避免重复 |
| BluOS | 无 BluOS 设备 |
| BlueBubbles | 已有飞书，iMessage 非必需 |
| CamSnap | 无 RTSP 摄像头 |
| Discord | 无 Discord 使用需求 |
| Eight Sleep | 无 Eight Sleep 设备 |
| GIF Grep | 非学习相关 |
| Google Places | 非学习相关 |
| iMsg | 已有飞书 |
| MCPorter | MCP 已手动配置 |

---

## 📋 执行计划

### 第一阶段：基础增强（今天完成）
1. ✅ 验证 GitHub/Gitee 同步（已完成）
2. ✅ 创建 Apple Notes 脚本（`apple-notes.sh`）
3. ✅ 安装 `remindctl`（Apple Reminders）
4. ⏳ 配置 Brave Search API（需要用户获取 Key）
5. ⏳ 授权 Reminders 访问（系统设置）

### 第二阶段：学习工具（本周内）
1. ✅ 使用 `media-downloader` RSS 功能监控博客（替代 blogwatcher）
2. ⏳ 配置 RSS 订阅（AI/金融/机器人领域）
3. ⏳ 创建学习提醒系统（remindctl + cron）

### 第三阶段：高级能力（按需）
1. ⏳ Gemini CLI（多模型对比）- 需要 Google API Key
2. ⏳ Nano PDF（论文处理）- 技能 missing
3. ⏳ Model Usage（成本追踪）- 技能 missing

---

## 🔍 能力映射表

| 目标 | 核心能力 | 支持工具 |
|------|---------|---------|
| **AI 开发** | 代码、GitHub、文档 | github, gh-issues, coding-agent, summarize |
| **金融投资** | 数据、分析、新闻 | web_search, blogwatcher, himalaya |
| **具身智能** | 屏幕控制、视觉 | screen-automation, computer-control, video-frames |
| **AI 产品** | 文档、沟通、需求 | feishu-*, message, apple-notes, remindctl |

---

## 💡 立即可用的增强

### 1. 学习笔记自动化
```bash
# 创建学习笔记
echo "今天学习了 Transformer 架构" | memo create "AI 学习"
```

### 2. 复习提醒
```bash
# 设置 3 天后复习
remindctl add "复习 Transformer" --date "2026-03-01"
```

### 3. 技术博客监控
```bash
# 监控 AI 博客
blogwatcher subscribe https://openai.com/blog
```

---

## 下一步行动

### 立即可用（已就绪）
1. ✅ **Apple Notes** - 脚本已创建，首次使用需授权
2. ✅ **Apple Reminders** - 已安装，需系统授权
3. ✅ **GitHub/Gitee** - 已验证，同步正常

### 需要你操作（2 分钟）
1. ⏳ **Brave API Key** → 获取后运行 `~/.openclaw/scripts/configure-brave.sh`
2. ⏳ **系统授权** → 系统设置 > 隐私与安全性 > 提醒事项 > 允许 Terminal/OpenClaw

### 可选增强（按需）
1. ⏳ RSS 订阅配置（AI/金融/机器人博客）
2. ⏳ Gemini CLI（多模型对比）
3. ⏳ Coding Agent（编码任务委托）

**原则**: 每个工具安装不超过 3 步，不延长实现链条。
