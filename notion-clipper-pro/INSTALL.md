# 🚀 Notion Clipper Pro - 快速安装指南

## 第一步：生成图标

由于需要 PNG 格式图标，请选择：

### 选项 A: 使用在线工具（推荐）
1. 访问 https://cloudconvert.com/svg-to-png
2. 上传 `icons/icon.svg`
3. 下载 PNG，调整大小为 128x128
4. 保存为 `icons/icon128.png`
5. 同样生成 16x16, 32x32, 48x48 版本

### 选项 B: 使用命令行（如果有 ImageMagick）
```bash
cd ~/.openclaw/workspace/notion-clipper-pro/icons
convert icon.svg -resize 16x16 icon16.png
convert icon.svg -resize 32x32 icon32.png
convert icon.svg -resize 48x48 icon48.png
convert icon.svg -resize 128x128 icon128.png
```

### 选项 C: 临时跳过
暂时使用任意 PNG 图片作为占位符，后续再替换。

---

## 第二步：加载插件

1. **打开 Edge 浏览器**

2. **进入扩展管理**
   ```
   edge://extensions/
   ```

3. **开启开发者模式**
   - 右上角找到"开发者模式"开关
   - 打开它

4. **加载插件**
   - 点击"加载已解压的扩展程序"
   - 选择文件夹：`~/.openclaw/workspace/notion-clipper-pro`
   - 点击"选择文件夹"

5. **✅ 安装完成**
   - 看到插件出现在列表中
   - 工具栏出现插件图标

---

## 第三步：测试功能

### 测试 1: 保存整页
1. 打开任意网页（如新闻文章）
2. 点击插件图标
3. 点击"保存整页"
4. 看到"✅ 已复制到剪贴板"提示

### 测试 2: 保存选中内容
1. 在网页上选中一段文字
2. 右键点击
3. 选择"📋 保存到 Notion"
4. 看到成功提示

### 测试 3: 快捷键
1. 在任意页面
2. 按下 `Cmd+Shift+N` (Mac) 或 `Ctrl+Shift+N` (Win)
3. 应该触发保存整页

### 测试 4: 粘贴到 Notion
1. 打开 Notion (notion.so)
2. 创建新页面
3. 按 `Cmd+V` / `Ctrl+V` 粘贴
4. ✅ 应该看到格式化的内容

---

## 🐛 常见问题

### Q: 提示"清单文件缺失或不可读"
A: 检查 `manifest.json` 是否在文件夹根目录

### Q: 点击没反应
A: 
1. 刷新页面
2. 检查浏览器控制台（F12）
3. 查看是否有错误信息

### Q: 复制失败
A: 
1. 确保不是特殊页面（chrome://, edge://）
2. 检查剪贴板权限
3. 尝试手动复制粘贴

### Q: 图标不显示
A: 确保 PNG 图标文件存在，或临时使用其他 PNG 图片

---

## 📝 下一步

1. **测试所有功能**
2. **反馈问题或改进建议**
3. **后续功能开发**（Notion API 集成等）

---

**开发完成时间**: 2026-02-26  
**开发者**: Hans
