// Background Service Worker - 后台任务

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'exportReport') {
    exportReport(request.report);
    sendResponse({ success: true });
  }
  return true;
});

// 导出报告为 JSON 文件
function exportReport(report) {
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  chrome.downloads.download({
    url: url,
    filename: `test-report-${new Date().toISOString().slice(0, 19)}.json`,
    saveAs: false
  }, (downloadId) => {
    console.log('Report exported:', downloadId);
  });
}

// 插件安装时
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Auto Test Assistant installed', details.reason);
  
  // 初始化 storage
  chrome.storage.local.set({
    installedAt: new Date().toISOString(),
    version: '1.0.0'
  });
});

// 定时检查（可选）
chrome.alarms?.create('healthCheck', { periodInMinutes: 30 });

chrome.alarms?.onAlarm.addListener((alarm) => {
  if (alarm.name === 'healthCheck') {
    console.log('Health check passed');
  }
});
