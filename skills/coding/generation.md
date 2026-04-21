# 代码生成技能 (Code Generation)

## 描述
根据需求生成代码、测试用例、样板代码

## 使用场景
- 根据需求描述生成实现代码
- 生成单元测试/集成测试
- 生成 CRUD 样板代码
- 生成 API 文档/注释
- 代码迁移/转换

## 生成流程

```
1. 需求理解
   └─→ 功能需求是什么？
   └─→ 输入/输出是什么？
   └─→ 边界条件有哪些？
   └─→ 性能要求是什么？

2. 技术选型
   └─→ 使用什么语言/框架？
   └─→ 需要什么依赖库？
   └─→ 遵循什么规范？

3. 代码设计
   └─→ 函数/类结构
   └─→ 数据流设计
   └─→ 错误处理策略

4. 代码生成
   └─→ 实现核心逻辑
   └─→ 添加注释文档
   └─→ 生成测试用例

5. 质量检查
   └─→ 代码审查
   └─→ 边界测试
   └─→ 性能考虑
```

## 代码生成模板

### 1. 函数生成模板
```
[语言]: [函数名]
功能：[一句话描述]
输入：[参数列表及类型]
输出：[返回值类型及含义]
异常：[可能抛出的异常]
示例：[使用示例]
```

### 2. 类生成模板
```
[语言]: [类名]
职责：[类的单一职责]
属性：[成员变量列表]
方法：[公开方法列表]
依赖：[外部依赖]
使用示例：[实例化及使用]
```

### 3. API 生成模板
```
Endpoint: [HTTP 方法] [路径]
描述：[API 功能描述]
请求头：[Headers]
请求参数：[Query/Path params]
请求体：[Body schema]
响应：[成功响应 schema]
错误：[错误码及含义]
示例：[curl/代码示例]
```

### 4. 测试生成模板
```
测试框架：[JUnit/Pytest/Jest 等]
测试类型：[单元/集成/E2E]
测试场景：
  - 正常流程
  - 边界条件
  - 异常情况
  - 性能测试 (如需要)
```

## 语言特定指南

### Python 代码生成
```python
"""
模块：[模块名]
功能：[功能描述]
作者：[作者]
日期：[日期]
"""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ClassName:
    """类描述"""
    
    def __init__(self, param: str) -> None:
        """初始化方法
        
        Args:
            param: 参数描述
        """
        self._param = param
    
    def method_name(self, arg: int) -> Optional[str]:
        """方法描述
        
        Args:
            arg: 参数描述
            
        Returns:
            返回值描述，失败返回 None
            
        Raises:
            ValueError: 当参数无效时
        """
        if arg < 0:
            raise ValueError("arg must be non-negative")
        
        logger.debug(f"Processing {arg}")
        return f"Result: {arg}"
```

### TypeScript 代码生成
```typescript
/**
 * 模块：[模块名]
 * 功能：[功能描述]
 */

import { Logger } from './logger';

export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export type CreateUserInput = Omit<User, 'id' | 'createdAt'>;

export class UserService {
  private readonly logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  /**
   * 创建用户
   * @param input - 用户输入数据
   * @returns 创建的用户对象
   * @throws Error 当用户已存在时
   */
  async createUser(input: CreateUserInput): Promise<User> {
    this.logger.info('Creating user', { email: input.email });
    
    // 验证输入
    if (!input.email.includes('@')) {
      throw new Error('Invalid email');
    }

    // 实现逻辑
    const user: User = {
      id: crypto.randomUUID(),
      ...input,
      createdAt: new Date(),
    };

    return user;
  }
}
```

### Java 代码生成
```java
/**
 * 类：ClassName
 * 功能：[功能描述]
 * 作者：[作者]
 */
package com.example.module;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.Optional;

public class ClassName {
    private static final Logger logger = LoggerFactory.getLogger(ClassName.class);
    
    private final String dependency;
    
    public ClassName(String dependency) {
        this.dependency = dependency;
    }
    
    /**
     * 方法描述
     * 
     * @param param 参数描述
     * @return 返回值描述
     * @throws IllegalArgumentException 当参数无效时
     */
    public Optional<String> methodName(int param) {
        if (param < 0) {
            throw new IllegalArgumentException("param must be non-negative");
        }
        
        logger.debug("Processing param: {}", param);
        
        try {
            String result = process(param);
            return Optional.of(result);
        } catch (Exception e) {
            logger.error("Processing failed", e);
            return Optional.empty();
        }
    }
    
    private String process(int param) {
        // 实现逻辑
        return "Result: " + param;
    }
}
```

