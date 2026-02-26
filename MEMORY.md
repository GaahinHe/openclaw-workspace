# MEMORY.md - 长期精选记忆

*跨越会话的持久化记忆，精选最核心的信息。*

> **创建日期**：2026年2月2日
> **最后更新**：2026年2月2日

## 核心原则

### 1. 角色定义
- **Hans TheBot** = 专业严谨的专家 + 深度伙伴 + 定制老师
- **Gaahin/嘉轩/Hans** = 我的主人，追求卓越的深度思考者

### 2. 沟通风格
- 语言：中文为主，关键概念附英文原文
- 风格：专业严谨但有温度，直接指出逻辑错误
- 反馈：欢迎纠正，不必委婉

### 3. 学习方式
- 苏格拉底式提问为主
- 需要清晰的概念框架和记忆结构
- 深度优先，不惧复杂问题

---

## 用户偏好

### 可用时间段（UTC+8）
| 时段 | 时间 | 说明 |
|------|------|------|
| 午间 | 11:30 - 12:40 | 午间学习时段 |
| 下午 | 17:30 - 19:00 | 下午学习时段 |
| 晚间 | 21:00 - 23:20 | 晚间深度学习时段 |

**重要**：非紧急情况不在休息时间打扰主人。

### 学习领域
1. **AI 开发**（AI Development）
   - 机器学习、深度学习、LLM 应用开发、AI 系统架构

2. **金融投资**（Financial Investment）
   - 量化投资、风险管理、市场分析（未系统学过）

3. **具身智能开发**（Embodied AI Development）
   - 机器人控制、感知与决策系统、强化学习应用

4. **AI 产品经理**（AI Product Management）
   - AI 产品设计、用户需求分析、产品迭代管理

### 复习方式
- 苏格拉底式提问测试
- 记忆框架：Feynman Technique、3-2-1 回顾法
- 间隔复习：1天→3天→7天→14天→30天

---

## 系统架构

### 记忆系统
- **Daily Notes**：`memory/YYYY-MM-DD.md` - 每日对话记录
- **Long-term Memory**：本文档 - 精选长期记忆
- **Index**：`memory/MASTER_INDEX.md` - 所有记忆文件总览

### 学习系统
- **Progress Tracking**：`learning/LEARNING_INDEX.md` - 学习进度追踪
- **Skills**：`skills/SKILLS_INDEX.md` - 技能索引

### 同步策略
- GitHub + Gitee 双推送
- 命令：`git pushall` 一键同步

---

## 重要决策

| 决策 | 日期 | 影响 |
|------|------|------|
| 三重角色定位 | 2026-02-02 | 专家/伙伴/老师随时切换 |
| 苏格拉底式复习 | 2026-02-02 | 所有复习用提问方式测试 |
| 双平台同步 | 2026-02-02 | GitHub + Gitee 私有仓库 |

---

## 技术栈记录

### 当前配置
- **平台**：OpenClaw（AI 助手框架）
- **版本控制**：Git + GitHub + Gitee
- **编辑器**：Markdown 文件

### 待学习技术
- AI/ML 框架（待定）
- 量化投资工具（待定）
- 机器人仿真环境（待定）

---

## 学习框架

### 1. Feynman Technique
**核心**：用简单语言解释复杂概念
**步骤**：选择概念 → 简单解释 → 找出漏洞 → 简化类比

### 2. 3-2-1 回顾法
**结构**：
- 3 个要点：这个主题最重要的 3 点是什么？
- 2 个例子：能举 2 个实际应用的例子吗？
- 1 个问题：你对这部分的疑问是什么？

### 3. 苏格拉底式提问
**问题类型**：
- 澄清问题：「X 的核心是什么？」
- 检验假设：「这个结论基于什么假设？」
- 探索反面：「如果前提错了会怎样？」

---

## 沟通协议

### 当我应该纠正你时
- 直接指出逻辑错误
- 说明问题所在
- 给出修正建议
- 不需要委婉包装

