---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "非同步搜尋"
nav_order: 40
parent: Improving search performance
has_children: true
redirect_from:
  - /search-plugins/async/
---

# 非同步搜尋

搜尋大量資料可能需要很長的時間，尤其是當您跨暖節點或多個遠端叢集進行搜尋時。

OpenSearch 的非同步搜尋可讓您傳送在背景執行的搜尋請求。您可以監視這些搜尋的進度，並在部分結果可用時取得這些結果。搜尋完成後，您可以儲存結果，以便日後檢視。

## REST API
於 1.0 版推出
{: .label .label-purple }

若要執行非同步搜尋，請將請求傳送至 `_plugins/_asynchronous_search`，並在請求本文中放入您的查詢：

```json
POST _plugins/_asynchronous_search
```

您可以指定下列選項。

選項 | 說明 | 預設值 | 必要
:--- | :--- |:--- |:--- |
`wait_for_completion_timeout` | 您打算等待結果的時間長度。您可以在此時間內看到取得的任何結果，就像一般搜尋一樣。您可以根據 ID 輪詢剩餘的結果。最大值為 300 秒。 | 1 秒 | 否
`keep_on_completion` | 您是否要在搜尋完成後將結果儲存在叢集中。您可以稍後再檢視儲存的結果。 | `false` | 否
`keep_alive` | 結果儲存在叢集中的時間長度。例如，`2d` 表示結果會儲存在叢集中 48 小時。儲存的搜尋結果會在此期間過後或搜尋取消時刪除。請注意，這包含查詢執行時間。如果查詢超過此時間，程序會自動取消此查詢。 | 12 小時 | 否
`index` | 要搜尋的索引名稱。可以是個別名稱、以逗號分隔的索引清單，或索引名稱的萬用字元運算式。 | 叢集中的所有索引 | 否

#### 範例請求

```json
POST _plugins/_asynchronous_search/?pretty&size=10&wait_for_completion_timeout=1ms&keep_on_completion=true&request_cache=false
{
  "aggs": {
    "city": {
      "terms": {
        "field": "city",
        "size": 10
      }
    }
  }
}
```

#### 範例回應

```json
{
  "*id*": "FklfVlU4eFdIUTh1Q1hyM3ZnT19fUVEUd29KLWZYUUI3TzRpdU5wMjRYOHgAAAAAAAAABg==",
  "state": "RUNNING",
  "start_time_in_millis": 1599833301297,
  "expiration_time_in_millis": 1600265301297,
  "response": {
    "took": 15,
    "timed_out": false,
    "terminated_early": false,
    "num_reduce_phases": 4,
    "_shards": {
      "total": 21,
      "successful": 4,
      "skipped": 0,
      "failed": 0
    },
    "hits": {
      "total": {
        "value": 807,
        "relation": "eq"
      },
      "max_score": null,
      "hits": []
    },
    "aggregations": {
      "city": {
        "doc_count_error_upper_bound": 16,
        "sum_other_doc_count": 403,
        "buckets": [
          {
            "key": "downsville",
            "doc_count": 1
          },
        ....
        ....
        ....
          {
            "key": "blairstown",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```

#### 回應參數

選項 | 說明
:--- | :---
`id` | 非同步搜尋的 ID。使用此 ID 來監視搜尋的進度、取得其部分結果，以及/或刪除結果。如果非同步搜尋在逾時期間內完成，回應不會包含此 ID，因為結果不會儲存在叢集中。
`state` | 指定搜尋仍在執行或已完成，以及結果是否保存在叢集中。可能的狀態為 `RUNNING`、`SUCCEEDED`、`FAILED`、`PERSISTING`、`PERSIST_SUCCEEDED`、`PERSIST_FAILED`、`CLOSED` 及 `STORE_RESIDENT`。
`start_time_in_millis` | 開始時間 (毫秒)。
`expiration_time_in_millis` | 到期時間 (毫秒)。
`took` | 搜尋執行的總時間。
`response` | 實際的搜尋回應。
`num_reduce_phases` | 協調節點從各批次分片回應彙總結果的次數 (預設為 5)。如果此數字比上次擷取的結果增加，您可以預期搜尋回應中會包含其他結果。
`total` | 執行搜尋的分片總數。
`successful` | 協調節點成功收到的分片回應數。
`aggregations` | 分片到目前為止已完成的部分彙總結果。

