---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對話記憶 API"
parent: ML APIs
has_children: true
has_toc: false
nav_order: 50
redirect_from:
  - /ml-commons-plugin/api/memory-apis/
---

# 記憶 API
**於 2.12 版導入**
{: .label .label-purple }

記憶 API 提供實作[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)所需的操作。記憶 (memory) 會儲存目前對話的歷程。訊息 (message) 代表使用者與大型語言模型之間的一次問答互動。訊息會組織在記憶之中。

OpenSearch 支援下列記憶 API：

- [建立或更新記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/create-memory/)
- [取得記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-memory/)
- [搜尋記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/search-memory/)
- [刪除記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/delete-memory/)

OpenSearch 支援下列訊息 API：

- [建立或更新訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/create-message/)
- [取得訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message/)
- [搜尋訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/search-message/)
- [取得訊息追蹤]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message-traces/)

啟用 Security 外掛程式時，所有記憶都存在於 `private` 安全性模式。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}