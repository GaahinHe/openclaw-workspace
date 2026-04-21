# 记忆检索技能 (Memory Retrieval)

## 描述
根据关键词检索历史记忆，快速找到相关信息

## 使用场景
- 用户问"我们之前讨论过 X 吗"
- 需要查找特定决策的原因
- 回顾学习进度
- 寻找历史记录

## 检索策略

### 1. 关键词检索
**方法**: 提取用户 query 中的关键词

**示例**:
```
用户："我们之前讨论过机器学习的什么内容？"

关键词：["机器学习", "ML", "学习"]

搜索范围:
- MEMORY.md (长期记忆)
- memory/*.md (每日记录)
- learning/*.md (学习记录)
```

### 2. 语义检索
**方法**: 理解用户意图，扩展相关词

**示例**:
```
用户："我是怎么配置系统的？"

意图：查找系统配置历史

扩展词：["配置", "设置", "安装", "部署", "环境"]

搜索范围:
- MEMORY.md [技术栈记录]
- memory/ 中包含"配置"的文件
```

### 3. 时间范围检索
**方法**: 根据时间线索缩小范围

**示例**:
```
用户："上周我们说了什么？"

时间范围：过去 7 天

搜索文件：memory/YYYY-MM-DD.md (最近 7 个文件)
```

### 4. 主题检索
**方法**: 按主题分类检索

**示例**:
```
用户："我的学习进度如何？"

主题：学习进度

搜索范围:
- MEMORY.md [学习框架] [待办事项]
- learning/LEARNING_INDEX.md
- memory/ 中学习相关文件
```

## 检索算法

### 基础检索流程
```python
def retrieve_memory(query, filters=None):
    """
    检索记忆
    
    Args:
        query: 用户查询
        filters: 过滤条件 (时间/主题/类型)
    
    Returns:
        相关记忆片段列表
    """
    # 1. 提取关键词
    keywords = extract_keywords(query)
    
    # 2. 确定搜索范围
    scope = determine_scope(query, filters)
    
    # 3. 执行搜索
    results = []
    for file in scope:
        content = read_file(file)
        matches = search_content(content, keywords)
        results.extend(matches)
    
    # 4. 排序和过滤
    results = rank_results(results, query)
    
    # 5. 返回 Top N
    return results[:10]
```

### 关键词提取
```python
def extract_keywords(query):
    """提取查询关键词"""
    # 移除停用词
    stop_words = ["的", "了", "吗", "什么", "怎么", "我们", "之前"]
    
    # 分词 (简单实现)
    words = query.split()
    
    # 过滤停用词
    keywords = [w for w in words if w not in stop_words]
    
    # 添加同义词
    synonyms = {
        "ML": ["机器学习", "machine learning"],
        "AI": ["人工智能", "artificial intelligence"],
        "配置": ["设置", "install", "setup"],
    }
    
    for kw in keywords[:]:
        if kw in synonyms:
            keywords.extend(synonyms[kw])
    
    return keywords
```

### 相关性评分
```python
def score_match(match, query):
    """计算匹配片段的相关性分数"""
    score = 0
    
    # 1. 关键词匹配数
    for kw in query_keywords:
        if kw in match['text']:
            score += 1
    
    # 2. 位置加权 (标题 > 正文)
    if match['in_title']:
        score *= 2
    
    # 3. 时间衰减 (越近越相关)
    days_old = (now - match['date']).days
    time_weight = 1 / (1 + days_old * 0.1)
    score *= time_weight
    
    # 4. 来源加权 (MEMORY.md > daily notes)
    source_weight = {
        'MEMORY.md': 1.5,
        'learning/': 1.2,
        'memory/': 1.0,
    }
    score *= source_weight.get(match['source'], 1.0)
    
    return score
```

## 检索输出格式

