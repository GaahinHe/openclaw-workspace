# 重构建议技能 (Refactoring Suggestions)

## 描述
代码重构、消除代码异味、提升可维护性

## 使用场景
- 代码难以理解和维护
- 需要添加新功能但代码结构不支持
- 发现重复代码
- 性能优化前的结构整理
- 技术债务清理

## 代码异味 (Code Smells)

### 1. 重复代码 (Duplicated Code)
**症状**: 相同或相似代码在多处出现

**危害**: 
- 修改需要同步多处
- 容易遗漏导致 bug
- 代码膨胀

**重构方案**:
```python
# ❌ 重构前 - 重复代码
def process_user(user):
    if not user:
        raise ValueError("User is required")
    if not user.email:
        raise ValueError("Email is required")
    # ... 处理逻辑

def process_order(order):
    if not order:
        raise ValueError("Order is required")
    if not order.email:
        raise ValueError("Email is required")
    # ... 处理逻辑

# ✅ 重构后 - 提取公共逻辑
def validate_entity(entity, entity_type):
    if not entity:
        raise ValueError(f"{entity_type} is required")
    if not entity.email:
        raise ValueError("Email is required")

def process_user(user):
    validate_entity(user, "User")
    # ... 处理逻辑

def process_order(order):
    validate_entity(order, "Order")
    # ... 处理逻辑
```

### 2. 过长函数 (Long Method)
**症状**: 函数超过 20-30 行

**危害**:
- 难以理解
- 难以测试
- 难以复用

**重构方案**:
```python
# ❌ 重构前 - 过长函数
def process_order(order):
    # 验证订单
    if not order:
        raise ValueError("Order is required")
    if not order.items:
        raise ValueError("Order has no items")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")
        if item.price < 0:
            raise ValueError("Invalid price")
    
    # 计算总价
    total = 0
    for item in order.items:
        subtotal = item.quantity * item.price
        if subtotal > 1000:
            subtotal *= 0.9  # 折扣
        total += subtotal
    
    # 计算税费
    tax = total * 0.08
    total += tax
    
    # 应用优惠券
    if order.coupon:
        discount = calculate_discount(order.coupon, total)
        total -= discount
    
    # 保存订单
    order.total = total
    db.save(order)
    
    # 发送确认邮件
    send_email(order.user.email, "Order confirmed")
    
    # 更新库存
    for item in order.items:
        inventory.reduce(item.id, item.quantity)
    
    return order

# ✅ 重构后 - 拆分函数
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    apply_coupon(order, total)
    save_order(order)
    notify_user(order)
    update_inventory(order)
    return order

def validate_order(order):
    if not order:
        raise ValueError("Order is required")
    if not order.items:
        raise ValueError("Order has no items")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")
        if item.price < 0:
            raise ValueError("Invalid price")

def calculate_total(order):
    total = sum(
        apply_bulk_discount(item.quantity * item.price)
        for item in order.items
    )
    total += calculate_tax(total)
    order.total = total
    return total

def apply_coupon(order, total):
    if order.coupon:
        discount = calculate_discount(order.coupon, total)
        order.total -= discount

def save_order(order):
    db.save(order)

def notify_user(order):
    send_email(order.user.email, "Order confirmed")

def update_inventory(order):
    for item in order.items:
        inventory.reduce(item.id, item.quantity)
```

### 3. 过大类 (Large Class)
**症状**: 类超过 500 行，职责过多

**危害**:
- 难以理解
- 修改风险高
- 违反单一职责

**重构方案**:
```python
# ❌ 重构前 - 过大类
class UserManager:
    def create_user(self, ...): ...
    def delete_user(self, ...): ...
    def update_user(self, ...): ...
    def send_welcome_email(self, ...): ...
    def send_password_reset_email(self, ...): ...
    def validate_user_data(self, ...): ...
    def hash_password(self, ...): ...
    def generate_token(self, ...): ...
    def log_activity(self, ...): ...
    def get_user_stats(self, ...): ...
    # ... 50+ methods

# ✅ 重构后 - 拆分职责
class UserRepository:
    """数据访问层"""
    def create(self, ...): ...
    def delete(self, ...): ...
    def update(self, ...): ...
    def find_by_id(self, ...): ...

class UserValidator:
    """验证逻辑"""
    def validate_create(self, ...): ...
    def validate_update(self, ...): ...

class UserEmailService:
    """邮件通知"""
    def send_welcome(self, ...): ...
    def send_password_reset(self, ...): ...

class UserAuthService:
    """认证相关"""
    def hash_password(self, ...): ...
    def generate_token(self, ...): ...

class UserService:
    """业务逻辑层 - 协调各组件"""
    def __init__(self, repo, validator, email_service, auth_service):
        self.repo = repo
        self.validator = validator
        self.email_service = email_service
        self.auth_service = auth_service
    
    def create_user(self, data):
        self.validator.validate_create(data)
        user = self.repo.create(data)
        self.email_service.send_welcome(user)
        return user
```

### 4. 过长参数列表 (Long Parameter List)
**症状**: 函数参数超过 4-5 个

**危害**:
- 调用困难
- 容易传错顺序
- 难以扩展