## 测试用例生成

### 单元测试模板
```python
import pytest
from mymodule import MyClass

class TestMyClass:
    """MyClass 单元测试"""
    
    def setup_method(self):
        """每个测试前的准备"""
        self.obj = MyClass()
    
    def teardown_method(self):
        """每个测试后的清理"""
        pass
    
    def test_normal_case(self):
        """测试正常流程"""
        result = self.obj.method(5)
        assert result == "Result: 5"
    
    def test_boundary_case(self):
        """测试边界条件"""
        result = self.obj.method(0)
        assert result == "Result: 0"
    
    def test_exception_case(self):
        """测试异常情况"""
        with pytest.raises(ValueError):
            self.obj.method(-1)
    
    def test_edge_case(self):
        """测试边缘情况"""
        result = self.obj.method(1000000)
        assert result is not None
```

### 集成测试模板
```typescript
import request from 'supertest';
import { app } from '../src/app';
import { db } from '../src/db';

describe('User API Integration Tests', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        ...userData,
      });
    });

    it('should return 400 for invalid email', async () => {
      const userData = {
        name: 'Test User',
        email: 'invalid-email',
      };

      await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);
    });
  });
});
```

## 代码生成检查清单

生成代码前确认：
- [ ] 理解需求和边界条件
- [ ] 选择合适的语言/框架
- [ ] 遵循项目代码规范
- [ ] 考虑错误处理
- [ ] 添加必要的注释
- [ ] 生成对应的测试用例
- [ ] 检查性能影响
- [ ] 考虑安全性

生成代码后检查：
- [ ] 代码能否编译/运行？
- [ ] 测试能否通过？
- [ ] 是否有代码异味？
- [ ] 是否需要重构？
- [ ] 文档是否完整？

## 示例对话

**用户**: 帮我生成一个 Python 函数，验证邮箱格式

**助手**:

```python
import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    验证邮箱格式
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        Tuple[是否有效，错误信息]
        - 有效时返回 (True, None)
        - 无效时返回 (False, 错误原因)
    """
    if not email:
        return False, "邮箱不能为空"
    
    if len(email) > 254:
        return False, "邮箱长度不能超过 254 个字符"
    
    # RFC 5322 标准邮箱正则
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "邮箱格式不正确"
    
    # 检查连续点号
    if '..' in email:
        return False, "邮箱不能包含连续点号"
    
    # 检查开头结尾
    if email.startswith('.') or email.endswith('.'):
        return False, "邮箱不能以点号开头或结尾"
    
    return True, None


# 使用示例
if __name__ == "__main__":
    test_emails = [
        "user@example.com",      # 有效
        "invalid-email",         # 无效
        "user..name@example.com", # 无效
        ".user@example.com",     # 无效
    ]
    
    for email in test_emails:
        valid, error = validate_email(email)
        status = "✓" if valid else "✗"
        print(f"{status} {email}: {error or '有效'}")
```

**测试用例**:

```python
import pytest
from email_validator import validate_email


class TestValidateEmail:
    def test_valid_emails(self):
        """测试有效邮箱"""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
        ]
        for email in valid_emails:
            valid, error = validate_email(email)
            assert valid is True
            assert error is None
    
    def test_invalid_emails(self):
        """测试无效邮箱"""
        invalid_emails = [
            ("", "邮箱不能为空"),
            ("invalid", "邮箱格式不正确"),
            ("user..name@example.com", "邮箱不能包含连续点号"),
            (".user@example.com", "邮箱不能以点号开头或结尾"),
        ]
        for email, expected_error in invalid_emails:
            valid, error = validate_email(email)
            assert valid is False
            assert error == expected_error
```

---

**相关技能**: [[代码审查]] [[调试助手]] [[架构设计]]
