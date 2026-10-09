---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "前 N 筆查詢"
parent: Query insights
nav_order: 10
---

# 前 N 筆查詢

使用查詢洞察監視前 N 筆查詢，可讓您即時掌握指定時間範圍內 (例如過去一小時) 延遲最高或資源耗用最多的查詢。

## 設定前 N 筆查詢監視

您可以依下列指標類型設定前 N 筆查詢監視：

- `latency`
- `cpu`
- `memory`

每個指標都有一組對應的設定：

- `search.insights.top_queries.<metric>.enabled`：設為 `true` 以依該指標[啟用前 N 筆查詢監視](#enabling-top-n-query-monitoring)。
- `search.insights.top_queries.<metric>.window_size`：[設定該指標前 N 筆查詢的視窗大小](#configuring-the-window-size)。
- `search.insights.top_queries.<metric>.top_n_size`：[指定該指標前 N 筆查詢的 N 值](#configuring-the-value-of-n)。

例如，若要依 CPU 使用率啟用前 N 筆查詢監視，請將 `search.insights.top_queries.cpu.enabled` 設為 `true`。如需指定動態設定的各種方式詳細資訊，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

若為需要細緻 API 存取控制的正式環境部署 (例如具有網路區隔的儀表板節點)，請改用 [Query Insights Settings API]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/settings-api/)，而非本頁所示的 Cluster Settings API。Query Insights Settings API 提供同等功能，並具備更強的安全性與更簡化的結構。
{: .tip}

啟用此功能時請務必謹慎，因為它可能耗用系統資源。
{: .important}

## 啟用前 N 筆查詢監視 

當您安裝 `query-insights` 外掛程式時，前 N 筆查詢監視預設為啟用。若要停用前 N 筆查詢監視，請更新所需指標類型的動態叢集設定。例如，若要停用依延遲監視前 N 筆查詢，請更新 `search.insights.top_queries.latency.enabled` 設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.latency.enabled" : false
  }
}
```
{% include copy-curl.html %}

## 設定視窗大小

若要設定監視視窗大小，請更新所需指標類型的 `window_size` 設定。預設的 `window_size` 為 `5m`。例如，若要在 60 分鐘的視窗內收集依延遲排序的前 N 筆查詢，請更新 `search.insights.top_queries.latency.window_size` 設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.latency.window_size" : "60m"
  }
}
```
{% include copy-curl.html %}

## 設定 N 值 

若要設定 N 值，請更新所需指標類型的 `top_n_size` 設定。預設的 `top_n_size` 為 `10`。例如，若要收集依延遲排序的前 20 筆查詢，請更新 `insights.top_queries.latency.top_n_size` 設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.latency.top_n_size" : 20
  }
}
```
{% include copy-curl.html %}

## 設定來源截斷

為最佳化儲存空間使用量，您可以設定前 N 筆查詢記錄中所儲存查詢來源的最大長度 (以字元為單位)。預設的 `max_source_length` 為 `524288` 個字元 (1 MB)。例如，若要將來源長度限制為 1000 個字元，請更新 `search.insights.top_queries.max_source_length` 設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.max_source_length" : 1000
  }
}
```
{% include copy-curl.html %}

將此值設為 `0` 會完全截斷來源，不儲存任何查詢來源資訊。當來源超過最大長度時，會剛好在字元限制處截斷，且回應中的 `source_truncated` 欄位會設為 `true`。
{: .note}


## 監視目前的前 N 筆查詢 

您可以使用 Insights API 端點，擷取目前時間視窗的前 N 筆查詢。此 API 預設會傳回前 N 筆 `latency` 結果。

