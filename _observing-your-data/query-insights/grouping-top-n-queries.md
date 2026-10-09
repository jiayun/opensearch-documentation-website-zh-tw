---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將前 N 筆查詢分組"
parent: Query insights
nav_order: 20
---

# 將前 N 筆查詢分組
**於 2.17 版推出**
{: .label .label-purple }

監視[前 N 筆查詢]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/)可協助您依據指定時間範圍內的延遲、CPU 及記憶體使用量，找出最耗用資源的查詢。然而，若單一運算成本高昂的查詢被執行多次，可能會佔用所有前 N 筆查詢的名額，進而導致其他高成本查詢無法出現在清單中。為解決此問題，您可以將類似的查詢分組，以深入了解各種高影響力的查詢群組。

## 依相似度將查詢分組

依 `similarity` 將查詢分組，會依據查詢結構來組織查詢，移除核心查詢操作以外的所有內容。

例如，下列查詢：

```json
{
  "query": {
    "bool": {
      "must": [
        { "exists": { "field": "field1" } }
      ],
      "query_string": {
        "query": "search query"
      }
    }
  }
}
```

具有下列對應的查詢結構：

```c
bool
  must
    exists
  query_string
```

當查詢共用相同的查詢結構時，便會歸為同一組，確保所有類似的查詢都屬於同一個群組。

## 設定查詢結構

上述範例查詢顯示的是簡化的查詢結構。根據預設，查詢結構也會包含欄位名稱及欄位資料類型。

例如，假設有一個索引 `index1` 具有下列欄位對應：

```json
"mappings": {
  "properties": {
    "field1": {
      "type": "keyword"
    },
    "field2": {
      "type": "text"
    },
    "field3": {
      "type": "text"
    },
    "field4": {
      "type": "long"
    }
  }
}
```

若您對此索引執行下列查詢：

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "field1": "example_value"
          }
        }
      ],
      "filter": [
        {
          "match": {
            "field2": "search_text"
          }
        },
        {
          "range": {
            "field4": {
              "gte": 1,
              "lte": 100
            }
          }
        }
      ],
      "should": [
        {
          "regexp": {
            "field3": ".*"
          }
        }
      ]
    }
  }
}
```

則該查詢具有下列對應的查詢結構：

```c
bool []
  must:
    term [field1, keyword]
  filter:
    match [field2, text]
    range [field4, long]
  should:
    regexp [field3, text]
```

若要從查詢結構中排除欄位名稱及欄位資料類型，請設定下列設定：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.grouping.attributes.field_name" : false,
    "search.insights.top_queries.grouping.attributes.field_type" : false
  }
}
```
{% include copy-curl.html %}

## 各群組的彙總指標

除了擷取個別前 N 筆查詢的延遲、CPU 及記憶體指標之外，您也可以取得前 N 筆查詢群組的彙總統計資料。回應中會針對每個查詢群組包含下列統計資料：
- 總延遲、CPU 使用量或記憶體使用量（視設定的指標類型而定）
- 查詢總數

您可以利用這些統計資料，計算每個查詢群組的平均延遲、CPU 使用量或記憶體使用量。
回應中也會包含該查詢群組中的一個範例查詢。

## 設定查詢分組

若要設定前 N 筆查詢的分組，請使用下列步驟。

本頁的範例使用 Cluster Settings API。若為需要細緻 API 存取控制的正式部署環境，您可以改用 [Query Insights Settings API]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/settings-api/)，其提供相同的功能並強化了安全性。
{: .tip}

### 步驟 1：啟用前 N 筆查詢監視

請確認已針對至少一種指標啟用前 N 筆查詢監視：延遲、CPU 或記憶體。如需詳細資訊，請參閱[設定前 N 筆查詢監視]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/#configuring-top-n-query-monitoring)。

例如，若要使用預設設定依延遲啟用前 N 筆查詢監視，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.latency.enabled" : true
  }
}
```
{% include copy-curl.html %}

### 步驟 2：設定查詢分組

藉由更新下列叢集設定來設定所需的分組方法：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.grouping.group_by" : "similarity"
  }
}
```
{% include copy-curl.html %}

`group_by` 設定的預設值為 `none`，其會停用分組。`group_by` 支援的值為 `similarity` 及 `none`。

### 步驟 3（選用）：限制受監視的查詢群組數目

您也可以選擇限制受監視的查詢群組數目。已納入前 N 筆查詢清單（最耗用資源的查詢）的查詢，將不會納入限制的判定。基本上，此上限僅適用於其他查詢群組，前 N 筆查詢則會個別追蹤。這有助於依據工作負載及查詢時間範圍大小來管理查詢群組的追蹤。

