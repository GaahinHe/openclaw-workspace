# 📋 Notion Clipper Pro

> 智能网页剪藏工具 - 将网页内容一键保存到 Notion

**版本**: 1.0.0  
**作者**: Hans  
**兼容**: Chrome / Edge / Brave 等 Chromium 浏览器

---

## ✨ 功能特性

### 核心功能
- ✅ **智能内容提取** - 自动识别正文，过滤广告和导航
- ✅ **Markdown 格式** - 完美兼容 Notion
- ✅ **元数据保存** - 自动提取标题、作者、来源、时间
- ✅ **两种模式** - 保存整页 / 保存选中内容
- ✅ **快捷键支持** - 快速操作无需鼠标

### 技术特点
- 🎯 Manifest V3 标准
- 🔒 纯前端实现，无需后端
- 🚀 轻量快速，无外部依赖
- 📱 响应式设计

---

## 📦 安装方法

### 方法 1: 本地加载（开发测试）

1. **下载项目**
   ```bash
   cd ~/.openclaw/workspace
   # 项目已在 notion-clipper-pro 目录
   ```

2. **打开扩展管理**
   - Chrome/Edge: `edge://extensions/` 或 `chrome://extensions/`
   - 开启 **开发者模式**（右上角开关）

3. **加载插件**
   - 点击 **加载已解压的扩展程序**
   - 选择 `notion-clipper-pro` 文件夹
   - ✅ 安装完成

### 方法 2: 发布到商店（后续）

```bash
# 打包为 ZIP
cd notion-clipper-pro
zip -r ../notion-clipper-pro.zip .

# 上传到 Edge Add-ons
# https://partner.microsoft.com/dashboard
```

---

## 🎯 使用方法

### 方式 1: 右键菜单
1. 选中网页文字
2. 右键点击 → **📋 保存到 Notion**

### 方式 2: 工具栏按钮
1. 点击插件图标
2. 选择 **保存整页** 或 **保存选中内容**

### 方式 3: 快捷键
- **保存整页**: `Cmd+Shift+N` (Mac) / `Ctrl+Shift+N` (Win)
- **保存选中**: `Cmd+Shift+S` (Mac) / `Ctrl+Shift+S` (Win)

### 粘贴到 Notion
1. 打开 Notion
2. `Cmd+V` / `Ctrl+V` 粘贴
3. ✅ 自动转换为 Notion 块

---

## 📁 项目结构

```
notion-clipper-pro/
├── manifest.json          # 插件配置
├── background.js          # 后台服务
├── content.js            # 页面脚本
├── popup/
│   ├── popup.html        # 弹出界面
│   └── popup.js          # 界面逻辑
├── icons/                # 图标文件
└── README.md             # 说明文档
```

---

## 🔧 技术实现

### 内容提取算法

1. **智能识别正文**
   - 优先查找 `<article>` 标签
   - 启发式评分（文本密度、链接密度、段落数量）
   - 移除无关元素（导航、广告、侧边栏）

2. **HTML 转 Markdown**
   - 递归处理 DOM 节点
   - 支持标题、段落、列表、链接、图片等
   - 保留基本格式（粗体、斜体、代码）

3. **元数据提取**
   - Open Graph 标签优先
   - 降级到 HTML 元素
   - 域名作为网站名称

### 权限说明

| 权限 | 用途 |
|------|------|
| `activeTab` | 获取当前标签页信息 |
| `contextMenus` | 右键菜单 |
| `storage` | 保存用户设置 |
| `scripting` | 注入内容脚本 |
| `clipboardWrite` | 复制到剪贴板 |

---

## 🎨 自定义

### 修改样式

编辑 `popup/popup.html` 中的 `<style>` 部分。

### 修改提取规则

编辑 `content.js` 中的：
- `articleSelectors` - 文章容器选择器
- `removeSelectors` - 要移除的元素
- `htmlToMarkdown()` - Markdown 转换逻辑

### 添加功能

在 `background.js` 中添加消息处理，在 `content.js` 中实现功能。

---

## 🐛 故障排查

### 插件不工作
1. 检查是否已加载插件
2. 刷新页面后重试
3. 查看控制台错误（F12）

### 无法复制内容
1. 确保页面不是特殊页面（chrome://, edge://）
2. 检查剪贴板权限
3. 尝试手动复制

### 提取内容不完整
1. 某些网站使用动态加载
2. 尝试滚动页面后再保存
3. 使用"保存选中内容"手动选择

---

## 📝 更新日志

### v1.0.0 (2026-02-26)
- ✅ 初始版本发布
- ✅ 智能内容提取
- ✅ Markdown 格式化
- ✅ 右键菜单和快捷键
- ✅ 设置管理

---

## 🚀 后续计划

- [ ] Notion API 直接写入
- [ ] AI 内容摘要
- [ ] 标签分类管理
- [ ] 保存历史记录
- [ ] 批量操作
- [ ] 自定义模板

---

## 📄 许可证

MIT License

---

## 💬 反馈

如有问题或建议，欢迎反馈！
