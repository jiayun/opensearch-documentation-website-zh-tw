---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式記憶體 API"
parent: ML Commons APIs
has_children: true
has_toc: false
nav_order: 35
redirect_from: 
  - /ml-commons-plugin/api/agentic-memory-apis/
---

# 代理程式記憶體 API
**3.3 版推出**
{: .label .label-purple }

代理程式記憶體 API 為 AI 代理程式提供持久性記憶體管理。如需概念概觀、使用案例及入門資訊，請參閱[代理程式記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。

## 停用代理程式記憶體 API

代理程式記憶體 API 預設為啟用。若要停用代理程式記憶體 API，請更新下列叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
      "plugins.ml_commons.agentic_memory_enabled": false
  }
}
```
{% include copy-curl.html %}

OpenSearch 支援下列記憶體容器 API：

- [建立記憶體容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)
- [取得記憶體容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory-container/)
- [更新記憶體容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory-container/)
- [刪除記憶體容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/delete-memory-container/)
- [搜尋記憶體容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory-container/)

OpenSearch 支援下列記憶體 API：

- [新增記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/add-memory/)
- [建立工作階段]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-session/)
- [取得記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory/)
- [更新記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory/)
- [刪除記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/delete-memory/)
- [搜尋記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/)
- [語意搜尋記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/semantic-search-memory/)
- [混合搜尋記憶體]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/hybrid-search-memory/)
