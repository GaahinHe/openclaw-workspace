# Docker Desktop 安装（手动）

由于网络限制，请手动完成以下步骤：

## 步骤 1：下载 Docker Desktop

访问以下链接下载（需要外网）：

**官方下载：**
- Apple Silicon (M1/M2/M3): https://desktop.docker.com/mac/main/arm64/Docker.dmg
- Intel Mac: https://desktop.docker.com/mac/main/amd64/Docker.dmg

**国内镜像（如果有代理）：**
- 使用 Clash Verge 代理访问上述链接

## 步骤 2：安装

1. 打开下载的 `Docker.dmg`
2. 将 `Docker.app` 拖到 `Applications` 文件夹
3. 从 Applications 启动 Docker Desktop

## 步骤 3：启动项目

Docker 安装完成后，在终端执行：

```bash
cd ~/.openclaw/workspace/project-management-system

# 1. 启动中间件（OceanBase, Kafka, Redis）
docker-compose up -d

# 2. 初始化数据库
mysql -h localhost -P 2881 -uroot -proot123 < docs/init-db.sql

# 3. 启动后端（新终端）
cd backend
./mvnw spring-boot:run

# 4. 启动前端（新终端）
cd frontend
npm run dev
```

## 步骤 4：访问

- 前端: http://localhost:3000
- 后端: http://localhost:8080
- 文档: http://localhost:8080/doc.html

## 账号

- admin / 123456
- test / 123456

---

**注意**：Docker Desktop 安装大约需要 5-10 分钟完成。
