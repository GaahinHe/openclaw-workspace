# 项目管理系统 - DDNS 与部署配置

## 前置条件

### 1. 阿里云准备
- ✅ 已购买域名：`your-domain.com`
- ⚠️ 获取 AccessKey（见下方）

### 2. 获取阿里云 AccessKey

1. 登录阿里云控制台：https://ram.console.aliyun.com/
2. 访问 **RAM 访问控制** → **用户管理** → **创建用户**
3. 勾选 **OpenAPI 调用访问**，创建 AccessKey
4. **重要**：为该用户添加 **AliyunDNSFullAccess** 权限（仅操作DNS）

### 3. 域名解析设置

在阿里云 DNS 控制台添加记录：
| 记录类型 | 主机记录 | 解析线路 | 记录值 | TTL |
|---------|---------|---------|-------|-----|
| A | home | 默认 | 你的公网IP | 600 |
| A | pm | 默认 | 你的公网IP | 600 |
| A | api | 默认 | 你的公网IP | 600 |

---

## 快速开始

### 第一步：配置环境变量

```bash
# 复制配置模板
cp env.example .env

# 编辑配置
nano .env
```

配置内容：
```env
# 阿里云 API 凭证
ALIBABA_CLOUD_ACCESS_KEY_ID=你的AccessKey_ID
ALIBABA_CLOUD_ACCESS_KEY_SECRET=你的AccessKey_Secret

# 域名配置
DOMAIN_NAME=your-domain.com        # 你的域名
SUB_DOMAIN=pm                        # 子域名（可改）

# 你的公网IP（脚本会自动检测）
CURRENT_IP=
```

### 第二步：运行 DDNS

```bash
# 方式一：手动运行（测试）
./ddns.sh

# 方式二：设置定时任务（推荐）
crontab -e
# 添加：
*/5 * * * * /Users/hans/.openclaw/workspace/ddns-deployment/ddns.sh >> /var/log/ddns.log 2>&1
```

### 第三步：部署项目

```bash
# 赋予执行权限
chmod +x deploy.sh ddns.sh

# 运行部署
./deploy.sh
```

---

## 脚本说明

### ddns.sh
- 功能：检测公网 IP 变化，自动更新阿里云 DNS 解析
- 位置：`~/.openclaw/workspace/ddns-deployment/ddns.sh`
- 日志：`~/ddns.log`

### deploy.sh
- 功能：启动项目管理系统所有服务
- 包含：
  - 前端 (Vue3 + Element Plus) - 端口 3000
  - 后端 (Spring Boot) - 端口 8080
  - 数据库 (OceanBase) - 端口 2881
  - 消息队列 (Kafka) - 端口 9092

---

## 访问地址

部署成功后：

| 服务 | 地址 |
|------|------|
| 前端 | http://pm.your-domain.com:3000 |
| 后端 API | http://api.your-domain.com:8080 |
| Swagger | http://api.your-domain.com:8080/doc.html |

---

## 故障排查

### DDNS 不更新
```bash
# 检查日志
tail -f ~/ddns.log

# 手动测试
./ddns.sh --verbose
```

### Docker 服务启动失败
```bash
# 检查容器状态
cd ~/.openclaw/workspace/project-management-system
docker-compose logs

# 重启服务
docker-compose restart
```

### 端口被占用
```bash
# 查看端口占用
lsof -i :3000
lsof -i :8080
```

---

## 安全建议

1. **AccessKey 权限**：仅授予 DNS 权限，不要给全部权限
2. **防火墙**：仅开放必要端口 (3000, 8080)
3. **HTTPS**：生产环境建议配置 SSL 证书
