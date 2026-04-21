# 网络搜索技能 (Web Search)

## 描述
搜索信息和资源，获取最新知识和数据

## 使用场景
- 查找最新信息
- 验证事实
- 获取文档
- 研究主题

## 搜索工具

### web_search 工具
```
工具：web_search
参数：query, count, freshness, language, country

示例:
web_search(query="AI 最新进展", count=10)
web_search(query="Python 教程", freshness="week")
web_search(query="machine learning", language="en")
```

### web_fetch 工具
```
工具：web_fetch
参数：url, extractMode, maxChars

示例:
web_fetch(url="https://example.com/article")
web_fetch(url="https://...", extractMode="text")
```

### browser 工具
```
工具：browser
动作：open, navigate, snapshot, act

用于复杂网页交互
```

## 搜索策略

### 关键词优化
```
✅ 好关键词:
- 具体明确："Python 3.11 新特性"
- 包含类型："tutorial", "guide", "documentation"
- 使用引号："精确短语匹配"
- 排除词："-广告 -推广"

❌ 差关键词:
- 太宽泛："Python"
- 模糊："怎么用"
- 口语化："那个什么工具"
```

### 搜索操作符
```
site:      限制域名
  示例：site:github.com AI

filetype:  限制文件类型
  示例：filetype:pdf 机器学习

intitle:   标题包含
  示例：intitle:教程 Python

inurl:     URL 包含
  示例：inurl:docs API

"":        精确匹配
  示例："deep learning"

-:        排除
  示例：python -snake

OR:       或
  示例：AI OR "人工智能"

*:        通配符
  示例："machine * learning"
```

### 时间过滤
```
freshness 参数:
- day: 24 小时内
- week: 一周内
- month: 一月内
- year: 一年内

date_after: YYYY-MM-DD
date_before: YYYY-MM-DD
```

### 语言/地区
```
language: en, zh, ja, ...
country: US, CN, JP, ...
ui_lang: en-US, zh-CN, ...
search_lang: en, zh-hans, ...
```

## 信息评估

### 来源可信度
```
高可信度:
✅ 官方文档 (docs.python.org)
✅ 学术论文 (arxiv.org)
✅ 权威媒体 (reuters.com)
✅ 知名机构 (mit.edu)

中可信度:
⚠️ 技术博客 (需验证)
⚠️ Stack Overflow (看票数)
⚠️ GitHub 项目 (看 star)

低可信度:
❌ 营销内容
❌ 匿名文章
❌ 过期信息
```

### 信息质量检查
```
检查清单:
- [ ] 来源可靠吗？
- [ ] 作者是谁？
- [ ] 何时发布？
- [ ] 有引用来源吗？
- [ ] 有其他佐证吗？
- [ ] 是否有偏见？
- [ ] 信息完整吗？
```

### 交叉验证
```
多源验证:
1. 搜索同一主题多个来源
2. 对比信息是否一致
3. 查找原始来源
4. 检查是否有更新

示例:
搜索 "Python 3.11 发布"
→ 查看 python.org 官方
→ 查看 GitHub release
→ 查看权威媒体报道
```

## 搜索流程

### 步骤 1: 明确需求
```
- 要找什么信息？
- 需要什么格式？
- 时间要求？
- 质量要求？
```

### 步骤 2: 制定策略
```
- 关键词选择
- 搜索工具选择
- 过滤条件设置
```

### 步骤 3: 执行搜索
```
- 运行搜索
- 查看结果
- 调整策略 (如无结果)
```

### 步骤 4: 评估结果
```
- 来源可信度
- 信息相关性
- 时效性
```

### 步骤 5: 提取信息
```
- 读取内容
- 提取要点
- 记录来源
```

### 步骤 6: 整理输出
```
- 总结信息
- 标注来源
- 提供链接
```

## 输出格式

### 搜索结果摘要
```markdown
## 🔍 搜索结果：[主题]

**搜索词**: [query]
**结果数**: X 条
**时间范围**: [freshness]

### 关键发现

1. **[标题 1]**
   - 来源：[网站]
   - 日期：[日期]
   - 要点：[摘要]
   - 链接：[URL]

2. **[标题 2]**
   ...

### 总结
[综合总结]
```

### 对比分析
```markdown
## 📊 信息对比

| 来源 | 观点 | 证据 | 可信度 |
|------|------|------|--------|
| A | ... | ... | 高 |
| B | ... | ... | 中 |
| C | ... | ... | 低 |

### 共识点
- ...

### 分歧点
- ...
```

### 深度报告
```markdown
# [主题] 调研报告

## 执行摘要
[核心发现]

## 背景
[问题背景]

## 方法
[搜索策略]

## 发现

### 主题 1
[内容 + 引用]

### 主题 2
[内容 + 引用]

## 分析
[深入分析]

## 结论
[结论]

## 参考来源
1. [来源 1] - [URL]
2. [来源 2] - [URL]
```

## 高级技巧

### 学术搜索
```
工具:
- Google Scholar
- arXiv
- Semantic Scholar

技巧:
- 使用学术关键词
- 查看引用次数
- 查找综述文章
- 追踪作者
```

### 代码搜索
```
工具:
- GitHub
- Stack Overflow
- 官方文档

技巧:
- 搜索库/框架名
- 查看 issue/discussion
- 检查 star 和更新
- 阅读文档
```

### 新闻监控
```
工具:
- Google News
- 专业媒体
- RSS 订阅

技巧:
- 设置关键词提醒
- 关注权威来源
- 对比多家报道
- 追踪事件发展
```

## 示例对话

**用户**: 帮我查一下 Qwen3.5 的最新信息

**助手**:

好的，让我搜索 Qwen3.5 的最新信息。

```bash
web_search(query="Qwen3.5 阿里 发布", count=10, freshness="month")
```

## 🔍 搜索结果：Qwen3.5

**搜索词**: Qwen3.5 阿里 发布
**时间范围**: 过去 1 个月

### 关键发现

1. **阿里云发布 Qwen3.5 模型**
   - 来源：阿里云官网
   - 日期：2026-02-15
   - 要点：
     - 上下文窗口 256K
     - 支持 100+ 语言
     - 性能提升 30%
   - 链接：aliyun.com/qwen3.5

2. **Qwen3.5 技术报告**
   - 来源：arXiv
   - 日期：2026-02-16
   - 要点：
     - 新架构设计
     - 训练数据细节
     - 基准测试结果
   - 链接：arxiv.org/abs/xxxx.xxxxx

3. **Qwen3.5 vs 竞品对比**
   - 来源：技术博客
   - 日期：2026-02-20
   - 要点：
     - 与 GPT-4 对比
     - 性能分析
     - 使用建议
   - 链接：blog.example.com/qwen3.5-review

### 总结

Qwen3.5 是阿里云 2026 年 2 月发布的大语言模型，
主要特点：
- 256K 上下文窗口
- 多语言支持
- 性能显著提升

你目前使用的 qwen3-max 是之前的版本，
可以考虑升级到 Qwen3.5。

需要我帮你查具体的配置方法吗？

---

**相关技能**: [[信息检索]] [[文档操作]] [[会话管理]]