**重构方案**:
```python
# ❌ 重构前 - 参数过多
def create_user(username, email, password, first_name, last_name, 
                phone, address, city, state, zip_code, country, 
                birth_date, gender):
    pass

# ✅ 重构后 - 使用对象
from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

@dataclass
class UserProfile:
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Address
    birth_date: Optional[date]
    gender: Optional[str]

def create_user(username: str, email: str, password: str, 
                profile: UserProfile):
    pass

# 调用
profile = UserProfile(
    first_name="John",
    last_name="Doe",
    phone="123-456-7890",
    address=Address("123 Main St", "City", "State", "12345", "USA"),
    birth_date=None,
    gender=None
)
create_user("johndoe", "john@example.com", "password", profile)
```

### 5. 过度耦合 (Coupling)
**症状**: 类之间直接依赖具体实现

**危害**:
- 修改影响范围大
- 难以测试
- 难以替换

**重构方案**:
```python
# ❌ 重构前 - 紧耦合
class OrderService:
    def __init__(self):
        self.mysql_db = MySQLDatabase()
        self.redis_cache = RedisCache()
        self.smtp_mail = SMTPMailer()
    
    def create_order(self, order):
        self.mysql_db.save(order)
        self.redis_cache.set(order.id, order)
        self.smtp_mail.send(order.user.email, "Order created")

# ✅ 重构后 - 依赖注入
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, order): pass

class Cache(ABC):
    @abstractmethod
    def set(self, key, value): pass

class Mailer(ABC):
    @abstractmethod
    def send(self, to, subject): pass

class OrderService:
    def __init__(self, db: Database, cache: Cache, mailer: Mailer):
        self.db = db
        self.cache = cache
        self.mailer = mailer
    
    def create_order(self, order):
        self.db.save(order)
        self.cache.set(order.id, order)
        self.mailer.send(order.user.email, "Order created")

# 测试时可轻松替换为 mock
class MockDatabase(Database):
    def save(self, order): pass
```

## 重构手法 (Refactoring Techniques)

### 1. 提取函数 (Extract Method)
**适用**: 代码块可独立命名

```python
# Before
def print_invoice(order):
    # ... 计算逻辑
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    print(f"Total: ${total}")
    # ... 更多逻辑

# After
def print_invoice(order):
    total = calculate_total(order)
    print(f"Total: ${total}")

def calculate_total(order):
    return sum(item.price * item.quantity for item in order.items)
```

### 2. 搬移函数 (Move Method)
**适用**: 函数被其他类更多使用

```python
# Before - 在 Order 类中
class Order:
    def calculate_discount(self, coupon):
        return coupon.rate * self.total

# After - 移到 Coupon 类
class Coupon:
    def calculate_discount(self, order_total):
        return self.rate * order_total
```

### 3. 以多态取代条件表达式 (Replace Conditional with Polymorphism)
**适用**: 复杂的 if-else 或 switch

```python
# Before
class Bird:
    def get_migration_speed(self):
        if self.type == "EUROPEAN_SWALLOW":
            return 24
        elif self.type == "AFRICAN_SWALLOW":
            return 18
        elif self.type == "NORWEGIAN_BLUE":
            return 0
        return 0

# After
class Bird(ABC):
    @abstractmethod
    def get_migration_speed(self): pass

class EuropeanSwallow(Bird):
    def get_migration_speed(self): return 24

class AfricanSwallow(Bird):
    def get_migration_speed(self): return 18

class NorwegianBlue(Bird):
    def get_migration_speed(self): return 0
```

### 4. 引入参数对象 (Introduce Parameter Object)
**适用**: 一组参数总是一起出现

```python
# Before
def book_flight(origin, origin_code, origin_city, 
                destination, destination_code, destination_city):
    pass

# After
@dataclass
class Airport:
    name: str
    code: str
    city: str

def book_flight(origin: Airport, destination: Airport):
    pass
```

### 5. 保留完整对象 (Preserve Whole Object)
**适用**: 从对象取多个值传入

```python
# Before
def send_email(to_name, to_email, from_name, from_email, subject, body):
    pass

# After
@dataclass
class EmailAddress:
    name: str
    email: str

def send_email(to: EmailAddress, from_addr: EmailAddress, 
               subject: str, body: str):
    pass
```

## 重构优先级矩阵

| 异味 | 修改频率 | 影响范围 | 优先级 |
|------|---------|---------|--------|
| 重复代码 | 高 | 大 | 🔴 紧急 |
| 过长函数 | 高 | 中 | 🔴 紧急 |
| 过度耦合 | 中 | 大 | 🟡 重要 |
| 过大类 | 低 | 大 | 🟡 重要 |
| 过长参数 | 中 | 小 | 🟢 可延后 |
| 命名不当 | 低 | 小 | 🟢 可延后 |

## 重构安全检查清单

重构前:
- [ ] 有完整的测试覆盖
- [ ] 理解代码的业务逻辑
- [ ] 评估重构风险
- [ ] 制定回滚方案

重构中:
- [ ] 小步提交
- [ ] 频繁运行测试
- [ ] 保持代码可运行
- [ ] 记录重构决策

重构后:
- [ ] 所有测试通过
- [ ] 性能未下降
- [ ] 代码更清晰
- [ ] 文档已更新

## 重构原则

1. **两顶帽子原则**: 重构时只重构，不加新功能
2. **小步快走**: 每次只做一个小重构
3. **测试保护**: 没有测试不重构
4. **持续重构**: 童子军规则 - 让代码比来时更干净
5. **价值驱动**: 优先重构经常修改的代码

---

**相关技能**: [[代码审查]] [[架构设计]] [[调试助手]]