若要將追蹤限制為 100 個查詢群組，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent" : {
    "search.insights.top_queries.grouping.max_groups_excluding_topn" : 100
  }
}
```
{% include copy-curl.html %}

`max_groups_excluding_topn` 的預設值為 `100`，您可以將其設為 `0` 到 `10,000` 之間的任何值（含頭尾）。

## 監視查詢群組

若要檢視前 N 筆查詢群組，請傳送下列請求：

```json
GET /_insights/top_queries
```
{% include copy-curl.html %}

回應中包含前 N 筆查詢群組：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "top_queries" : [
    {
      "timestamp" : 1770931952020,
      "id" : "51ac5963-d73c-4f6b-992a-5138b9047be0",
      "total_shards" : 1,
      "wlm_group_id" : "DEFAULT_WORKLOAD_GROUP",
      "query_group_hashcode" : "de0332051d2bf67681386dd2985000dc",
      "task_resource_usages" : [
        {
          "action" : "indices:data/read/search[phase/query]",
          "taskId" : 50,
          "parentTaskId" : 61,
          "nodeId" : "V1yz4VnKSCKEycWsrlyAbw",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 14479000,
            "memory_in_bytes" : 6284264
          }
        },
        {
          "action" : "indices:data/read/search",
          "taskId" : 61,
          "parentTaskId" : -1,
          "nodeId" : "ADfsi3bpRweDLK1GMbNBWg",
          "taskResourceUsage" : {
            "cpu_time_in_nanos" : 1415000,
            "memory_in_bytes" : 390848
          }
        }
      ],
      "username": "admin",
      "failed": false,
      "user_roles": [
        "all_access"
      ],
      "node_id" : "ADfsi3bpRweDLK1GMbNBWg",
      "labels" : { },
      "search_type" : "query_then_fetch",
      "source_truncated" : false,
      "phase_latency_map" : {
        "expand" : 0,
        "query" : 38,
        "fetch" : 2
      },
      "source" : "{\"query\":{\"match_all\":{\"boost\":1.0}}}",
      "indices" : [
        "my-index"
      ],
      "group_by" : "SIMILARITY",
      "measurements" : {
        "memory" : {
          "number" : 6675112,
          "count" : 1,
          "aggregationType" : "AVERAGE"
        },
        "cpu" : {
          "number" : 15894000,
          "count" : 1,
          "aggregationType" : "AVERAGE"
        },
        "latency" : {
          "number" : 52,
          "count" : 1,
          "aggregationType" : "AVERAGE"
        }
      }
    }
  ]
}
```

</details>

## 回應本文欄位

回應中包含下列欄位。

欄位 | 資料類型        | 說明
:--- |:-----------------| :---
`top_queries` | 陣列            | 前幾名查詢群組的清單。
`top_queries.timestamp` | 整數          | 查詢群組中第一筆查詢的執行時間戳記。
`top_queries.id` | 字串           | 查詢或查詢群組的唯一識別碼。
`top_queries.total_shards` | 整數          | 執行第一筆查詢時所用的分片數。
`top_queries.failed` | 布林值           | 指出搜尋請求在執行期間是否失敗。
`top_queries.wlm_group_id` | 字串           | 查詢群組中第一筆查詢的工作負載管理群組 ID。
`top_queries.query_group_hashcode` | 字串           | 可唯一識別查詢群組的雜湊碼，由[查詢結構](#grouping-queries-by-similarity)產生。
`top_queries.task_resource_usages` | 物件陣列 | 查詢群組中第一筆查詢所屬各項工作的資源使用量明細。
`top_queries.username` | 字串           | 與查詢群組中第一筆查詢相關聯的使用者名稱。
`top_queries.user_roles` | 陣列            | 與傳送查詢群組中第一筆查詢之使用者相關聯的安全性角色。
`top_queries.node_id` | 字串           | 協調查詢群組中第一筆查詢執行之節點的節點 ID。
`top_queries.labels` | 物件           | 用於標示前幾名查詢。
`top_queries.search_type` | 字串           | 搜尋請求的執行類型。有效值為 `query_then_fetch` 及 `dfs_query_then_fetch`。請參閱 [Search API 文件]({{site.url}}{{site.baseurl}}/api-reference/search/#query-parameters)中的 `search_type` 參數。
`top_queries.source_truncated` | 布林值          | 查詢群組中第一筆查詢的來源欄位是否遭到截斷。如需詳細資訊，請參閱[設定來源截斷]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/#configuring-source-truncation)。
`top_queries.phase_latency_map` | 物件           | 查詢群組中第一筆查詢的協調器階段延遲對應。此對應包含查詢在 `expand`、`query` 及 `fetch` 階段所花費的時間（以毫秒為單位）。
`top_queries.source` | 物件           | 查詢群組中第一筆查詢的來源。
`top_queries.indices` | 陣列            | 查詢群組中第一筆查詢所指定的索引。
`top_queries.group_by` | 字串           | 執行查詢時所套用的 `group_by` 設定。
`top_queries.measurements` | 物件           | 查詢群組的彙總量測值。
`top_queries.measurements.<metric>` | 物件           | 指標的彙總量測值。
`top_queries.measurements.<metric>.number` | 整數          | 查詢群組中所有查詢的累計指標值。
`top_queries.measurements.<metric>.count` | 整數          | 查詢群組中的查詢數。
`top_queries.measurements.<metric>.aggregationType` | 字串           | 目前項目的彙總類型。若已啟用依相似度分組，則 `aggregationType` 為 `AVERAGE`。若未啟用，則 `aggregationType` 為 `NONE`。 