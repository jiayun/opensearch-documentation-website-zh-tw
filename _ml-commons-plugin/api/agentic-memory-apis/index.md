---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理記憶（agentic memory）API"
parent: ML APIs
has_children: true
has_toc: false
nav_order: 35
redirect_from: 
  - /ml-commons-plugin/api/agentic-memory-apis/
---

# 代理記憶（agentic memory）API
**3.3 版推出**
{: .label .label-purple }

代理記憶 API 為 AI 代理程式提供持久性記憶管理。如需概念概觀、使用案例及入門資訊，請參閱[代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。

## 停用代理記憶 API

代理記憶 API 預設為啟用。若要停用代理記憶 API，請更新下列叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
      "plugins.ml_commons.agentic_memory_enabled": false
  }
}
```
{% include copy-curl.html %}

OpenSearch 支援下列記憶容器 API：

- [建立記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)
- [取得記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory-container/)
- [更新記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory-container/)
- [刪除記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/delete-memory-container/)
- [搜尋記憶容器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory-container/)

OpenSearch 支援下列記憶 API：

- [新增記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/add-memory/)
- [建立工作階段]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-session/)
- [取得記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory/)
- [更新記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory/)
- [刪除記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/delete-memory/)
- [搜尋記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/)
- [語意搜尋記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/semantic-search-memory/)
- [混合搜尋記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/hybrid-search-memory/)
