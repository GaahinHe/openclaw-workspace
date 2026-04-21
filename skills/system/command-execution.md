# 命令执行技能 (Command Execution)

## 描述
运行 shell 命令和脚本，执行系统操作

## 使用场景
- 执行系统命令
- 运行脚本
- 文件操作
- 服务管理

## 命令执行工具

### exec 工具
```
工具：exec
参数：command, workdir, env, timeout, pty

示例:
exec(command="ls -la")
exec(command="python script.py", workdir="/path")
exec(command="npm install", timeout=60)
```

### process 工具
```
工具：process
动作：list, poll, log, write, kill

用于管理后台进程
```

## 常用命令分类

### 文件操作
```bash
# 查看
ls -la           # 详细列表
pwd              # 当前目录
cat file.md      # 查看内容
head -n 20 file  # 前 20 行
tail -f file.log # 跟踪日志

# 复制移动
cp src dst       # 复制
mv src dst       # 移动/重命名
rm file          # 删除
trash file       # 移到回收站

# 创建
mkdir dir        # 创建目录
touch file       # 创建空文件
```

### 文本处理
```bash
# 搜索
grep "pattern" file
grep -r "pattern" dir/
grep -i "pattern"  # 忽略大小写

# 替换
sed 's/old/new/g' file
sed -i 's/old/new/g' file  # 原地修改

# 统计
wc -l file         # 行数
wc -w file         # 单词数
```

### 系统信息
```bash
# 系统
uname -a           # 系统信息
hostname           # 主机名
whoami             # 当前用户

# 性能
top                # 进程监控
htop               # 增强版 top
df -h              # 磁盘空间
free -h            # 内存使用

# 网络
ping host          # 连通性
curl url           # HTTP 请求
wget url           # 下载
```

### 进程管理
```bash
# 查看
ps aux             # 所有进程
ps aux | grep xxx  # 搜索进程
pgrep xxx          # 按名搜索

# 控制
kill PID           # 终止进程
kill -9 PID        # 强制终止
pkill name         # 按名终止

# 后台
command &          # 后台运行
nohup command &    # 忽略挂起
```

### Git 操作
```bash
# 状态
git status
git log --oneline

# 提交
git add .
git commit -m "msg"
git push

# 分支
git branch
git checkout -b new
git merge main
```

### 网络服务
```bash
# 端口
lsof -i :8080      # 查看端口
netstat -tulpn     # 网络状态

# SSH
ssh user@host      # 连接
scp file user@host:/path  # 复制
```

## 安全规范

### 高风险命令 (需确认)
```bash
❌ 危险命令 (执行前必须确认):
rm -rf /           # 删除根目录
rm -rf ~           # 删除家目录
dd if=/dev/zero    # 磁盘操作
mkfs               # 格式化
chmod 777          # 权限设置
sudo               # 提权操作
```

### 安全实践
```
✅ 建议:
- 使用 trash 而非 rm
- 重要操作前备份
- 测试命令用小范围
- 避免在生产环境直接执行

✅ 检查清单:
- [ ] 命令正确吗？
- [ ] 路径对吗？
- [ ] 有备份吗？
- [ ] 影响范围？
- [ ] 可回滚吗？
```

## 脚本编写

### Shell 脚本模板
```bash
#!/bin/bash
set -e  # 出错即停

# 变量
DATE=$(date +%Y%m%d)
BACKUP_DIR="/path/backup"

# 函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 主逻辑
log "开始备份..."
mkdir -p "$BACKUP_DIR"
cp -r source "$BACKUP_DIR/backup-$DATE"
log "备份完成"
```

### Python 脚本模板
```python
#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("开始执行")
    try:
        # 主逻辑
        pass
    except Exception as e:
        logger.error(f"错误：{e}")
        sys.exit(1)
    logger.info("执行完成")

if __name__ == "__main__":
    main()
```

## 错误处理

### 常见错误
```bash
# 权限拒绝
Permission denied → 检查权限或加 sudo

# 命令不存在
Command not found → 检查是否安装

# 文件不存在
No such file → 检查路径

# 磁盘满
No space left → 清理空间
```

### 错误处理策略
```bash
# 检查命令存在
if command -v git &> /dev/null; then
    git --version
else
    echo "Git 未安装"
    exit 1
fi

# 检查文件存在
if [ -f "file.md" ]; then
    cat file.md
else
    echo "文件不存在"
    exit 1
fi

# 捕获错误
command || echo "命令失败"
command || exit 1  # 失败则退出
```

## 输出处理

### 重定向
```bash
# 标准输出
command > output.txt      # 覆盖
command >> output.txt     # 追加

# 标准错误
command 2> error.txt      # 错误输出
command &> all.txt        # 所有输出

# 丢弃
command > /dev/null       # 丢弃输出
command 2>&1 > /dev/null  # 丢弃所有
```

### 管道
```bash
# 管道传递
ls -la | grep ".md" | wc -l

# tee 同时输出和保存
command | tee output.txt

# xargs 参数传递
find . -name "*.md" | xargs wc -l
```

## 示例对话

**用户**: 帮我检查 OpenClaw 的状态

**助手**:

好的，让我检查 OpenClaw 的状态。

```bash
# 1. 检查进程
ps aux | grep openclaw

# 2. 检查端口
lsof -i :18789

# 3. 检查配置
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 4. 查看日志
tail -50 /tmp/openclaw/openclaw-*.log
```

执行结果：

```
✅ 进程：运行中 (PID: 12345)
✅ 端口：18789 已监听
✅ 配置：语法正确
✅ 日志：最近无错误
```

**状态**: 🟢 正常

需要我执行其他检查吗？

---

**相关技能**: [[文件管理]] [[系统管理]] [[屏幕自动化]]
