// Content Script - 页面元素分析

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyze') {
    const elements = analyzePage();
    sendResponse({ elements });
  }
  return true;
});

// 分析页面元素
function analyzePage() {
  const elements = [];
  
  // 可交互元素
  const interactiveSelectors = [
    'a[href]',
    'button',
    'input',
    'select',
    'textarea',
    '[onclick]',
    '[role="button"]',
    '[tabindex]'
  ];
  
  // 内容元素
  const contentSelectors = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'img', 'video', 'audio',
    'article', 'section', 'nav', 'header', 'footer'
  ];
  
  // 表单元素
  const formSelectors = [
    'form',
    'input[type="text"]',
    'input[type="email"]',
    'input[type="password"]',
    'input[type="search"]',
    'input[type="number"]',
    'input[type="checkbox"]',
    'input[type="radio"]'
  ];
  
  // 收集可交互元素
  document.querySelectorAll(interactiveSelectors.join(', ')).forEach(el => {
    if (isVisible(el)) {
      elements.push({
        type: 'interactive',
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        class: el.className || null,
        text: el.textContent?.trim().substring(0, 50) || null,
        href: el.href || null,
        rect: getRect(el)
      });
    }
  });
  
  // 收集内容元素
  document.querySelectorAll(contentSelectors.join(', ')).forEach(el => {
    if (isVisible(el)) {
      elements.push({
        type: 'content',
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        class: el.className || null,
        text: el.textContent?.trim().substring(0, 50) || null,
        src: el.src || null,
        rect: getRect(el)
      });
    }
  });
  
  // 收集表单元素
  document.querySelectorAll(formSelectors.join(', ')).forEach(el => {
    if (isVisible(el)) {
      elements.push({
        type: 'form',
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        class: el.className || null,
        name: el.name || null,
        placeholder: el.placeholder || null,
        rect: getRect(el)
      });
    }
  });
  
  return elements;
}

// 检查元素是否可见
function isVisible(el) {
  const style = window.getComputedStyle(el);
  return style.display !== 'none' && 
         style.visibility !== 'hidden' && 
         style.opacity !== '0' &&
         el.offsetWidth > 0 &&
         el.offsetHeight > 0;
}

// 获取元素位置
function getRect(el) {
  const rect = el.getBoundingClientRect();
  return {
    x: Math.round(rect.left),
    y: Math.round(rect.top),
    width: Math.round(rect.width),
    height: Math.round(rect.height),
    centerX: Math.round(rect.left + rect.width / 2),
    centerY: Math.round(rect.top + rect.height / 2)
  };
}

// 页面加载完成后自动标记
console.log('🤖 Auto Test Assistant loaded');
