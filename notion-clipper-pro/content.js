/**
 * Notion Clipper Pro - Content Script
 * 
 * 核心功能：
 * 1. 提取页面内容（智能识别正文）
 * 2. 获取用户选中内容
 * 3. 复制到剪贴板
 * 4. 清理无关元素
 * 
 * @author Hans
 * @version 1.0.0
 */

// ==================== 消息监听 ====================

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSelection') {
    // 获取选中内容
    const selection = getSelectedText();
    sendResponse(selection);
  }

  if (request.action === 'getPageContent') {
    // 获取页面内容
    const content = extractPageContent();
    sendResponse(content);
  }

  if (request.action === 'copyToClipboard') {
    // 复制到剪贴板
    copyToClipboard(request.text);
    sendResponse({ success: true });
  }

  return true;
});

// ==================== 内容提取 ====================

/**
 * 获取用户选中的文本
 */
function getSelectedText() {
  const selection = window.getSelection();
  if (selection && selection.toString().trim()) {
    return {
      text: selection.toString().trim(),
      html: getSelectionHtml(selection)
    };
  }
  return null;
}

/**
 * 获取选中内容的 HTML
 */
function getSelectionHtml(selection) {
  if (selection.rangeCount > 0) {
    const container = document.createElement('div');
    for (let i = 0; i < selection.rangeCount; i++) {
      container.appendChild(selection.getRangeAt(i).cloneContents());
    }
    return container.innerHTML;
  }
  return '';
}

/**
 * 智能提取页面正文内容
 * 
 * 算法：
 * 1. 移除无关元素（导航、广告、侧边栏等）
 * 2. 查找内容最密集的区域
 * 3. 提取标题、作者、发布时间等元数据
 */
function extractPageContent() {
  const content = {
    title: extractTitle(),
    content: extractMainContent(),
    author: extractAuthor(),
    siteName: extractSiteName(),
    timestamp: extractTimestamp()
  };

  console.log('[Notion Clipper] 提取的内容:', content);
  return content;
}

/**
 * 提取页面标题
 */
function extractTitle() {
  // 优先级：OG 标签 > h1 > title
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle && ogTitle.content) {
    return ogTitle.content.trim();
  }

  const h1 = document.querySelector('h1');
  if (h1 && h1.textContent.trim()) {
    return h1.textContent.trim();
  }

  return document.title.trim();
}

/**
 * 提取正文内容
 */
function extractMainContent() {
  // 1. 尝试查找文章容器
  const articleSelectors = [
    'article',
    '[role="article"]',
    '.post-content',
    '.article-content',
    '.entry-content',
    '.post',
    '.article',
    '#content',
    '.content'
  ];

  let mainElement = null;
  for (const selector of articleSelectors) {
    mainElement = document.querySelector(selector);
    if (mainElement) break;
  }

  // 2. 如果没找到，使用启发式算法
  if (!mainElement) {
    mainElement = findContentHeuristic();
  }

  // 3. 提取并清理内容
  if (mainElement) {
    return cleanContent(mainElement);
  }

  // 4. 降级：使用整个 body
  return cleanContent(document.body);
}

/**
 * 启发式查找内容区域
 */
function findContentHeuristic() {
  const candidates = [];
  
  // 查找所有可能的内容容器
  const elements = document.querySelectorAll('div, section, main');
  
  elements.forEach(el => {
    const score = scoreElement(el);
    if (score > 0) {
      candidates.push({ element: el, score });
    }
  });

  // 返回得分最高的
  if (candidates.length > 0) {
    candidates.sort((a, b) => b.score - a.score);
    return candidates[0].element;
  }

  return document.body;
}

/**
 * 给元素打分（内容密度评估）
 */
function scoreElement(el) {
  const text = el.textContent.trim();
  const textLength = text.length;
  
  // 文本太少的排除
  if (textLength < 100) return 0;

  // 链接密度
  const links = el.querySelectorAll('a');
  const linkText = Array.from(links).reduce((sum, link) => sum + link.textContent.length, 0);
  const linkDensity = textLength > 0 ? linkText / textLength : 0;

  // 段落数量
  const paragraphs = el.querySelectorAll('p');
  
  // 打分逻辑
  let score = textLength / 100;  // 基础分
  
  // 链接密度低加分（内容更可能是正文）
  if (linkDensity < 0.3) score += 20;
  
  // 段落多加分
  score += paragraphs.length * 5;

  // 负面标签减分
  const negativeClasses = ['nav', 'footer', 'sidebar', 'ad', 'comment'];
  const className = el.className.toLowerCase();
  for (const neg of negativeClasses) {
    if (className.includes(neg)) score -= 10;
  }

  return score;
}

