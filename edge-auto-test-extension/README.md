# Auto Test Assistant - Edge 插件

网页自动化测试助手 - 自动检测页面元素并生成测试报告

## 📦 安装步骤

### 1. 打开 Edge 扩展页面
在 Edge 地址栏输入：
```
edge://extensions/
```

### 2. 启用开发者模式
- 在扩展页面左侧找到 **"开发者模式"** 开关
- 打开开关

### 3. 加载插件
- 点击 **"加载解压缩的扩展"** 按钮
- 选择本文件夹：`~/.openclaw/workspace/edge-auto-test-extension/`
- 确认加载

### 4. 验证安装
- 工具栏会出现 🤖 机器人图标
- 点击图标打开插件面板

---

## 🎯 功能说明

### 分析页面
点击 **"🔍 分析页面"** 按钮：
- 自动检测页面上的所有可交互元素
- 统计按钮、链接、表单等元素数量
- 显示元素类型分布

### 导出报告
点击 **"📥 导出报告"** 按钮：
- 生成 JSON 格式的测试报告
- 包含所有检测到的元素信息
- 自动下载到下载文件夹

### 清除数据
点击 **"🗑️ 清除数据"** 按钮：
- 清除本地存储的测试数据

---

## 🧪 自动化测试

### 使用 Computer Control MCP 测试

```bash
# 1. 激活 Edge
osascript -e 'tell application "Microsoft Edge" to activate'

# 2. 打开测试页面
osascript -e 'tell application "Microsoft Edge" to open location "https://example.com"'

# 3. 等待加载
sleep 2

# 4. 点击插件图标（需要知道图标位置）
cliclick c:1800,50

# 5. 点击"分析页面"按钮
cliclick c:1700,300

# 6. 截图记录
screencapture -x /tmp/test-result.png
```

### 测试脚本

运行自动化测试：
```bash
./scripts/auto-test.sh
```

---

## 📁 文件结构

```
edge-auto-test-extension/
├── manifest.json      # 插件配置
├── popup.html         # 弹出界面
├── popup.js           # 弹出界面逻辑
├── content.js         # 页面内容脚本
├── background.js      # 后台服务
├── icons/             # 图标文件
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── scripts/           # 测试脚本
    └── auto-test.sh
```

---

## 🔧 开发调试

### 查看日志
1. 打开扩展页面 `edge://extensions/`
2. 找到 "Auto Test Assistant"
3. 点击 **"查看视图：background page"**
4. 打开开发者工具查看控制台

### 热重载
修改代码后：
1. 在扩展页面点击 🔄 刷新按钮
2. 重新加载插件

---

## 📊 测试报告格式

```json
{
  "timestamp": "2026-02-27T16:24:00.000Z",
  "url": "https://example.com",
  "title": "Example Domain",
  "elementCount": 15,
  "elements": [...],
  "summary": {
    "interactive": 5,
    "content": 8,
    "form": 2
  }
}
```

---

## 🚀 下一步

- [ ] 添加自动化测试脚本
- [ ] 添加元素截图功能
- [ ] 添加测试用例录制
- [ ] 添加测试报告对比

---

**版本**: 1.0.0  
**创建日期**: 2026-02-27  
**开发者**: Hans TheBot