```json
GET /_insights/top_queries
```
{% include copy-curl.html %}

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型     | 說明
:--- |:---------| :---
`type`    | 字串   | 要擷取前 N 筆查詢資料的指標類型。結果將依此指標以遞減順序排序。有效值為 `latency`、`cpu` 及 `memory`。預設為 `latency`。
`from`    | 字串 | 擷取歷史前 N 筆查詢之時間範圍的開始時間。如需詳細資訊，請參閱[監視歷史前 N 筆查詢](#monitoring-historical-top-n-queries)。
`to`      | 字串 | 擷取歷史前 N 筆查詢之時間範圍的結束時間。如需詳細資訊，請參閱[監視歷史前 N 筆查詢](#monitoring-historical-top-n-queries)。
`id`      | 字串   | 要擷取之特定前 N 筆查詢記錄的 ID。
`verbose` | 布林值  | 指出是否傳回詳細輸出。預設為 `true`。

### 範例回應

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "top_queries" : [
    {
      "timestamp" : 1745021834451,
      "id" : "36506bd2-7bca-4a0a-a6b8-f3e7db2b0745",
      "wlm_group_id" : "DEFAULT_WORKLOAD_GROUP",
      "group_by" : "NONE",
      "indices" : [
        "my-index-0"
      ],
      "source" : """{"size":20,"query":{"bool":{"must":[{"match_phrase":{"message":{"query":"document","slop":0,"zero_terms_query":"NONE","boost":1.0}}},{"match":{"user.id":{"query":"userId","operator":"OR","prefix_length":0,"max_expansions":50,"fuzzy_transpositions":true,"lenient":false,"zero_terms_query":"NONE","auto_generate_synonyms_phrase_query":true,"boost":1.0}}}],"adjust_pure_negative":true,"boost":1.0}}}""",
      "task_resource_usages" : [
        {
          "action" : "indices:data/read/search[phase/query]",
          "taskId" : 28,
          "parentTaskId" : 27,
          "nodeId" : "BBgWzu8QR0qDkR0G45aw8w",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 22664000,
            "memory_in_bytes" : 6604536
          }
        },
        {
          "action" : "indices:data/read/search",
          "taskId" : 27,
          "parentTaskId" : -1,
          "nodeId" : "BBgWzu8QR0qDkR0G45aw8w",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 119000,
            "memory_in_bytes" : 3920
          }
        }
      ],
      "username" : "admin",
      "failed": false,
      "node_id" : "BBgWzu8QR0qDkR0G45aw8w",
      "phase_latency_map" : {
        "expand" : 0,
        "query" : 23,
        "fetch" : 0
      },
      "labels" : {
        "X-Opaque-Id" : "query-label-1"
      },
      "search_type" : "query_then_fetch",
      "source_truncated" : false,
      "total_shards" : 1,
      "user_roles" : [
        "all_access"
      ],
      "measurements" : {
        "memory" : {
          "number" : 6608456,
          "count" : 1,
          "aggregationType" : "NONE"
        },
        "latency" : {
          "number" : 24,
          "count" : 1,
          "aggregationType" : "NONE"
        },
        "cpu" : {
          "number" : 22783000,
          "count" : 1,
          "aggregationType" : "NONE"
        }
      }
    },
    {
      "timestamp" : 1745021826937,
      "id" : "86e161d0-e982-48c2-b8da-e3a3763f2e36",
      "wlm_group_id" : "DEFAULT_WORKLOAD_GROUP",
      "group_by" : "NONE",
      "indices" : [
        "my-index-*"
      ],
      "source" : """{"size":20,"query":{"term":{"user.id":{"value":"userId","boost":1.0}}}}""",
      "task_resource_usages" : [
        {
          "action" : "indices:data/read/search[phase/query]",
          "taskId" : 26,
          "parentTaskId" : 25,
          "nodeId" : "BBgWzu8QR0qDkR0G45aw8w",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 11020000,
            "memory_in_bytes" : 4292272
          }
        },
        {
          "action" : "indices:data/read/search",
          "taskId" : 25,
          "parentTaskId" : -1,
          "nodeId" : "BBgWzu8QR0qDkR0G45aw8w",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 1032000,
            "memory_in_bytes" : 115816
          }
        }
      ],
      "username" : "admin",
      "failed": false,
      "node_id" : "BBgWzu8QR0qDkR0G45aw8w",
      "phase_latency_map" : {
        "expand" : 0,
        "query" : 15,
        "fetch" : 1
      },
      "labels" : { },
      "search_type" : "query_then_fetch",
      "source_truncated" : false,
      "total_shards" : 1,
      "user_roles" : [
        "all_access"
      ],
      "measurements" : {
        "memory" : {
          "number" : 4408088,
          "count" : 1,
          "aggregationType" : "NONE"
        },
        "latency" : {
          "number" : 23,
          "count" : 1,
          "aggregationType" : "NONE"
        },
        "cpu" : {
          "number" : 12052000,
          "count" : 1,
          "aggregationType" : "NONE"
        }
      }
    }
  ]
}
```

</details>

如果您的查詢未傳回任何結果，請確認目標指標類型已啟用前 N 筆查詢監視，且搜尋請求是在目前的[時間視窗](#configuring-the-window-size)內發出。
{: .important}

## 監視歷史前 N 筆查詢

若要查詢歷史前 N 筆結果，請使用 `from` 與 `to` 參數以 ISO 8601 格式指定時間範圍：`YYYY-MM-DD'T'HH:mm:ss.SSSZ`。
例如，若要擷取 2024 年 8 月 25 日 15:00 UTC 至 2024 年 8 月 30 日 17:00 UTC 之間的前 N 筆查詢，請傳送以下請求：

```json
GET /_insights/top_queries?from=2024-08-25T15:00:00.000Z&to=2024-08-30T17:00:00.000Z
```
{% include copy-curl.html %}

若要檢視歷史查詢資料，匯出器類型必須設定為 `local_index`。如需更多資訊，請參閱[設定本機索引匯出器](#configuring-a-local-index-exporter)。
{: .important}

## 匯出前 N 筆查詢資料

您可以設定所需的匯出器，將前 N 筆查詢資料匯出至不同的接收端，以便更好地監視與分析您的 OpenSearch 查詢。支援下列匯出器：
- [Debug 匯出器](#configuring-a-debug-exporter)
- [本機索引匯出器](#configuring-a-local-index-exporter)
- [遠端儲存庫匯出器](#configuring-a-remote-repository-exporter)

### 設定 debug 匯出器

若要使用 debug 匯出器，請將匯出器類型設定為 `debug`：

```json
PUT _cluster/settings
{
  "persistent" : {
      "search.insights.top_queries.exporter.type" : "debug"
  }
}
```
{% include copy-curl.html %}

### 設定本機索引匯出器

預設匯出器為 `local_index`。本機索引匯出器可讓您將前 N 筆查詢資料儲存至在 OpenSearch 網域中自動建立的索引。Query Insights 會依照命名模式 `top_queries-YYYY.MM.dd-hashcode` 建立這些索引，其中 `hashcode` 是根據目前 UTC 日期產生的 5 位數數字。每天會建立一個新索引。若要使用 Top Queries API 或 Query Insights 儀表板查詢歷史前 N 筆資料，您必須啟用本機索引匯出器。

若要使用本機索引匯出器，請將匯出器類型設定為 `local_index`：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.exporter.type" : "local_index"
  }
}
```
{% include copy-curl.html %}

