/**
 * Notion Clipper Pro - Background Service Worker
 * 
 * 核心功能：
 * 1. 管理右键菜单
 * 2. 处理保存请求
 * 3. 生成 Markdown 格式内容
 * 4. 复制到剪贴板
 * 
 * @author Hans
 * @version 1.0.0
 */

// ==================== 初始化 ====================

// 插件安装/更新时初始化
chrome.runtime.onInstalled.addListener((details) => {
  console.log('[Notion Clipper] 插件已安装/更新', details.reason);
  createContextMenu();
  initializeStorage();
});

// 初始化右键菜单
function createContextMenu() {
  chrome.contextMenus.removeAll(() => {
    // 保存选中内容
    chrome.contextMenus.create({
      id: 'save-selection',
      title: '📋 保存到 Notion',
      contexts: ['selection']
    });

    // 保存整页
    chrome.contextMenus.create({
      id: 'save-page',
      title: '📄 保存整页到 Notion',
      contexts: ['page']
    });
  });
}

// 初始化存储
function initializeStorage() {
  chrome.storage.local.get(['settings'], (result) => {
    if (!result.settings) {
      chrome.storage.local.set({
        settings: {
          format: 'markdown',
          includeMetadata: true,
          autoCopy: true
        }
      });
    }
  });
}

// ==================== 右键菜单处理 ====================

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'save-selection') {
    // 保存选中内容
    handleSaveSelection(tab);
  } else if (info.menuItemId === 'save-page') {
    // 保存整页
    handleSavePage(tab);
  }
});

// ==================== 快捷键处理 ====================

chrome.commands.onCommand.addListener((command) => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      if (command === 'save-page') {
        handleSavePage(tabs[0]);
      } else if (command === 'save-selection') {
        handleSaveSelection(tabs[0]);
      }
    }
  });
});

// ==================== 核心保存逻辑 ====================

/**
 * 处理保存选中内容
 */
function handleSaveSelection(tab) {
  chrome.tabs.sendMessage(tab.id, { action: 'getSelection' }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('[Notion Clipper] 发送消息失败:', chrome.runtime.lastError);
      showNotification('错误：无法获取选中内容');
      return;
    }

    if (response && response.text) {
      const content = formatAsMarkdown({
        title: getSelectionTitle(response.text),
        content: response.text,
        url: tab.url,
        timestamp: new Date().toISOString()
      });

      copyToClipboard(content, () => {
        showNotification('✅ 选中内容已复制到剪贴板');
      });
    } else {
      showNotification('⚠️ 未选中任何内容');
    }
  });
}

/**
 * 处理保存整页
 */
function handleSavePage(tab) {
  chrome.tabs.sendMessage(tab.id, { action: 'getPageContent' }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('[Notion Clipper] 发送消息失败:', chrome.runtime.lastError);
      showNotification('错误：无法获取页面内容');
      return;
    }

    if (response) {
      const content = formatAsMarkdown({
        title: response.title || tab.title,
        content: response.content,
        url: tab.url,
        timestamp: new Date().toISOString(),
        author: response.author,
        siteName: response.siteName
      });

      copyToClipboard(content, () => {
        showNotification('✅ 页面内容已复制到剪贴板');
      });
    }
  });
}

// ==================== Markdown 格式化 ====================

/**
 * 将内容格式化为 Markdown（Notion 兼容）
 */
function formatAsMarkdown(data) {
  const { title, content, url, timestamp, author, siteName } = data;

  let markdown = '';

  // 标题
  if (title) {
    markdown += `# ${title}\n\n`;
  }

  // 元数据
  markdown += `---\n`;
  markdown += `**来源**: ${url}\n`;
  markdown += `**保存时间**: ${new Date(timestamp).toLocaleString('zh-CN')}\n`;
  
  if (author) {
    markdown += `**作者**: ${author}\n`;
  }
  
  if (siteName) {
    markdown += `**网站**: ${siteName}\n`;
  }
  
  markdown += `---\n\n`;

  // 正文内容
  markdown += `${content}\n`;

  return markdown;
}

/**
 * 从选中内容提取标题（第一行或前 50 字符）
 */
function getSelectionTitle(text) {
  const lines = text.split('\n').filter(line => line.trim());
  if (lines.length > 0) {
    return lines[0].substring(0, 100);
  }
  return '选中内容';
}

// ==================== 剪贴板操作 ====================

/**
 * 复制到剪贴板
 */
function copyToClipboard(text, callback) {
  // 通过 content script 复制到剪贴板
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(
        tabs[0].id,
        { action: 'copyToClipboard', text: text },
        (response) => {
          if (callback) callback();
        }
      );
    }
  });
}

// ==================== 通知显示 ====================

/**
 * 显示通知（使用 chrome.notifications）
 */
function showNotification(message) {
  // 简单版本：通过 badge 显示
  chrome.action.setBadgeText({ text: '✓' });
  chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });

  // 2 秒后清除
  setTimeout(() => {
    chrome.action.setBadgeText({ text: '' });
  }, 2000);

  console.log('[Notion Clipper]', message);
}

// ==================== 消息监听 ====================

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSettings') {
    chrome.storage.local.get(['settings'], (result) => {
      sendResponse(result.settings);
    });
    return true;
  }

  if (request.action === 'updateSettings') {
    chrome.storage.local.set({ settings: request.settings }, () => {
      sendResponse({ success: true });
    });
    return true;
  }
});

console.log('[Notion Clipper Pro] Background service worker initialized');