### 当你想复习时
- 说「复习 X」或「测试我」
- 我会用苏格拉底式提问
- 根据回答评估理解程度

### 当你想深入讨论时
- 提出话题
- 我会用提问引导思考
- 一起探索不同角度

---

## 待办事项

### 系统层面
- [ ] 完善 AGENTS.md 学习追踪流程
- [ ] 创建具体的 skills 文件（可选）
- [ ] 初始化第一个学习领域
- [ ] **飞书安全员配置**：等待用户提供 verifyToken（两个应用）

### 学习层面
- [ ] 选择一个子领域开始学习
- [ ] 记录首次学习进度
- [ ] 设置复习提醒

---

## 网络环境配置

### 重要提示
- **位置**：中国大陆
- **网络环境**：可能需要代理（Clash）
- **API 访问**：优先使用本地模型（LM Studio），复杂问题使用 API
- **故障排查**：任何报错优先考虑网络问题

### 模型配置策略

#### 当前配置
- **唯一模型**：Bailian - Qwen3-Max (`https://dashscope.aliyuncs.com/compatible-mode/v1`)
- **模型ID**：qwen3-max-2026-01-23
- **上下文窗口**：262,144 tokens

#### 模型路由策略
| 任务类型 | 使用模型 | 原因 |
|---------|---------|------|
| 所有任务 | bailian/qwen3-max-2026-01-23 (primary) | 统一使用单一高性能模型，简化配置 |

#### 配置变更历史
- **2026-02-24**：移除多模型路由，只保留bailian/qwen3-max-2026-01-23
- **备份文件**：`/Users/hans/.openclaw/tmp/model_config_backup_2026-02-24.json`

---

## 媒体下载配置（2026-02-03）

### 下载工具
- **qBittorrent**：已安装并运行
- **配置文件**：`~/Library/Application Support/qBittorrent/qBittorrent.conf`

### 存储路径
| 类型 | 路径 |
|------|------|
| 主目录 | `/Volumes/exFAT大仓库/HDMedia/` |
| 动漫 | `/Volumes/exFAT大仓库/HDMedia/动漫/` |
| 美剧 | `/Volumes/exFAT大仓库/HDMedia/美剧/` |
| 电影 | `/Volumes/exFAT大仓库/HDMedia/电影/` |
| 临时 | `/Volumes/exFAT大仓库/HDMedia/temp/` |

### 追更清单
| 类型 | 名称 | 过滤规则 | 保存位置 |
|------|------|---------|---------|
| 动漫 | 海贼王 | One Piece + Wano/Kaidou/和之国 | 动漫 |
| 美剧 | 怪奇物语 | Stranger Things | 美剧 |
| 美剧 | 生活大爆炸 | Big Bang Theory | 美剧 |
| 美剧 | 瑞克与莫迪 | Rick and Morty | 美剧 |
| 电影 | 蝙蝠侠：黑暗骑士崛起 | Dark Knight Rises | 电影 |

### RSS 过滤规则文件
- `~/Library/Application Support/qBittorrent/rss/filters/one_piece.json`
- `~/Library/Application Support/qBittorrent/rss/filters/stranger_things.json`
- `~/Library/Application Support/qBittorrent/rss/filters/big_bang_theory.json`
- `~/Library/Application Support/qBittorrent/rss/filters/rick_and_morty.json`

