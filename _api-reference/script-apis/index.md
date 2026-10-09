---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼 API"
has_children: true
has_toc: false
nav_order: 90
redirect_from:
  - /opensearch/rest-api/script-apis/
  - /api-reference/script-apis/
---

# 指令碼 API
**於 1.0 版導入**
{: .label .label-purple }

指令碼 API 可讓您在 OpenSearch 中使用已儲存與內嵌指令碼。預設的指令碼語言是 Painless。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 指令碼類型

OpenSearch 支援兩種指令碼類型：

- **內嵌指令碼**：直接定義於 API 請求中的指令碼。每次執行時都會重新編譯。
- **已儲存指令碼**：預先編譯並儲存在叢集狀態中的指令碼，可跨多個請求重複使用。它們可縮短編譯時間並提升搜尋速度。


## 指令碼 API 操作

OpenSearch 支援下列指令碼 API 操作。

### 內嵌指令碼操作

直接執行指令碼，而不將其儲存至叢集狀態：

- [執行內嵌指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/)

### 已儲存指令碼操作

管理儲存在叢集狀態中的預先編譯指令碼：

- [建立或更新已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)
- [執行已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-stored-script/) 
- [取得已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-stored-script/)
- [刪除已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/delete-script/)

### 指令碼資訊

取得可用指令碼內容與語言的相關資訊：

- [取得指令碼內容]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-contexts/) - 列出已儲存指令碼可用的內容
- [取得指令碼語言]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-language/) - 列出支援的指令碼語言
