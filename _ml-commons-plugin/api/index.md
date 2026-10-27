---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML API"
nav_order: 110
has_children: true
has_toc: false
redirect_from:
  - /ml-commons-plugin/api/
  - /ml-commons-plugin/api/train-predict/
---

# ML API

OpenSearch 支援下列機器學習 (ML) API：

- [模型 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/)
- [模型群組 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-group-apis/index/)
- [連接器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/index/)
- [代理程式 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/index/)
- [記憶 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/index/)
- [代理記憶（Agentic Memory）API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/)
- [控制器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/index/)
- [執行演算法 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-algorithm/)
- [執行工具 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/)
- [ML 任務 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/index/)
- [Profile API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/profile/)
- [統計 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/stats/)
- [MCP 伺服器 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/)
- [MCP 用戶端 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-client-apis/)

## 記憶 API 比較

OpenSearch 提供兩種不同的記憶系統：

- **[記憶 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/index/)** -- 供[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)使用的簡易對話歷程儲存機制。依時間順序儲存問答配對，不進行處理或學習。

- **[代理記憶 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/)** -- 供 AI 代理程式使用的智慧記憶系統。使用大型語言模型 (LLM) 擷取知識、學習使用者偏好，並跨工作階段維持脈絡。如需概念說明，請參閱[代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。