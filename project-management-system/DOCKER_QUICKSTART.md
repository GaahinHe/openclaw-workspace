# 项目管理系统 - Docker 快速启动

## 前置要求

- [x] Java 21 ✅ (已安装)
- [x] Node.js 20 ✅ (已安装)
- [x] Maven ✅ (已安装)
- [ ] Docker Desktop ⏳ (需手动安装)

## 快速开始

### 1. 安装 Docker Desktop

**必须手动下载安装**：

1. 访问: https://www.docker.com/products/docker-desktop/
2. 下载 **Docker Desktop for Mac (Apple Silicon)**
3. 安装并启动 Docker Desktop

### 2. 启动中间件

```bash
cd /Users/hans/.openclaw/workspace/project-management-system

# 启动所有中间件
docker-compose up -d

# 查看状态
docker-compose ps
```

### 3. 初始化数据库

连接 OceanBase 并执行 SQL：

```bash
# 连接信息
Host: localhost
Port: 2881
Username: root
Password: root123
Database: project_manager
```

执行文件: `docs/init-db.sql`

### 4. 启动服务

```bash
# 后端 (端口 8080)
cd backend
mvn spring-boot:run

# 前端 (端口 3000) - 新开终端
cd frontend
npm install
npm run dev
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端 API | http://localhost:8080 |
| Swagger 文档 | http://localhost:8080/doc.html |
| OceanBase | localhost:2881 |
| Kafka | localhost:9092 |

## 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| test | test123 | 开发者 |

## 常用命令

```bash
# 查看日志
docker-compose logs -f

# 重启中间件
docker-compose restart

# 停止中间件
docker-compose down

# 查看端口占用
lsof -i :8080 -i :3000 -i :2881 -i :9092
```