### 1. 搜索结果摘要
```markdown
## 🔍 检索结果

**查询**: "[用户原始查询]"
**找到**: X 条相关记录

### 最相关 (3 条)

#### 1. [标题/主题]
**来源**: `文件路径：行号`
**日期**: YYYY-MM-DD
**内容**: 
> [引用相关片段]

#### 2. [标题/主题]
...

### 查看全部
[列出所有匹配文件]
```

### 2. 时间线视图
```markdown
## 📅 [主题] 时间线

**2026-02-24**: 首次讨论 X
- 决策：采用 Y 方案
- 原因：性能更好

**2026-02-20**: 实施 X
- 完成：模块 A
- 待办：模块 B

**2026-02-15**: 规划 X
- 需求分析
- 技术选型
```

### 3. 主题汇总
```markdown
## 📚 [主题] 汇总

### 核心信息
[从 MEMORY.md 提取的核心记录]

### 详细记录
[按时间排序的详细记录]

### 当前状态
[最新状态]

### 相关文件
- `MEMORY.md` - 核心原则
- `memory/2026-02-24.md` - 讨论记录
- `learning/ai-dev.md` - 学习进度
```

## 高级检索功能

### 1. 布尔检索
```
支持操作符:
- AND: "机器学习 AND 进度"
- OR: "机器学习 OR 深度学习"
- NOT: "机器学习 NOT 理论"
- "": "精确短语匹配"
```

### 2. 模糊检索
```
支持模糊匹配:
- 拼写错误容忍
- 同义词扩展
- 词干提取 (中英文)
```

### 3. 结构化检索
```
支持字段过滤:
- date:2026-02-24
- type:decision
- topic:learning
- status:completed
```

## 检索优化

### 1. 索引预建
```python
# 启动时建立索引
def build_index():
    index = {}
    for file in all_memory_files():
        content = read_file(file)
        for line_num, line in enumerate(content):
            for word in extract_words(line):
                if word not in index:
                    index[word] = []
                index[word].append({
                    'file': file,
                    'line': line_num,
                    'text': line,
                    'date': extract_date(file)
                })
    return index
```

### 2. 缓存热点
```python
# 缓存常见查询结果
cache = {}

def cached_search(query):
    if query in cache:
        return cache[query]
    
    results = search(query)
    cache[query] = results
    return results
```

### 3. 增量更新
```python
# 文件变化时更新索引
def update_index(changed_file):
    content = read_file(changed_file)
    for word in all_words:
        if word in changed_file:
            rebuild_word_index(word)
```

## 示例对话

**用户**: 我们之前讨论过什么关于配置的事情？

**助手**:

## 🔍 记忆检索结果

**查询**: "配置"
**找到**: 5 条相关记录

### 最相关

#### 1. 模型配置策略
**来源**: `MEMORY.md: 网络环境配置`
**日期**: 2026-02-24
**内容**: 
> 当前配置：唯一模型 Bailian - Qwen3-Max
> 配置变更历史：2026-02-24 移除多模型路由，只保留 qwen3-max
> 备份文件：`/Users/hans/.openclaw/tmp/model_config_backup_2026-02-24.json`

#### 2. 媒体下载配置
**来源**: `MEMORY.md: 媒体下载配置`
**日期**: 2026-02-03
**内容**:
> qBittorrent 已安装并运行
> 存储路径：/Volumes/exFAT 大仓库/HDMedia/
> 追更清单：海贼王、怪奇物语等

#### 3. MCP 与技能配置
**来源**: `MEMORY.md: MCP 与技能配置`
**日期**: 2026-02-03
**内容**:
> 已配置 3 个自定义 Skill:
> - media-downloader
> - screen-automation
> - system-manager

### 完整时间线
1. **2026-02-24**: 简化模型配置为单一 Qwen3-Max
2. **2026-02-03**: 配置媒体下载和 MCP 服务器
3. **2026-02-02**: 初始系统配置

需要查看某个配置的详细信息吗？

---

**相关技能**: [[长期记忆读取]] [[记忆维护]] [[短期记忆管理]]