/**
 * 清理内容（移除无关元素，转换为 Markdown）
 */
function cleanContent(element) {
  // 克隆节点，避免修改原页面
  const clone = element.cloneNode(true);

  // 移除不需要的元素
  const removeSelectors = [
    'script', 'style', 'noscript',
    'nav', 'footer', 'header',
    '.ad', '.ads', '.advertisement',
    '.sidebar', '.comments', '.related',
    '[class*="nav"]', '[class*="footer"]',
    '[class*="sidebar"]', '[class*="ad"]'
  ];

  removeSelectors.forEach(selector => {
    clone.querySelectorAll(selector).forEach(el => el.remove());
  });

  // 转换为 Markdown
  return htmlToMarkdown(clone);
}

/**
 * HTML 转 Markdown
 */
function htmlToMarkdown(element) {
  let markdown = '';

  // 处理文本节点
  function processNode(node, depth = 0) {
    if (node.nodeType === Node.TEXT_NODE) {
      markdown += node.textContent;
      return;
    }

    if (node.nodeType !== Node.ELEMENT_NODE) return;

    const tagName = node.tagName.toLowerCase();

    // 根据标签类型处理
    switch (tagName) {
      case 'h1':
        markdown += '\n\n# ';
        processChildren(node);
        markdown += '\n\n';
        break;

      case 'h2':
        markdown += '\n\n## ';
        processChildren(node);
        markdown += '\n\n';
        break;

      case 'h3':
        markdown += '\n\n### ';
        processChildren(node);
        markdown += '\n\n';
        break;

      case 'p':
        markdown += '\n\n';
        processChildren(node);
        break;

      case 'br':
        markdown += '\n';
        break;

      case 'strong':
      case 'b':
        markdown += '**';
        processChildren(node);
        markdown += '**';
        break;

      case 'em':
      case 'i':
        markdown += '*';
        processChildren(node);
        markdown += '*';
        break;

      case 'a':
        const href = node.href;
        markdown += '[';
        processChildren(node);
        markdown += `](${href})`;
        break;

      case 'ul':
      case 'ol':
        markdown += '\n\n';
        processChildren(node);
        markdown += '\n\n';
        break;

      case 'li':
        markdown += '\n- ';
        processChildren(node);
        break;

      case 'blockquote':
        markdown += '\n\n> ';
        processChildren(node);
        markdown += '\n\n';
        break;

      case 'code':
        markdown += '`';
        processChildren(node);
        markdown += '`';
        break;

      case 'pre':
        markdown += '\n\n```\n';
        processChildren(node);
        markdown += '\n```\n\n';
        break;

      case 'img':
        const alt = node.alt || 'image';
        const src = node.src;
        markdown += `![${alt}](${src})`;
        break;

      default:
        processChildren(node);
    }
  }

  function processChildren(node) {
    Array.from(node.childNodes).forEach(child => {
      processNode(child);
    });
  }

  processNode(element);

  // 清理多余空白
  return markdown
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^[ \t]+/gm, '')
    .trim();
}

/**
 * 提取作者
 */
function extractAuthor() {
  const selectors = [
    'meta[name="author"]',
    'meta[property="article:author"]',
    '.author',
    '[class*="author"]',
    'time'
  ];

  for (const selector of selectors) {
    const el = document.querySelector(selector);
    if (el) {
      return el.content || el.textContent.trim();
    }
  }

  return null;
}

/**
 * 提取网站名称
 */
function extractSiteName() {
  const ogSiteName = document.querySelector('meta[property="og:site_name"]');
  if (ogSiteName && ogSiteName.content) {
    return ogSiteName.content.trim();
  }

  // 从域名提取
  try {
    const url = new URL(window.location.href);
    return url.hostname.replace('www.', '');
  } catch {
    return null;
  }
}

/**
 * 提取发布时间
 */
function extractTimestamp() {
  const selectors = [
    'meta[property="article:published_time"]',
    'meta[name="date"]',
    'time[datetime]',
    'time[pubdate]'
  ];

  for (const selector of selectors) {
    const el = document.querySelector(selector);
    if (el) {
      return el.content || el.dateTime;
    }
  }

  return null;
}

// ==================== 剪贴板操作 ====================

/**
 * 复制到剪贴板（使用现代 API）
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    console.log('[Notion Clipper] 复制成功');
  } catch (err) {
    // 降级方案：使用 execCommand
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
      document.execCommand('copy');
      console.log('[Notion Clipper] 复制成功（降级方案）');
    } catch (e) {
      console.error('[Notion Clipper] 复制失败:', e);
    }
    
    document.body.removeChild(textarea);
  }
}

console.log('[Notion Clipper Pro] Content script loaded');
