# Docker Desktop 安装指南

## 方法一：手动下载（推荐）

### 步骤 1：下载 Docker Desktop

访问以下链接之一下载：

**官方链接：**
- Apple Silicon (M1/M2/M3): https://desktop.docker.com/mac/main/arm64/Docker.dmg
- Intel: https://desktop.docker.com/mac/main/amd64/Docker.dmg

**国内镜像（需要代理）：**
- 阿里云: https://mirrors.aliyun.com/docker-desktop/

### 步骤 2：安装

1. 打开下载的 `.dmg` 文件
2. 将 Docker.app 拖动到Applications文件夹
3. 启动 Docker Desktop
4. 按照向导完成配置

### 步骤 3：验证安装

```bash
docker --version
docker-compose --version
```

---

## 方法二：使用 Homebrew（可能失败）

```bash
# 安装 Docker Desktop
brew install --cask docker

# 启动 Docker Desktop
open -a Docker
```

---

## 方法三：使用命令行安装（仅限 Linux）

如果你在 Linux 服务器上：

```bash
# 使用官方脚本安装
curl -fsSL https://get.docker.com | sh

# 或者使用 Docker 官方仓库
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

---

## 安装后配置

### 1. 启动 Docker Desktop 后，在终端执行：

```bash
# 验证 Docker
docker run hello-world
```

### 2. 配置 Docker 镜像加速

在 Docker Desktop 中：
- Preferences → Docker Engine
- 添加镜像加速地址：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
```

---

## 验证安装

```bash
# 检查 Docker 版本
docker --version
# Docker version 24.0.7

# 检查 Docker Compose
docker-compose --version
# Docker Compose version v2.21.0

# 运行测试容器
docker run hello-world
```

---

## 常见问题

### Q: Docker 启动失败？
A: 检查系统要求（macOS 11+），重启电脑

### Q: 权限问题？
A: 执行 `sudo usermod -aG docker $USER`（Linux）

### Q: 下载慢？
A: 配置 Docker 镜像加速器
