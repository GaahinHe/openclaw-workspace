/**
 * Notion Clipper Pro - Popup Script
 * 
 * 功能：
 * 1. 处理用户界面交互
 * 2. 管理设置
 * 3. 触发保存操作
 * 
 * @author Hans
 * @version 1.0.0
 */

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  setupEventListeners();
});

// ==================== 事件监听 ====================

function setupEventListeners() {
  // 保存整页按钮
  document.getElementById('savePageBtn').addEventListener('click', () => {
    savePage();
  });

  // 保存选中内容按钮
  document.getElementById('saveSelectionBtn').addEventListener('click', () => {
    saveSelection();
  });

  // 设置切换
  document.getElementById('autoCopyToggle').addEventListener('change', (e) => {
    saveSettings();
  });

  document.getElementById('metadataToggle').addEventListener('change', (e) => {
    saveSettings();
  });
}

// ==================== 设置管理 ====================

function loadSettings() {
  chrome.storage.local.get(['settings'], (result) => {
    if (result.settings) {
      document.getElementById('autoCopyToggle').checked = result.settings.autoCopy !== false;
      document.getElementById('metadataToggle').checked = result.settings.includeMetadata !== false;
    }
  });
}

function saveSettings() {
  const settings = {
    autoCopy: document.getElementById('autoCopyToggle').checked,
    includeMetadata: document.getElementById('metadataToggle').checked,
    format: 'markdown'
  };

  chrome.storage.local.set({ settings }, () => {
    showStatus('✅ 设置已保存', 'success');
  });
}

// ==================== 保存操作 ====================

function savePage() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0]) return;

    chrome.tabs.sendMessage(tabs[0].id, { action: 'getPageContent' }, (response) => {
      if (chrome.runtime.lastError) {
        showStatus('❌ 无法获取页面内容', 'error');
        return;
      }

      if (response) {
        const content = formatContent(response, tabs[0]);
        copyContent(content);
      }
    });
  });
}

function saveSelection() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0]) return;

    chrome.tabs.sendMessage(tabs[0].id, { action: 'getSelection' }, (response) => {
      if (chrome.runtime.lastError) {
        showStatus('❌ 无法获取选中内容', 'error');
        return;
      }

      if (response && response.text) {
        const content = formatContent(
          {
            title: getSelectionTitle(response.text),
            content: response.text,
            author: null,
            siteName: null,
            timestamp: null
          },
          tabs[0]
        );
        copyContent(content);
      } else {
        showStatus('⚠️ 请先选中要保存的内容', 'error');
      }
    });
  });
}

// ==================== 内容格式化 ====================

function formatContent(data, tab) {
  const { title, content, author, siteName, timestamp } = data;
  
  let markdown = '';

  // 标题
  if (title) {
    markdown += `# ${title}\n\n`;
  }

  // 元数据
  markdown += `---\n`;
  markdown += `**来源**: ${tab.url}\n`;
  markdown += `**保存时间**: ${new Date().toLocaleString('zh-CN')}\n`;
  
  if (author) {
    markdown += `**作者**: ${author}\n`;
  }
  
  if (siteName) {
    markdown += `**网站**: ${siteName}\n`;
  }
  
  markdown += `---\n\n`;

  // 正文
  markdown += `${content}\n`;

  return markdown;
}

function getSelectionTitle(text) {
  const lines = text.split('\n').filter(line => line.trim());
  if (lines.length > 0) {
    return lines[0].substring(0, 100);
  }
  return '选中内容';
}

// ==================== 剪贴板操作 ====================

function copyContent(text) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0]) return;

    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: 'copyToClipboard', text: text },
      (response) => {
        if (chrome.runtime.lastError) {
          showStatus('❌ 复制失败', 'error');
        } else {
          showStatus('✅ 已复制到剪贴板！去 Notion 粘贴吧', 'success');
          
          // 2 秒后关闭 popup
          setTimeout(() => {
            window.close();
          }, 2000);
        }
      }
    );
  });
}

// ==================== 状态显示 ====================

function showStatus(message, type) {
  const statusEl = document.getElementById('statusMessage');
  statusEl.textContent = message;
  statusEl.className = `status ${type}`;

  // 3 秒后隐藏
  setTimeout(() => {
    statusEl.className = 'status';
  }, 3000);
}