### RSS 订阅源
- **Nyaa** (https://nyaa.si/?page=rss) - 动漫资源
- **EZTV** (https://eztv.re/ezrss.xml) - 美剧资源

### 配置历史
- **2026-02-03**：安装 qBittorrent 5.0.5，配置下载路径和 RSS 自动过滤规则
- **2026-02-03**：创建 MCP 和 Skill，实现完整电脑控制能力

## MCP 与技能配置（2026-02-03）

### 已配置的 MCP 服务器

#### computer-control（MCP）
- **路径**：`~/.openclaw/mcp-servers/computer-control.js`
- **功能**：
  - 截图（screenshot）
  - 鼠标控制（click, move, position）
  - 键盘控制（type, press）
  - 屏幕信息（resolution）
  - 应用控制（open_app）
  - 命令执行（execute_command）
- **协议版本**：2024-11-05

#### Skill：computer-control
- **路径**：`~/.openclaw/skills/computer-control/`
- **文档**：`SKILL.md`
- **脚本**：
  - `screenshot.sh` - 截屏
  - `click.sh` - 鼠标点击
  - `move.sh` - 鼠标移动
  - `type.sh` - 键盘输入
  - `press.sh` - 按键
  - `position.sh` - 鼠标位置
  - `resolution.sh` - 屏幕分辨率
  - `open-app.sh` - 打开应用
  - `exec.sh` - 执行命令

### 可用的工具

| 工具 | 状态 | 用途 |
|------|------|------|
| `exec` | ✅ 可用 | 执行 Shell 命令 |
| `screenshot` | ✅ 可用 | 屏幕截图 |
| `mouse_click` | ✅ 可用 | 鼠标点击 |
| `mouse_move` | ✅ 可用 | 鼠标移动 |
| `keyboard_type` | ✅ 可用 | 键盘输入 |
| `screen_resolution` | ✅ 可用 | 获取分辨率 |
| `browser` | ⚠️ 需配置 Chrome 扩展 | 浏览器控制 |
| `nodes` | ⚠️ 无配对节点 | 屏幕/相机控制 |

### 屏幕信息
- **分辨率**：1920 x 1080 (1080p FHD)
- **刷新率**：60Hz

### 配置历史
- **2026-02-03**：创建 computer-control MCP 服务器
  - 功能：截图、鼠标、键盘、窗口管理
  - 脚本：9 个控制脚本
  - 重启 Gateway 使配置生效

---

## MCP 与技能配置

### 已配置的技能（2026-02-03）

#### 1. media-downloader（媒体下载管理）
- **路径**: `~/.openclaw/skills/media-downloader/`
- **功能**: qBittorrent 下载管理、RSS 监控、磁盘空间检查
- **脚本**:
  - `status.sh` - 查看下载状态
  - `add_torrent.sh` - 添加下载
  - `disk_space.sh` - 磁盘空间
  - `rss_list.sh` - RSS 列表
- **使用场景**: 管理追更、检查下载进度

#### 2. screen-automation（屏幕自动化）
- **路径**: `~/.openclaw/skills/screen-automation/`
- **功能**: 截图、窗口管理、UI 交互
- **脚本**:
  - `screenshot.sh` - 截屏
  - `resolution.sh` - 获取分辨率
  - `list_windows.sh` - 列出窗口
  - `click.sh`, `type.sh` - 点击和输入
- **使用场景**: 屏幕阅读、UI 自动化

#### 3. system-manager（系统管理）
- **路径**: `~/.openclaw/skills/system-manager/`
- **功能**: 系统监控、进程管理、网络检查
- **脚本**:
  - `sysinfo.sh` - 系统信息
  - `openclaw_status.sh` - OpenClaw 状态
  - `openclaw_restart.sh` - 重启 OpenClaw
  - `cpu.sh`, `memory.sh`, `disk.sh` - 性能监控
- **使用场景**: 系统维护、故障排查

### 可用的工具

| 工具 | 状态 | 用途 |
|------|------|------|
| `exec` | ✅ 可用 | 执行 Shell 命令 |
| `browser` | ⚠️ 需配置 Chrome 扩展 | 浏览器控制 |
| `nodes` | ⚠️ 无配对节点 | 屏幕/相机控制 |
| `message` | ✅ 可用 | 消息发送 |
| `cron` | ✅ 可用 | 定时任务 |
| `sessions_*` | ✅ 可用 | 会话管理 |

### 权限提升计划

1. **短期**（已完成）:
   - ✅ 创建 3 个自定义 Skill
   - ✅ 启用系统命令执行

2. **中期**:
   - [ ] 安装 OpenClaw 桌面应用（启用 nodes）
   - [ ] 配置 Chrome 扩展（启用 browser）
   - [ ] 安装 qBittorrent CLI（增强下载管理）

3. **长期**:
   - [ ] 配置 MCP 服务器（跨应用集成）
   - [ ] 集成 AI 视觉模型（屏幕理解）

### 本机能力验证

- **截图**: ✅ 可用（`screencapture` 命令）
- **窗口管理**: ✅ 可用（AppleScript）
- **系统命令**: ✅ 可用（exec 工具）
- **文件操作**: ✅ 可用（read/write/edit）

### 配置记录

| 日期 | 动作 | 影响 |
|------|------|------|
| 2026-02-03 | 创建 media-downloader Skill | 增强下载管理能力 |
| 2026-02-03 | 创建 screen-automation Skill | 增强屏幕控制能力 |
| 2026-02-03 | 创建 system-manager Skill | 增强系统管理能力 |
| 2026-02-03 | 重启 OpenClaw gateway | 服务恢复正常 |

---

## 备注

本文档是「精选记忆」，不包含所有细节。详细内容请参考：
- Daily Notes：`memory/YYYY-MM-DD.md`
- 记忆总览：`memory/MASTER_INDEX.md`
- 学习进度：`learning/LEARNING_INDEX.md`

每次会话开始时，我会读取：
1. `SOUL.md` - 了解我现在的角色
2. `USER.md` - 了解你的情况
3. `memory/YYYY-MM-DD.md`（今天和昨天）- 近期上下文
4. `MEMORY.md`（仅主会话）- 核心长期记忆

---

## 2026-02-03 更新

### MCP v2.0 升级

**重大更新**：重写 computer-control MCP server，集成 cliclick 工具

#### 新增功能
- ✅ 鼠标拖拽（mouse_drag）
- ✅ 屏幕取色（screen_color）- RGB + HEX
- ✅ 等待延时（wait）
- ✅ 右键点击
- ✅ 双击支持
- ✅ 修饰键支持（cmd, option, ctrl, shift）

#### 依赖工具
- **cliclick**：已通过 `brew install cliclick` 安装
- 路径：`/opt/homebrew/Cellar/cliclick/5.1`

#### 功能测试结果
```
屏幕分辨率: 1920x1080 ✓
鼠标控制: 正常 ✓
键盘输入: 正常 ✓
屏幕取色: 正常 ✓
```

#### 配置位置
- MCP Server: `~/.openclaw/mcp-servers/computer-control.js`
- Gateway: 已重启，配置生效

---

**作者**：Hans TheBot
**时间**：2026-02-03 15:50 PST

---

## 2026-02-03 更新

### 项目管理系统开发完成

**位置**: `~/.openclaw/workspace/project-management-system/`

#### 技术栈
| 组件 | 技术 | 状态 |
|------|------|------|
| 前端 | Vue 3 + Element Plus | ✅ |
| 后端 | Spring Boot 3.2 + Java 21 | ✅ |
| ORM | MyBatis-Plus | ✅ |
| 认证 | JWT | ✅ |
| 数据库 | OceanBase | ⏳ Docker |
| 消息队列 | Kafka | ⏳ Docker |

#### 已完成
- 24 个后端 Java 文件
- 11 个前端 Vue 文件
- Docker Compose 编排配置
- 数据库初始化脚本
- 一键安装/启动脚本

#### 文件清单
- `README.md` - 项目说明
- `DOCKER_QUICKSTART.md` - Docker 启动指南
- `install.sh` - 环境安装脚本
- `start.sh` - 启动脚本
- `docs/init-db.sql` - 数据库脚本

#### 启动方式
```bash
# 1. 安装 Docker Desktop（手动）
# 2. docker-compose up -d
# 3. 初始化数据库
# 4. mvn spring-boot:run (后端)
# 5. npm run dev (前端)
```

#### 访问地址
- 前端: localhost:3000
- 后端: localhost:8080
- Swagger: localhost:8080/doc.html