## 取得部分結果
於 1.0 版推出
{: .label .label-purple }

提交非同步搜尋請求後，您可以使用非同步搜尋回應中所見的 ID 來請求部分回應。

```json
GET _plugins/_asynchronous_search/{ID}?pretty
```

#### 範例回應

```json
{
  "id": "Fk9lQk5aWHJIUUltR2xGWnpVcWtFdVEURUN1SWZYUUJBVkFVMEJCTUlZUUoAAAAAAAAAAg==",
  "state": "STORE_RESIDENT",
  "start_time_in_millis": 1599833907465,
  "expiration_time_in_millis": 1600265907465,
  "response": {
    "took": 83,
    "timed_out": false,
    "_shards": {
      "total": 20,
      "successful": 20,
      "skipped": 0,
      "failed": 0
    },
    "hits": {
      "total": {
        "value": 1000,
        "relation": "eq"
      },
      "max_score": 1,
      "hits": [
        {
          "_index": "bank",
          "_id": "1",
          "_score": 1,
          "_source": {
            "email": "amberduke@abc.com",
            "city": "Brogan",
            "state": "IL"
          }
        },
       {....}
      ]
    },
    "aggregations": {
      "city": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 997,
        "buckets": [
          {
            "key": "belvoir",
            "doc_count": 2
          },
          {
            "key": "aberdeen",
            "doc_count": 1
          },
          {
            "key": "abiquiu",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```

成功保存回應後，您會在回應中取得 `STORE_RESIDENT` 狀態。

您可以使用 `wait_for_completion_timeout` 參數輪詢該 ID，以等待您指定時間內收到的結果。

對於 `keep_on_completion` 為 `true` 且 `keep_alive` 時間夠長的非同步搜尋，您可以持續輪詢 ID，直到搜尋完成。如果您不想定期輪詢每個 ID，可以使用 `keep_alive` 參數將結果保留在叢集中，並稍後再回來查看。

## 刪除搜尋與結果
於 1.0 版推出
{: .label .label-purple }

若要刪除非同步搜尋：

```
DELETE _plugins/_asynchronous_search/{ID}?pretty
```

- 如果搜尋仍在執行，OpenSearch 會取消它。
- 如果搜尋已完成，OpenSearch 會刪除儲存的結果。


#### 範例回應

```json
{
  "acknowledged": "true"
}
```

## 監視統計資料
於 1.0 版推出
{: .label .label-purple }

您可以使用 stats API 作業來監視正在執行、已完成及/或已保存的非同步搜尋。

```json
GET _plugins/_asynchronous_search/stats
```

#### 範例回應

```json
{
  "_nodes": {
    "total": 8,
    "successful": 8,
    "failed": 0
  },
  "cluster_name": "264071961897:asynchronous-search",
  "nodes": {
    "JKEFl6pdRC-xNkKQauy7Yg": {
      "asynchronous_search_stats": {
        "submitted": 18236,
        "initialized": 112,
        "search_failed": 56,
        "search_completed": 56,
        "rejected": 18124,
        "persist_failed": 0,
        "cancelled": 1,
        "running_current": 399,
        "persisted": 100
      }
    }
  }
}
```

#### 回應參數

選項 | 說明
:--- | :---
`submitted` | 已提交的非同步搜尋請求數。
`initialized` | 已初始化的非同步搜尋請求數。
`rejected` | 已拒絕的非同步搜尋請求數。
`search_completed` | 以成功回應完成的非同步搜尋請求數。
`search_failed` | 以失敗回應完成的非同步搜尋請求數。
`persisted` | 最終結果成功保存在叢集中的非同步搜尋請求數。
`persist_failed` | 最終結果無法保存在叢集中的非同步搜尋請求數。
`running_current` | 在指定協調節點上執行的非同步搜尋請求數。
`cancelled` | 在搜尋執行期間取消的非同步搜尋請求數。
