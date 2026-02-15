# 项目管理系统 (Project Management System)

## 两种启动方式

### 方式一：本地测试（推荐新手）⭐

**无需安装 Docker，直接运行！**

```bash
# 1. 启动后端（使用 H2 内存数据库）
cd ~/.openclaw/workspace/project-management-system
chmod +x start-local.sh start-frontend.sh
./start-local.sh

# 2. 启动前端（新终端）
./start-frontend.sh
```

**特点**：
- ✅ 无需安装数据库
- ✅ 无需安装 Docker
- ✅ 自动创建示例数据
- ⚠️ 数据仅保存在内存（重启丢失）

---

### 方式二：完整部署（生产推荐）

**需要安装 Docker**

见 `docs/DOCKER_INSTALL.md`

---

## 快速开始（本地测试）

### 环境要求

| 组件 | 要求 | 检查命令 |
|------|------|---------|
| Java | 21+ | `java -version` |
| Node.js | 18+ | `node -v` |
| Maven | 3.8+ | `mvn -version` |

### 启动步骤

```bash
# 1. 进入项目目录
cd ~/.openclaw/workspace/project-management-system

# 2. 启动后端（新终端）
chmod +x start-local.sh
./start-local.sh

# 3. 启动前端（新终端）
chmod +x start-frontend.sh
./start-frontend.sh
```

---

## 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端** | http://localhost:3000 | Vue 3 应用 |
| **后端 API** | http://localhost:8080 | Spring Boot |
| **Swagger 文档** | http://localhost:8080/doc.html | API 文档 |
| **H2 控制台** | http://localhost:8080/h2-console | 数据库管理 |

---

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | 123456 |
| 普通用户 | test | 123456 |

---

## 项目功能

### 已完成 ✅

- [x] 用户认证 (JWT 登录/注册)
- [x] 项目管理 (CRUD)
- [x] 任务管理 (CRUD)
- [x] 用户管理 (CRUD)
- [x] Swagger API 文档

### 待实现 ⏳

- [ ] 权限管理 (RBAC)
- [ ] 项目成员管理
- [ ] 任务分配
- [ ] Kafka 消息通知

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Element Plus + Vite |
| 后端 | Spring Boot 3.2 + Java 21 |
| ORM | MyBatis-Plus |
| 认证 | JWT |
| 数据库 | H2（本地测试）/ OceanBase（生产） |

---

## 文件结构

```
project-management-system/
├── start-local.sh          # 本地启动（无需 Docker）
├── start-frontend.sh       # 前端启动
├── backend/
│   ├── pom.xml            # Maven 配置
│   ├── pom-local.xml      # 本地测试配置（H2）
│   └── src/main/
│       ├── resources/
│       │   ├── application.yml        # 生产配置
│       │   └── application-local.yml   # 本地测试配置（H2）
│       └── java/com/projectmanager/
├── frontend/               # Vue 3 前端
└── docs/
    ├── init-db.sql        # OceanBase 数据库脚本
    └── DOCKER_INSTALL.md  # Docker 安装指南
```

---

## 故障排除

### Q: Java 版本不对？

```bash
# 检查 Java 版本
java -version

# 使用 Java 21
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
```

### Q: 前端启动失败？

```bash
# 重新安装依赖
cd frontend
rm -rf node_modules
npm install
```

### Q: 后端启动失败端口被占用？

```bash
# 查看占用端口的进程
lsof -i :8080

# 杀掉进程
kill -9 <PID>
```

---

## 截图

### 登录页面

![登录页面](docs/images/login.png)

### 首页

![首页](docs/images/home.png)

### 项目管理

![项目管理](docs/images/projects.png)

---

## License

MIT