使用 `delete_after_days` 設定（整數）指定本機索引在多少天後自動刪除。Query Insights 每天於 00:05 UTC 執行一次工作，刪除超過指定天數、存放前 N 筆查詢資料的本機索引。`delete_after_days` 的預設值為 7，有效值範圍為 `1` 至 `180`。

例如，若要刪除超過 10 天的本機索引，請傳送以下請求：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.exporter.delete_after_days" : "10"
  }
}
```
{% include copy-curl.html %}

### 設定遠端儲存庫匯出器

遠端儲存庫匯出器可讓您將前 N 筆查詢洞察資料匯出至遠端 blob 儲存庫，並與現有的本機索引匯出器和 debug 匯出器獨立並行運作。匯出的資料會依時間戳記以 JSON 檔案組織，遵循模式 `{path}/top-queries/yyyy/MM/dd/HH/mm'UTC'/{node-id}-{metric-type}.json`。相較於本機索引，此選項提供更便宜、更長期的儲存解決方案。Query Insights 不會讀取或依賴遠端儲存庫資料，因此您可以使用匯出的資料建立自訂儀表板，或將其匯出以供其他用途使用。資料保留由儲存貯體組態管理，而非由 OpenSearch 管理。

遠端儲存庫匯出器僅支援 Amazon S3 儲存庫。
{: .note}

在設定遠端儲存庫匯出器之前，您必須先註冊遠端儲存庫。如需更多資訊，請參閱[註冊儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#register-repository)。

註冊儲存庫後，請使用下列叢集設定來設定遠端匯出器：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.exporter.remote.repository" : "my-s3-repository",
    "search.insights.top_queries.exporter.remote.path" : "query-insights",
    "search.insights.top_queries.exporter.remote.enabled" : true
  }
}
```
{% include copy-curl.html %}

下表列出可用的遠端匯出器設定。

設定 | 資料類型 | 預設值 | 說明
:--- | :--- | :--- | :---
`search.insights.top_queries.exporter.remote.enabled` | 布林值 | `false` | 啟用遠端儲存庫匯出器。
`search.insights.top_queries.exporter.remote.repository` | 字串 | `null` | 用於匯出資料的已註冊快照儲存庫名稱。啟用遠端匯出時為必要。
`search.insights.top_queries.exporter.remote.path` | 字串 | `query-insights` | 儲存庫內用於組織匯出檔案的基本路徑。

## 從前 N 筆查詢中排除索引

您可以根據搜尋查詢的目標索引，將其從前 N 筆查詢清單中排除。當已知某些索引存在長時間執行的查詢且不需要監視時，這項功能非常實用。

如果查詢搜尋了屬於 `excluded_indices` 所列索引的任何分片，則該查詢會被排除。

預設情況下，此設定為 `null`（包含所有索引）。若要排除特定索引，請在 `search.insights.top_queries.excluded_indices` 設定中提供以逗號分隔的索引名稱清單：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.excluded_indices" : "index-1,index-2,index-3"
  }
}
```
{% include copy-curl.html %}