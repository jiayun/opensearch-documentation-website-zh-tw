---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Query Insights 外掛程式健康狀態"
parent: Query insights
nav_order: 50
---

# Query Insights 外掛程式健康狀態

Query Insights 外掛程式提供 [API](#health-stats-api) 與[指標](#opentelemetry-error-metrics-counters)來監控其健康狀態與效能，讓您能主動識別可能影響查詢處理或系統資源的問題。

## Health Stats API
**2.18 版新增**
{: .label .label-purple }

Health Stats API 為每個執行 Query Insights 外掛程式的節點提供健康狀態指標。這些指標可讓您深入檢視資源使用情況以及查詢處理元件的健康狀態。

### 端點

```json
GET _insights/health_stats
```

### 範例請求

```json
GET _insights/health_stats
```
{% include copy-curl.html %}

### 範例回應

回應包含每個節點的一組健康狀態相關欄位：

```json
GET _insights/health_stats
{
  "AqegbPL0Tv2XWvZV4PTS8Q": {
    "ThreadPoolInfo": {
      "query_insights_executor": {
        "type": "scaling",
        "core": 1,
        "max": 5,
        "keep_alive": "5m",
        "queue_size": 2
      }
    },
    "QueryRecordsQueueSize": 2,
    "TopQueriesHealthStats": {
      "latency": {
        "TopQueriesHeapSize": 5,
        "QueryGroupCount_Total": 0,
        "QueryGroupCount_MaxHeap": 0
      },
      "memory": {
        "TopQueriesHeapSize": 5,
        "QueryGroupCount_Total": 0,
        "QueryGroupCount_MaxHeap": 0
      },
      "cpu": {
        "TopQueriesHeapSize": 5,
        "QueryGroupCount_Total": 0,
        "QueryGroupCount_MaxHeap": 0
      }
    },
    "FieldTypeCacheStats" : {
      "size_in_bytes" : 336,
      "entry_count" : 3,
      "evictions" : 1,
      "hit_count" : 5,
      "miss_count" : 4
    }
  }
}
```

### 回應欄位

下表列出所有回應本文欄位。

欄位 | 資料類型        | 說明
:--- |:---| :---
`ThreadPoolInfo` | 物件 | Query Insights 執行緒集區的相關資訊，包括類型、核心數、最大執行緒數與佇列大小。請參閱 [ThreadPoolInfo 物件](#the-threadpoolinfo-object)。
`QueryRecordsQueueSize` | 整數 | 在處理前緩衝傳入搜尋查詢的佇列大小。數值偏高可能表示負載增加或處理速度變慢。
`TopQueriesHealthStats` | 物件 | 每個熱門查詢服務的效能指標，提供記憶體配置 (堆積大小) 與查詢分組的相關資訊。請參閱 [TopQueriesHealthStats 物件](#the-topquerieshealthstats-object)。
`FieldTypeCacheStats` | 物件 | Query Insights 欄位類型快取的指標。此快取用於在啟用查詢分組時儲存欄位類型對應。

### ThreadPoolInfo 物件

`ThreadPoolInfo` 物件包含專屬於 Query Insights 外掛程式的執行緒集區的下列詳細組態與效能資料。

欄位 | 資料類型        | 說明
:--- |:---| :---
`type`| 字串 | 執行緒集區類型 (例如 `scaling`)。
`core`| 整數 | 執行緒集區中的最小執行緒數。
`max`| 整數 | 執行緒集區中的最大執行緒數。
`keep_alive`| 時間單位 | 閒置執行緒的保留時間。
`queue_size`| 整數 | 佇列中的最大工作數。

### TopQueriesHealthStats 物件

`TopQueriesHealthStats` 物件提供延遲、記憶體與 CPU 使用量的細部分析，並包含下列資訊。

欄位 | 資料類型        | 說明
:--- |:---| :---
`TopQueriesHeapSize`| 整數 | 查詢群組的堆積記憶體配置。
`QueryGroupCount_Total`| 整數 | 已處理查詢群組的總數。
`QueryGroupCount_MaxHeap`| 整數 | 在記憶體中儲存所有查詢群組的最大堆積大小。

### FieldTypeCacheStats 物件

`FieldTypeCacheStats` 物件包含下列統計資料。

欄位 | 資料類型        | 說明
:--- |:---| :---
`size_in_bytes`| 整數 | 快取的堆積記憶體配置。
`entry_count`| 整數 | 快取項目的總數。
`evictions`| 整數 | 快取驅逐的總次數。
`hit_count`| 整數 | 快取命中的總次數。
`miss_count`| 整數 | 快取未命中的總次數。

## OpenTelemetry 錯誤指標計數器

Query Insights 外掛程式與 OpenTelemetry 整合，以提供即時的錯誤指標計數器。這些計數器有助於識別外掛程式中特定的作業失敗並提升可靠性。每個指標都針對外掛程式工作流程中的潛在錯誤來源提供深入洞察，讓除錯與維護工作更聚焦。

若要收集這些指標，您必須設定並收集查詢指標。如需更多資訊，請參閱[查詢指標]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/query-metrics/)。

下表列出所有可用的指標。

欄位 | 說明
:--- | :---
`LOCAL_INDEX_READER_PARSING_EXCEPTIONS` | 使用 LocalIndexReader 解析資料時發生的錯誤次數。
`LOCAL_INDEX_EXPORTER_BULK_FAILURES` | 將 Query Insights 外掛程式資料匯入本機索引時發生的失敗次數。
`LOCAL_INDEX_EXPORTER_DELETE_FAILURES` | 刪除 Query Insights 本機索引時發生的失敗次數。
`LOCAL_INDEX_EXPORTER_EXCEPTIONS` | Query Insights 外掛程式 LocalIndexExporter 中發生的例外次數。
`INVALID_EXPORTER_TYPE_FAILURES` | 無效匯出器類型的失敗次數。
`DATA_INGEST_EXCEPTIONS` | 將資料匯入 Query Insights 外掛程式時發生的例外次數。
`QUERY_CATEGORIZE_EXCEPTIONS` | 對查詢進行分類時發生的例外次數。
`EXPORTER_FAIL_TO_CLOSE_EXCEPTION` | 關閉匯出器時發生的失敗次數。
`READER_FAIL_TO_CLOSE_EXCEPTION` | 關閉讀取器時發生的失敗次數。
`TOP_N_QUERIES_USAGE_COUNT` | Top N Queries API 的使用次數。
`TOP_N_QUERIES_SOURCE_TRUNCATION` | 查詢來源因大小限制而被截斷的次數。