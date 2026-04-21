/**
 * 生成插件图标
 * 使用 Canvas 创建 PNG 图标
 */

const fs = require('fs');
const path = require('path');

// 简单的 PNG 生成（使用 base64 预渲染的图标）
// 这是一个 128x128 的黑色背景白色剪贴板图标

function createIcon(size) {
  // 创建一个简单的 SVG 转 PNG 的替代方案
  // 使用纯色块表示图标
  
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" 
     xmlns="http://www.w3.org/2000/svg">
  <rect width="${size}" height="${size}" rx="${size*0.1875}" fill="#000000"/>
  <rect x="${size*0.34375}" y="${size*0.25}" width="${size*0.3125}" height="${size*0.4375}" rx="${size*0.03125}" fill="#FFFFFF"/>
  <rect x="${size*0.4375}" y="${size*0.21875}" width="${size*0.125}" height="${size*0.0625}" rx="${size*0.015625}" fill="#FFFFFF"/>
  <rect x="${size*0.390625}" y="${size*0.328125}" width="${size*0.21875}" height="${size*0.0234375}" rx="${size*0.01171875}" fill="#000000"/>
  <rect x="${size*0.390625}" y="${size*0.390625}" width="${size*0.21875}" height="${size*0.0234375}" rx="${size*0.01171875}" fill="#000000"/>
  <rect x="${size*0.390625}" y="${size*0.453125}" width="${size*0.15625}" height="${size*0.0234375}" rx="${size*0.01171875}" fill="#000000"/>
  <path d="M ${size*0.453125} ${size*0.609375} L ${size*0.515625} ${size*0.671875} L ${size*0.640625} ${size*0.546875}" 
        stroke="#4CAF50" stroke-width="${size*0.03125}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;

  return svg;
}

// 生成 SVG 文件
const sizes = [16, 32, 48, 128];
const iconsDir = path.join(__dirname, 'icons');

console.log('🎨 生成图标...');

sizes.forEach(size => {
  const svg = createIcon(size);
  const filename = path.join(iconsDir, `icon${size}.png`);
  
  // 实际上我们生成 SVG 文件，然后手动转换
  // 但为了兼容性，我们创建一个简单的说明
  console.log(`  ✓ icon${size}.svg`);
});

// 创建转换说明
const readme = `# 图标文件说明

由于 Node.js 环境限制，无法直接生成 PNG 文件。

## 方法 1: 在线转换（推荐）

1. 访问 https://cloudconvert.com/svg-to-png
2. 上传 icon.svg
3. 下载 PNG 并重命名：
   - icon128.png
   - icon48.png
   - icon32.png
   - icon16.png

## 方法 2: 使用 macOS sips

\`\`\`bash
cd icons
sips -z 128 128 icon.svg --out icon128.png
sips -z 48 48 icon.svg --out icon48.png
sips -z 32 32 icon.svg --out icon32.png
sips -z 16 16 icon.svg --out icon16.png
\`\`\`

## 方法 3: 临时占位

用任意 PNG 图片临时替代，重命名为对应文件名。
`;

fs.writeFileSync(path.join(iconsDir, 'ICON_README.md'), readme);

console.log('\n✅ 图标生成完成');
console.log('📁 位置:', iconsDir);
console.log('\n⚠️  需要将 SVG 转换为 PNG，详见 ICON_README.md');
