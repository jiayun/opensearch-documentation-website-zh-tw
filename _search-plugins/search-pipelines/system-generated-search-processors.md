---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "系統產生的搜尋處理器"
nav_order: 50
has_children: false
parent: Search pipelines
---

# 系統產生的搜尋處理器
**3.3 版新增**
{: .label .label-purple }

系統產生的搜尋處理器是 OpenSearch 根據搜尋請求自動建立的處理器。與您在管線中手動設定的[使用者自訂處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-processors/)不同，系統產生的處理器會在使用特定功能時自動觸發，無需手動設定處理器。

## 啟用系統產生的搜尋處理器

若要啟用系統產生搜尋處理器的建立功能，請將 `cluster.search.enabled_system_generated_factories` 叢集設定設為 `*` (所有工廠)，或明確列出您要啟用的工廠。以下範例啟用 `mmr_over_sample_factory`、`mmr_rerank_factory` 和 `semantic-highlighter`：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.search.enabled_system_generated_factories": [
      "mmr_over_sample_factory",
      "mmr_rerank_factory",
      "semantic-highlighter"
    ]
  }
}
```
{% include copy-curl.html %}

## 處理器類型

OpenSearch 支援下列類型的系統產生處理器：

* [搜尋請求處理器](#system-generated-search-request-processors)
* [搜尋回應處理器](#system-generated-search-response-processors)

每個系統產生的處理器都在固定的執行階段執行，也就是在同類型使用者自訂處理器之前或之後。
{: .note}

### 系統產生的搜尋請求處理器

下表列出可用的系統產生搜尋請求處理器。

| 處理器名稱    | 處理器工廠名稱    | 執行階段     | 觸發條件                                          | 說明                                                                                                                                         |
| ----------------- | ------------------------- | ------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mmr_over_sample` | `mmr_over_sample_factory` | 在所有使用者自訂請求處理器之後執行。 | 當搜尋請求在 `ext` 物件中包含 `mmr` 參數時觸發。請參閱[使用 MMR 重新排序的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/vector-search-mmr/)。 | 調整 `knn` 或 `neural` 查詢的查詢大小與 `k` 值，以對候選結果進行超額取樣，供最大邊際相關性 (MMR) 重新排序使用。 |
| `knn_default_excludes` | `knn_default_excludes_factory` | 在所有使用者自訂請求處理器之前執行。 | 對每個搜尋請求觸發，但請求已透過將 `_source` 設為 `true` 或 `false`，或將 `stored_fields` 設為 `_none_` 來指定如何回傳來源的情況除外。僅適用於包含已啟用 `_source` 的 `knn_vector` 欄位的索引。請參閱[自動從搜尋結果中排除向量]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-search/#automatically-exclude-vectors-from-search-results)。 | 將所有 `knn_vector` 欄位加入 `_source.excludes`，使向量預設不會出現在搜尋回應中。已在請求的 `_source.includes` 或 `_source.excludes` 中列出的欄位則保持不變。 |

### 系統產生的搜尋回應處理器

下表列出可用的系統產生搜尋回應處理器。

| 處理器名稱 | 處理器工廠名稱 | 執行階段    | 觸發條件                                          | 說明                                                                                                                               |
| -------------- | ---------------------- | ------------------ | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `mmr_rerank`   | `mmr_rerank_factory`   | 在所有使用者自訂回應處理器之前執行。 | 當搜尋請求在 `ext` 物件中包含 `mmr` 參數時觸發。請參閱[使用 MMR 重新排序的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/vector-search-mmr/)。 | 使用 MMR 對超額取樣的結果重新排序，並將其縮減為原始查詢大小。  |
| `semantic-highlighter` | `semantic-highlighter` | 在所有使用者自訂回應處理器之後執行。 | 當搜尋請求包含 `type` 設為 `semantic` 的 `highlight` 物件，且在 `ext` 物件中包含 `semantic_highlighting_batch` 參數時觸發。請參閱[`semantic` 高亮顯示器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/#the-semantic-highlighter)。 | 為語意高亮顯示執行批次推論處理。 |

## 限制

系統產生的處理器有下列限制：

- 針對特定搜尋請求，OpenSearch 對**每種處理器類型與執行階段僅支援一個系統產生的處理器**。由於每種處理器類型 (請求與回應) 可以在兩個執行階段 (使用者自訂處理器之前或之後) 執行，單一搜尋請求可以包含多個系統產生的處理器，只要它們屬於不同類型或在不同的執行階段執行即可。此限制可確保確定性的執行順序與可預測的行為。

## 相關文件

- [使用 MMR 重新排序的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/vector-search-mmr/)
- [自動從搜尋結果中排除向量]({{site.url}}{{site.baseurl}}/vector-search/performance-tuning-search/#automatically-exclude-vectors-from-search-results)