// Popup 脚本 - 处理用户交互

document.addEventListener('DOMContentLoaded', async () => {
  const btnAnalyze = document.getElementById('btnAnalyze');
  const btnExport = document.getElementById('btnExport');
  const btnClear = document.getElementById('btnClear');
  const resultsDiv = document.getElementById('results');
  const pageTitleEl = document.getElementById('pageTitle');
  const elementCountEl = document.getElementById('elementCount');
  
  // 获取当前标签页信息
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab) {
    pageTitleEl.textContent = tab.title.length > 30 ? tab.title.substring(0, 30) + '...' : tab.title;
  }
  
  // 分析页面按钮
  btnAnalyze.addEventListener('click', async () => {
    addResult('开始分析页面...', 'normal');
    
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;
    
    try {
      // 发送消息到 content script
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'analyze' });
      
      if (response && response.elements) {
        elementCountEl.textContent = response.elements.length;
        addResult(`✅ 检测到 ${response.elements.length} 个元素`, 'success');
        
        // 显示元素类型统计
        const stats = countByType(response.elements);
        for (const [type, count] of Object.entries(stats)) {
          addResult(`  • ${type}: ${count}`, 'normal');
        }
      } else {
        addResult('⚠️ 无法获取页面元素', 'warning');
      }
    } catch (error) {
      addResult(`❌ 错误：${error.message}`, 'error');
    }
  });
  
  // 导出报告按钮
  btnExport.addEventListener('click', async () => {
    addResult('📥 生成报告中...', 'normal');
    
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;
    
    try {
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'analyze' });
      const report = generateReport(tab, response?.elements || []);
      
      // 保存到 storage
      await chrome.storage.local.set({ lastReport: report });
      addResult('✅ 报告已保存', 'success');
      
      // 通知 background 下载
      chrome.runtime.sendMessage({ action: 'exportReport', report });
    } catch (error) {
      addResult(`❌ 导出失败：${error.message}`, 'error');
    }
  });
  
  // 清除数据按钮
  btnClear.addEventListener('click', async () => {
    await chrome.storage.local.clear();
    resultsDiv.innerHTML = '<div class="result-item">数据已清除</div>';
    elementCountEl.textContent = '-';
  });
  
  // 添加结果到列表
  function addResult(text, type = 'normal') {
    const div = document.createElement('div');
    div.className = `result-item ${type}`;
    div.textContent = text;
    resultsDiv.insertBefore(div, resultsDiv.firstChild);
  }
  
  // 统计元素类型
  function countByType(elements) {
    const stats = {};
    elements.forEach(el => {
      stats[el.type] = (stats[el.type] || 0) + 1;
    });
    return stats;
  }
  
  // 生成报告
  function generateReport(tab, elements) {
    return {
      timestamp: new Date().toISOString(),
      url: tab.url,
      title: tab.title,
      elementCount: elements.length,
      elements: elements,
      summary: countByType(elements)
    };
  }
});
