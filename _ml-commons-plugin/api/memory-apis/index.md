---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對話記憶 API"
parent: ML Commons APIs
has_children: true
has_toc: false
nav_order: 50
redirect_from:
  - /ml-commons-plugin/api/memory-apis/
---

# 對話記憶 API
**於 2.12 版推出**
{: .label .label-purple }

對話記憶 API 提供實作[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)所需的操作。對話記憶會儲存目前對話的歷程。訊息代表使用者與大型語言模型之間的一次問答互動。訊息會歸入對話記憶。

ML Commons 支援下列對話記憶層級 API：

- [建立或更新對話記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/create-memory/)
- [取得對話記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-memory/)
- [搜尋對話記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/search-memory/)
- [刪除對話記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/delete-memory/)

ML Commons 支援下列訊息層級 API：

- [建立或更新訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/create-message/)
- [取得訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message/)
- [搜尋訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/search-message/)
- [取得訊息追蹤]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message-traces/)

啟用 Security 外掛程式時，所有對話記憶都會以 `private` 安全性模式存在。只有建立對話記憶的使用者可以與該對話記憶及其訊息互動。
{: .important}