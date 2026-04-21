# 文件管理技能 (File Management)

## 描述
读取、写入、组织 workspace 文件，管理工作区内容

## 使用场景
- 创建/编辑文档
- 组织文件结构
- 搜索文件内容
- 版本控制管理

## 文件操作

### 读取文件
```
工具：read
参数：path, offset, limit

示例:
- 读取完整文件：read(path="file.md")
- 读取部分：read(path="file.md", offset=1, limit=100)
```

### 写入文件
```
工具：write
参数：path, content

示例:
write(path="file.md", content="# Title\n\nContent")
```

### 编辑文件
```
工具：edit
参数：path, oldText, newText

示例:
edit(path="file.md", oldText="旧内容", newText="新内容")
```

### 删除文件
```
工具：exec
命令：rm path 或 trash path

建议：使用 trash 而非 rm (可恢复)
```

## 文件组织

### 目录结构规范
```
workspace/
├── MEMORY.md              # 长期记忆
├── SOUL.md                # 角色定义
├── USER.md                # 用户信息
├── AGENTS.md              # 代理指南
├── HEARTBEAT.md           # 心跳任务
├── IDENTITY.md            # 身份定义
│
├── memory/                # 每日记忆
│   ├── 2026-02-01.md
│   ├── 2026-02-02.md
│   └── MASTER_INDEX.md
│
├── learning/              # 学习记录
│   ├── LEARNING_INDEX.md
│   └── [主题].md
│
├── skills/                # 技能文档
│   ├── SKILLS_INDEX.md
│   ├── coding/
│   ├── memory/
│   ├── learning/
│   ├── discussion/
│   └── system/
│
├── projects/              # 项目文件
│   └── [项目名]/
│
└── archive/               # 归档文件
    └── [年份]/
```

### 文件命名规范
```
✅ 推荐:
- 小写字母
- 连字符分隔：my-file.md
- 日期格式：YYYY-MM-DD.md
- 清晰描述：learning-progress.md

❌ 避免:
- 空格：my file.md
- 中文：我的文件.md (除非必要)
- 模糊：temp.md, test.md
- 过长：super-long-filename...md
```

## 文件模板

### 记忆文件模板
```markdown
# [日期] - [简短标题]

## 📅 日期
YYYY-MM-DD

## 🎯 主要活动
- [活动 1]
- [活动 2]

## 💡 关键学习
- [学习 1]
- [学习 2]

## 🤔 疑问与思考
- [疑问 1]
- [疑问 2]

## 📝 待办追踪
- [ ] [待办 1]
- [x] [已完成]

## 🔗 相关文件
- [[MEMORY.md]]
- [[learning/xxx.md]]
```

### 学习笔记模板
```markdown
# [主题] 学习笔记

**开始日期**: YYYY-MM-DD
**最后更新**: YYYY-MM-DD
**状态**: [学习中/已完成/暂停]

## 核心概念
1. [概念 1]
2. [概念 2]

## 关键要点
- [要点 1]
- [要点 2]

## 代码示例
```[语言]
[代码]
```

## 实际应用
- [应用场景 1]
- [应用场景 2]

## 疑问与待探索
- [ ] [疑问 1]
- [ ] [疑问 2]

## 参考资源
- [链接 1]
- [链接 2]

## 复习记录
- YYYY-MM-DD: 第一次学习
- YYYY-MM-DD: 第一次复习
```

### 项目文档模板
```markdown
# [项目名称]

## 项目概述
[一句话描述]

## 目标
- [目标 1]
- [目标 2]

## 技术栈
- [技术 1]
- [技术 2]

## 进度
- [ ] 阶段 1
- [x] 阶段 2 (完成日期)
- [ ] 阶段 3

## 文件结构
```
project/
├── README.md
├── src/
└── docs/
```

## 关键决策
| 决策 | 日期 | 原因 |
|------|------|------|
| | | |

## 问题与解决
| 问题 | 解决方案 | 日期 |
|------|---------|------|
| | | |

## 下一步
- [ ] [任务 1]
- [ ] [任务 2]
```

## 文件搜索

### 按名称搜索
```bash
# 查找文件
find ~/.openclaw/workspace -name "*.md"

# 查找包含关键词的文件
find ~/.openclaw/workspace -name "*memory*"
```

### 按内容搜索
```bash
# grep 搜索
grep -r "关键词" ~/.openclaw/workspace/

# 仅搜索 markdown 文件
grep -r "关键词" --include="*.md" ~/.openclaw/workspace/
```

### 按时间搜索
```bash
# 最近修改的文件
find ~/.openclaw/workspace -mtime -7 -name "*.md"

# 特定日期范围
find ~/.openclaw/workspace -newermt "2026-02-01" ! -newermt "2026-02-28"
```

## 版本控制

### Git 基本操作
```bash
# 查看状态
git status

# 添加文件
git add file.md
git add .  # 全部

# 提交
git commit -m "描述"

# 查看历史
git log --oneline

# 撤销
git checkout -- file.md
```

### 提交信息规范
```
格式：<类型>: <描述>

类型:
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- chore: 杂项

示例:
feat: 添加学习笔记模板
fix: 修正 MEMORY.md 格式
docs: 更新 README
```

### 同步操作
```bash
# 一键同步 (GitHub + Gitee)
git pushall

# 手动同步
git push origin main
git push gitee main
```

## 文件安全

### 备份策略
```bash
# 重要文件备份
cp file.md file.md.bak.YYYY-MM-DD

# 目录备份
tar -czf backup-$(date +%Y%m%d).tar.gz workspace/

# 自动备份脚本
#!/bin/bash
cp MEMORY.md MEMORY.md.bak.$(date +%Y%m%d-%H%M%S)
```

### 敏感信息处理
```
❌ 不要写入:
- 密码、密钥
- 个人隐私信息
- 第三方机密

✅ 可以写入:
- 学习心得
- 项目文档
- 公开信息
```

## 示例对话

**用户**: 帮我创建一个今天的学习笔记

**助手**:

好的，我来创建今天的学习笔记。

```markdown
# 2026-03-10 - 技能安装

## 📅 日期
2026-03-10

## 🎯 主要活动
- 创建 coding 技能 (5 个文件)
- 创建 memory 技能 (5 个文件)
- 创建 learning 技能 (6 个文件)
- 创建 discussion 技能 (5 个文件)
- 创建 system 技能 (进行中)

## 💡 关键学习
- 技能文件的标准结构
- 如何组织知识体系
- 文档模板的重要性

## 🤔 疑问与思考
- 技能如何更好地被调用？
- 如何评估技能效果？

## 📝 待办追踪
- [x] 创建技能文件
- [ ] 更新 SKILLS_INDEX.md
- [ ] 测试技能调用

## 🔗 相关文件
- [[SKILLS_INDEX.md]]
- [[memory/2026-03-10.md]]
```

已保存到 `memory/2026-03-10.md`。

需要我帮你记录具体学习内容吗？

---

**相关技能**: [[文档操作]] [[命令执行]] [[会话管理]]
