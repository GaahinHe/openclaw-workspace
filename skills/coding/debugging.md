# 调试助手技能 (Debugging Assistant)

## 描述
定位 bug、分析错误信息、提供修复方案

## 使用场景
- 代码运行报错需要诊断
- 逻辑错误需要定位
- 性能问题需要分析
- 异常行为需要排查

## 调试方法论

### 1. 信息收集
```
- 错误信息 (完整 stack trace)
- 复现步骤 (如何触发 bug)
- 预期行为 vs 实际行为
- 环境信息 (OS、版本、依赖)
- 最近变更 (什么改动后出现的问题)
```

### 2. 问题分类
| 类型 | 特征 | 排查重点 |
|------|------|---------|
| 语法错误 | 编译/解析失败 | 检查语法、拼写 |
| 运行时错误 | 程序崩溃、异常 | 检查 null、边界、资源 |
| 逻辑错误 | 结果不对但不报错 | 检查算法、条件、状态 |
| 性能问题 | 慢、卡顿、内存高 | 检查复杂度、泄漏、阻塞 |
| 并发问题 | 偶发、竞态条件 | 检查锁、同步、共享状态 |

### 3. 定位策略

#### 二分法排查
```
1. 确定问题范围 (整个系统 vs 某个模块)
2. 逐步缩小 (模块 → 函数 → 代码行)
3. 添加日志/断言验证假设
```

#### 对比法排查
```
1. 对比正常 vs 异常的输入
2. 对比正常 vs 异常的执行路径
3. 对比正常 vs 异常的状态
```

#### 假设验证法
```
1. 列出所有可能的原因
2. 逐一验证或排除
3. 找到根本原因
```

## 调试工具集

### 日志调试
```python
# 添加调试日志
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def suspicious_function(data):
    logger.debug(f"Input: {data}")
    # ... 处理逻辑
    logger.debug(f"Output: {result}")
```

### 断言调试
```python
def process_user(user):
    assert user is not None, "User cannot be None"
    assert hasattr(user, 'id'), "User must have id"
    # ... 处理逻辑
```

### 断点调试
```
# VS Code / PyCharm / IDE
- 设置断点
- 单步执行
- 查看变量
- 调用栈分析
```

### 性能分析
```bash
# Python
python -m cProfile script.py

# Node.js
node --inspect script.js

# Java
jmap -heap <pid>
```

## 调试流程

```
1. 复现问题
   └─→ 能否稳定复现？
       ├─ 是 → 进入步骤 2
       └─ 否 → 收集更多上下文，添加日志

2. 定位问题
   └─→ 使用二分法/对比法/假设法
       └─→ 找到具体代码位置

3. 分析原因
   └─→ 为什么这里会出错？
       └─→ 根本原因是什么？

4. 制定方案
   └─→ 临时修复 (workaround)
   └─→ 根本修复 (fix root cause)
   └─→ 预防措施 (test, monitor)

5. 验证修复
   └─→ 原问题是否解决？
   └─→ 是否引入新问题？
   └─→ 边界情况是否覆盖？
```

## 输出格式

```markdown
## 🐛 调试报告

### 问题描述
[用户描述的问题]

### 错误信息
```
[完整错误日志/stack trace]
```

### 根本原因
[分析出的根本原因]

### 修复方案

#### 方案 1: [推荐]
```code
[修复代码]
```
**优点**: [...]
**缺点**: [...]

#### 方案 2: [备选]
```code
[备选方案]
```

### 验证步骤
1. [ ] 步骤 1
2. [ ] 步骤 2
3. [ ] 确认问题解决

### 预防建议
- [ ] 添加单元测试
- [ ] 添加输入验证
- [ ] 添加监控告警
```

## 常见错误模式

### 1. Null/Undefined 引用
```javascript
// ❌ 错误
const name = user.profile.name;

// ✅ 修复
const name = user?.profile?.name ?? 'Unknown';
```

### 2. 异步时序问题
```javascript
// ❌ 错误
let data;
fetch('/api').then(r => data = r.json());
console.log(data); // undefined

// ✅ 修复
const data = await fetch('/api').then(r => r.json());
console.log(data);
```

### 3. 闭包陷阱
```javascript
// ❌ 错误
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100);
}
// 输出：5, 5, 5, 5, 5

// ✅ 修复
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100);
}
// 输出：0, 1, 2, 3, 4
```

### 4. 浮点数精度
```python
# ❌ 错误
0.1 + 0.2 == 0.3  # False

# ✅ 修复
from decimal import Decimal
Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True
```

## 调试检查清单

- [ ] 能否稳定复现？
- [ ] 错误信息完整吗？
- [ ] 最近有什么变更？
- [ ] 输入数据正常吗？
- [ ] 依赖服务正常吗？
- [ ] 资源 (内存/磁盘/网络) 充足吗？
- [ ] 并发/竞态条件？
- [ ] 缓存导致的问题？
- [ ] 时区/编码/格式问题？
- [ ] 权限/配置问题？

---

**相关技能**: [[代码审查]] [[重构建议]] [[代码生成]]
