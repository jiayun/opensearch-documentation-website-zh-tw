---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋 API"
nav_order: 100
has_children: true
has_toc: false
redirect_from:
  - /api-reference/search-apis/
---

# 搜尋 API
**於 1.0 版推出**
{: .label .label-purple }

OpenSearch 提供一套完整的搜尋相關 API，讓您執行各種搜尋作業、測試及驗證搜尋，以及使用搜尋範本。OpenSearch 支援下列搜尋 API。

本頁列出的端點路徑（例如 `GET /{index}/_search`）皆相對於您的 OpenSearch 主機與連接埠。完整的 URL 格式為 `https://<host>:<port>/{index}/_search`，其中預設連接埠為 `9200`。如需連線至 OpenSearch 的詳細資訊，請參閱[與 OpenSearch 通訊]({{site.url}}{{site.baseurl}}/getting-started/communicate/)。
{: .note}

## 核心搜尋 API

這些 API 構成 OpenSearch 搜尋功能的基礎：

- **[Search]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/)**：針對一或多個索引執行搜尋查詢。
- **[Multi-search]({{site.url}}{{site.baseurl}}/api-reference/search-apis/multi-search/)**：在單次 API 呼叫中執行多個搜尋請求。
- **[Point in Time]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/)**：為搜尋作業建立一致的索引檢視。
- **[Scroll]({{site.url}}{{site.baseurl}}/api-reference/search-apis/scroll/)**：從搜尋查詢擷取大量結果。
- **[Count]({{site.url}}{{site.baseurl}}/api-reference/search-apis/count/)**：取得符合查詢的文件數量。

## 搜尋測試 API

這些 API 可協助您測試、偵錯及最佳化搜尋作業：

- **[Explain]({{site.url}}{{site.baseurl}}/api-reference/search-apis/explain/)**：說明特定文件如何符合（或不符合）查詢。
- **[Field capabilities]({{site.url}}{{site.baseurl}}/api-reference/search-apis/field-caps/)**：取得多個索引中欄位的功能。
- **[Profile]({{site.url}}{{site.baseurl}}/api-reference/search-apis/profile/)**：分析搜尋請求的執行效能。
- **[Ranking evaluation]({{site.url}}{{site.baseurl}}/api-reference/search-apis/rank-eval/)**：評估搜尋結果的品質。
- **[Search shards]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-shards/)**：取得搜尋請求將在哪些分片上執行的資訊。
- **[Validate]({{site.url}}{{site.baseurl}}/api-reference/search-apis/validate/)**：在執行可能耗用大量資源的查詢之前，先驗證該查詢。

## 搜尋範本 API

這些 API 讓您使用搜尋範本：

- **[Search template]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/)**：使用搜尋範本執行參數化搜尋查詢。
- **[Multi-search template]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/msearch-template/)**：在單次 API 呼叫中執行多個搜尋範本請求。
- **[Render template]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/render-template/)**：透過代入參數，預覽搜尋範本產生的最終查詢，而不執行搜尋。
