---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引統計"
parent: Index operations
grand_parent: Index APIs
nav_order: 120
---

# Index Stats API 
**1.0 版新增**
{: .label .label-purple }

Index Stats API 提供索引統計資訊。對於資料串流，此 API 提供該串流後端索引的統計資訊。預設情況下，傳回的統計資訊為索引層級。若要接收分片層級的統計資訊，請將 `level` 參數設為 `shards`。

當分片移動到不同節點時，該分片的分片層級統計資訊會被清除。雖然該分片已不屬於該節點，節點仍會保留該分片曾貢獻的所有節點層級統計資訊。
{: .note}

<!-- spec_insert_start
api: indices.stats
component: endpoints
-->
## 端點
```json
GET /_stats
GET /{index}/_stats
GET /_stats/{metric}
GET /{index}/_stats/{metric}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 以逗號分隔的索引、資料串流或索引別名清單，用於篩選結果。支援萬用字元運算式。若要擷取所有索引的統計資訊，請使用 `_all` 或 `*`，或省略此參數。 |
| `metric` | 字串 | 以逗號分隔的指標群組清單，用於包含在回應中。有效值請參閱[指標](#metrics)。預設為所有指標。 |

### 指標

下表列出所有可用的指標群組。

指標 | 說明
:--- |:----
`_all` | 傳回所有統計資料。無法與其他指標合併使用。
`completion` | 自動完成建議器 (completion suggester) 統計資料。 
`docs` | 傳回文件數量，以及尚未合併的已刪除文件數量。索引重新整理操作可能會影響此統計資料。 
`fielddata` | 欄位資料統計資料。 
`flush` | 排清統計資料。 
`get` | Get 操作統計資料，包括找不到文件 (missing) 的統計資料。 
`indexing` | 編製索引統計資料。 
`merge` | 合併統計資料。 
`query_cache` | 查詢快取統計資料。 
`recovery` | 復原統計資料，包括分片作為來源 (`current_as_source`) 或目標 (`current_as_target`) 的進行中復原數量，以及復原節流時間 (`throttle_time_in_millis`)。
`refresh` | 重新整理統計資料。 
`request_cache` | 分片請求快取統計資料。 
`search` | 搜尋統計資料，包括建議操作統計資料。搜尋操作可與一個或多個群組相關聯。若要包含自訂群組的統計資料，請在 `groups` 查詢參數中提供以逗號分隔的群組名稱清單。若要傳回所有群組的統計資料，請使用 `_all`。如果設定了 `groups`，`search` 物件會包含一個 `groups` 物件，其中含有每個群組的統計資料。
`segments` | 所有開啟中分段的記憶體使用統計資料。如果 `include_segment_file_sizes` 參數為 `true`，此指標會包含每個 Lucene 索引檔案的彙總磁碟使用量。
`store` | 以位元組為單位的索引大小。 
`translog` | 交易記錄 (translog) 統計資料。 
`warmer` | 預熱器 (warmer) 統計資料。 

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：展開至所有開啟和關閉的索引，包括隱藏索引。<br> - `open`：展開至開啟的索引。<br> - `closed`：展開至關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。
`fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要納入統計資料的欄位。若未提供 `completion_fields` 和 `fielddata_fields`，則此參數會指定預設的欄位清單。
`completion_fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要納入欄位層級 `completion` 統計資料的欄位。
`fielddata_fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要納入欄位層級 `fielddata` 統計資料的欄位。
`forbid_closed_indices` | 布林值 | 若為 `true`，以關閉的索引為目標或將萬用字元展開至關閉索引的請求會傳回錯誤。設定為 `false` 可傳回關閉索引的統計資料。預設為 `true`。
`groups` | 字串 | 以逗號分隔的搜尋群組清單，指定要納入 `search` 統計資料的搜尋群組。搜尋群組是使用 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#search-stats-groups) 的 `stats` 參數指派給搜尋請求的自訂標籤。使用 `_all` 可傳回所有群組的統計資料。
`level` | 字串 | 指定用來彙總統計資料的層級。有效值為：<br> - `cluster`：叢集層級統計資料。<br> - `indices`：索引層級統計資料。<br> - `shards`：分片層級統計資料。<br> 預設為 `indices`。
`include_segment_file_sizes` | 布林值 | 指定是否回報每個 Lucene 索引檔案的彙總磁碟使用量。僅適用於 `segments` 統計資料。預設為 `false`。
`include_unloaded_segments` | 布林值 | 指定是否納入關閉索引的分段統計資料，這些索引的分段不會載入記憶體。僅在 `forbid_closed_indices` 為 `false` 時適用。預設為 `false`。
`ignore_unavailable` | 布林值 | 若為 `true`，回應中會省略不存在或已關閉的索引。若為 `false`，當請求以不存在或已關閉的索引為目標時，會傳回錯誤。預設為 `false`。
`allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值不符合任何索引時，請求會傳回錯誤。預設為 `true`。
`timeout` | 時間 | 等待每個節點回應的時間長度。預設為 `30s`。

## 範例請求

以下範例請求示範如何使用 Index Stats API。

### 單一索引

以下範例傳回單一索引的索引統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /testindex/_stats
-->
{% capture step1_rest %}
GET /testindex/_stats
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  index = "testindex"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 以逗號分隔的索引清單

以下範例傳回多個索引的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /testindex1,testindex2/_stats
-->
{% capture step1_rest %}
GET /testindex1,testindex2/_stats
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  index = "testindex1,testindex2"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 萬用字元運算式

以下範例傳回名稱以 `testindex` 開頭之所有索引的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /testindex*/_stats
-->
{% capture step1_rest %}
GET /testindex*/_stats
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  index = "testindex*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 特定統計資料

下列範例會傳回與重新整理及排清操作相關的索引統計資料：

<!-- spec_insert_start
component: example_code
rest: GET /testindex/_stats/refresh,flush
-->
{% capture step1_rest %}
GET /testindex/_stats/refresh,flush
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  metric = "refresh,flush",
  index = "testindex"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 展開萬用字元

下列範例會傳回名稱以 `testindex` 開頭的所有開啟中索引（包括隱藏索引）的統計資料：

<!-- spec_insert_start
component: example_code
rest: GET /testindex*/_stats?expand_wildcards=open,hidden
-->
{% capture step1_rest %}
GET /testindex*/_stats?expand_wildcards=open,hidden
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  index = "testindex*",
  params = { "expand_wildcards": "open,hidden" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 分片層級統計資料

下列範例會傳回測試索引的分片層級統計資料：

<!-- spec_insert_start
component: example_code
rest: GET /testindex/_stats?level=shards
-->
{% capture step1_rest %}
GET /testindex/_stats?level=shards
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  index = "testindex",
  params = { "level": "shards" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 特定搜尋群組

下列範例會傳回 `group1` 與 `group2` 搜尋群組的搜尋統計資料：

<!-- spec_insert_start
component: example_code
rest: GET /_stats/search?groups=group1,group2
-->
{% capture step1_rest %}
GET /_stats/search?groups=group1,group2
{% endcapture %}

{% capture step1_python %}


response = client.indices.stats(
  metric = "search",
  params = { "groups": "group1,group2" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

根據預設，傳回的統計資料會分成兩組：`primaries` 和 `total`。`primaries` 群組僅包含針對主要分片計算的值，而 `total` 群組則包含主要分片與副本分片的累計值。以下是 Index Stats API 回應範例：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "docs": {
        "count": 4,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 5172,
        "reserved_in_bytes": 0
      },
      "indexing": {
        "index_total": 4,
        "index_time_in_millis": 1,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0,
        "max_last_index_request_timestamp": 1792186272652
      },
      "get": {
        "total": 2,
        "getTime": "0s",
        "time_in_millis": 0,
        "exists_total": 1,
        "exists_time_in_millis": 0,
        "missing_total": 1,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 3,
        "query_time_in_millis": 2,
        "query_current": 0,
        "query_failed": 0,
        "concurrent_query_total": 0,
        "concurrent_query_time_in_millis": 0,
        "concurrent_query_current": 0,
        "concurrent_avg_slice_count": 0.0,
        "startree_query_total": 0,
        "startree_query_time_in_millis": 0,
        "startree_query_current": 0,
        "startree_query_failed": 0,
        "fetch_total": 3,
        "fetch_time_in_millis": 0,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "point_in_time_total": 0,
        "point_in_time_time_in_millis": 0,
        "point_in_time_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0,
        "search_idle_reactivate_count_total": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 0,
        "total_time_in_millis": 0,
        "total_docs": 0,
        "total_size_in_bytes": 0,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 0,
        "total_auto_throttle_in_bytes": 20971520,
        "unreferenced_file_cleanups_performed": 0,
        "warmer": {
          "total_invocations_count": 0,
          "total_time_millis": 0,
          "total_failure_count": 0,
          "total_bytes_sent": 0,
          "total_bytes_received": 0,
          "total_send_time_millis": 0,
          "total_receive_time_millis": 0,
          "ongoing_count": 0
        }
      },
      "refresh": {
        "total": 3,
        "total_time_in_millis": 13,
        "external_total": 3,
        "external_total_time_in_millis": 13,
        "listeners": 0
      },
      "flush": {
        "total": 0,
        "periodic": 0,
        "total_time_in_millis": 0
      },
      "warmer": {
        "current": 0,
        "total": 2,
        "total_time_in_millis": 0
      },
      "query_cache": {
        "memory_size_in_bytes": 0,
        "total_count": 0,
        "hit_count": 0,
        "miss_count": 0,
        "cache_size": 0,
        "cache_count": 0,
        "evictions": 0
      },
      "fielddata": {
        "memory_size_in_bytes": 0,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 1,
        "memory_in_bytes": 0,
        "terms_memory_in_bytes": 0,
        "stored_fields_memory_in_bytes": 0,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 0,
        "points_memory_in_bytes": 0,
        "doc_values_memory_in_bytes": 0,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "remote_store": {
          "upload": {
            "total_upload_size": {
              "started_bytes": 0,
              "succeeded_bytes": 0,
              "failed_bytes": 0
            },
            "refresh_size_lag": {
              "total_bytes": 0,
              "max_bytes": 0
            },
            "max_refresh_time_lag_in_millis": 0,
            "total_time_spent_in_millis": 0,
            "pressure": {
              "total_rejections": 0
            }
          },
          "download": {
            "total_download_size": {
              "started_bytes": 0,
              "succeeded_bytes": 0,
              "failed_bytes": 0
            },
            "total_time_spent_in_millis": 0
          }
        },
        "segment_replication": {
          "max_bytes_behind": 0,
          "total_bytes_behind": 0,
          "max_replication_lag": 0
        },
        "file_sizes": {}
      },
      "translog": {
        "operations": 4,
        "size_in_bytes": 363,
        "uncommitted_operations": 4,
        "uncommitted_size_in_bytes": 363,
        "earliest_last_modified_age": 300,
        "remote_store": {
          "upload": {
            "total_uploads": {
              "started": 0,
              "failed": 0,
              "succeeded": 0
            },
            "total_upload_size": {
              "started_bytes": 0,
              "failed_bytes": 0,
              "succeeded_bytes": 0
            }
          }
        }
      },
      "request_cache": {
        "memory_size_in_bytes": 0,
        "evictions": 0,
        "hit_count": 0,
        "miss_count": 0
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    },
    "total": {
      "docs": {
        "count": 4,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 5172,
        "reserved_in_bytes": 0
      },
      "indexing": {
        "index_total": 4,
        "index_time_in_millis": 1,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0,
        "max_last_index_request_timestamp": 1792186272652
      },
      "get": {
        "total": 2,
        "getTime": "0s",
        "time_in_millis": 0,
        "exists_total": 1,
        "exists_time_in_millis": 0,
        "missing_total": 1,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 3,
        "query_time_in_millis": 2,
        "query_current": 0,
        "query_failed": 0,
        "concurrent_query_total": 0,
        "concurrent_query_time_in_millis": 0,
        "concurrent_query_current": 0,
        "concurrent_avg_slice_count": 0.0,
        "startree_query_total": 0,
        "startree_query_time_in_millis": 0,
        "startree_query_current": 0,
        "startree_query_failed": 0,
        "fetch_total": 3,
        "fetch_time_in_millis": 0,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "point_in_time_total": 0,
        "point_in_time_time_in_millis": 0,
        "point_in_time_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0,
        "search_idle_reactivate_count_total": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 0,
        "total_time_in_millis": 0,
        "total_docs": 0,
        "total_size_in_bytes": 0,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 0,
        "total_auto_throttle_in_bytes": 20971520,
        "unreferenced_file_cleanups_performed": 0,
        "warmer": {
          "total_invocations_count": 0,
          "total_time_millis": 0,
          "total_failure_count": 0,
          "total_bytes_sent": 0,
          "total_bytes_received": 0,
          "total_send_time_millis": 0,
          "total_receive_time_millis": 0,
          "ongoing_count": 0
        }
      },
      "refresh": {
        "total": 3,
        "total_time_in_millis": 13,
        "external_total": 3,
        "external_total_time_in_millis": 13,
        "listeners": 0
      },
      "flush": {
        "total": 0,
        "periodic": 0,
        "total_time_in_millis": 0
      },
      "warmer": {
        "current": 0,
        "total": 2,
        "total_time_in_millis": 0
      },
      "query_cache": {
        "memory_size_in_bytes": 0,
        "total_count": 0,
        "hit_count": 0,
        "miss_count": 0,
        "cache_size": 0,
        "cache_count": 0,
        "evictions": 0
      },
      "fielddata": {
        "memory_size_in_bytes": 0,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 1,
        "memory_in_bytes": 0,
        "terms_memory_in_bytes": 0,
        "stored_fields_memory_in_bytes": 0,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 0,
        "points_memory_in_bytes": 0,
        "doc_values_memory_in_bytes": 0,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "remote_store": {
          "upload": {
            "total_upload_size": {
              "started_bytes": 0,
              "succeeded_bytes": 0,
              "failed_bytes": 0
            },
            "refresh_size_lag": {
              "total_bytes": 0,
              "max_bytes": 0
            },
            "max_refresh_time_lag_in_millis": 0,
            "total_time_spent_in_millis": 0,
            "pressure": {
              "total_rejections": 0
            }
          },
          "download": {
            "total_download_size": {
              "started_bytes": 0,
              "succeeded_bytes": 0,
              "failed_bytes": 0
            },
            "total_time_spent_in_millis": 0
          }
        },
        "segment_replication": {
          "max_bytes_behind": 0,
          "total_bytes_behind": 0,
          "max_replication_lag": 0
        },
        "file_sizes": {}
      },
      "translog": {
        "operations": 4,
        "size_in_bytes": 363,
        "uncommitted_operations": 4,
        "uncommitted_size_in_bytes": 363,
        "earliest_last_modified_age": 300,
        "remote_store": {
          "upload": {
            "total_uploads": {
              "started": 0,
              "failed": 0,
              "succeeded": 0
            },
            "total_upload_size": {
              "started_bytes": 0,
              "failed_bytes": 0,
              "succeeded_bytes": 0
            }
          }
        }
      },
      "request_cache": {
        "memory_size_in_bytes": 0,
        "evictions": 0,
        "hit_count": 0,
        "miss_count": 0
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    }
  },
  "indices": {
    "testindex": {
      "uuid": "fnaTkGq4QIqB__mdUzGqiw",
      "primaries": {
        "docs": {
          "count": 4,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 5172,
          "reserved_in_bytes": 0
        },
        "indexing": {
          "index_total": 4,
          "index_time_in_millis": 1,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0,
          "max_last_index_request_timestamp": 1792186272652
        },
        "get": {
          "total": 2,
          "getTime": "0s",
          "time_in_millis": 0,
          "exists_total": 1,
          "exists_time_in_millis": 0,
          "missing_total": 1,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 3,
          "query_time_in_millis": 2,
          "query_current": 0,
          "query_failed": 0,
          "concurrent_query_total": 0,
          "concurrent_query_time_in_millis": 0,
          "concurrent_query_current": 0,
          "concurrent_avg_slice_count": 0.0,
          "startree_query_total": 0,
          "startree_query_time_in_millis": 0,
          "startree_query_current": 0,
          "startree_query_failed": 0,
          "fetch_total": 3,
          "fetch_time_in_millis": 0,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "point_in_time_total": 0,
          "point_in_time_time_in_millis": 0,
          "point_in_time_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0,
          "search_idle_reactivate_count_total": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 0,
          "total_time_in_millis": 0,
          "total_docs": 0,
          "total_size_in_bytes": 0,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 0,
          "total_auto_throttle_in_bytes": 20971520,
          "unreferenced_file_cleanups_performed": 0,
          "warmer": {
            "total_invocations_count": 0,
            "total_time_millis": 0,
            "total_failure_count": 0,
            "total_bytes_sent": 0,
            "total_bytes_received": 0,
            "total_send_time_millis": 0,
            "total_receive_time_millis": 0,
            "ongoing_count": 0
          }
        },
        "refresh": {
          "total": 3,
          "total_time_in_millis": 13,
          "external_total": 3,
          "external_total_time_in_millis": 13,
          "listeners": 0
        },
        "flush": {
          "total": 0,
          "periodic": 0,
          "total_time_in_millis": 0
        },
        "warmer": {
          "current": 0,
          "total": 2,
          "total_time_in_millis": 0
        },
        "query_cache": {
          "memory_size_in_bytes": 0,
          "total_count": 0,
          "hit_count": 0,
          "miss_count": 0,
          "cache_size": 0,
          "cache_count": 0,
          "evictions": 0
        },
        "fielddata": {
          "memory_size_in_bytes": 0,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 1,
          "memory_in_bytes": 0,
          "terms_memory_in_bytes": 0,
          "stored_fields_memory_in_bytes": 0,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 0,
          "points_memory_in_bytes": 0,
          "doc_values_memory_in_bytes": 0,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "remote_store": {
            "upload": {
              "total_upload_size": {
                "started_bytes": 0,
                "succeeded_bytes": 0,
                "failed_bytes": 0
              },
              "refresh_size_lag": {
                "total_bytes": 0,
                "max_bytes": 0
              },
              "max_refresh_time_lag_in_millis": 0,
              "total_time_spent_in_millis": 0,
              "pressure": {
                "total_rejections": 0
              }
            },
            "download": {
              "total_download_size": {
                "started_bytes": 0,
                "succeeded_bytes": 0,
                "failed_bytes": 0
              },
              "total_time_spent_in_millis": 0
            }
          },
          "segment_replication": {
            "max_bytes_behind": 0,
            "total_bytes_behind": 0,
            "max_replication_lag": 0
          },
          "file_sizes": {}
        },
        "translog": {
          "operations": 4,
          "size_in_bytes": 363,
          "uncommitted_operations": 4,
          "uncommitted_size_in_bytes": 363,
          "earliest_last_modified_age": 300,
          "remote_store": {
            "upload": {
              "total_uploads": {
                "started": 0,
                "failed": 0,
                "succeeded": 0
              },
              "total_upload_size": {
                "started_bytes": 0,
                "failed_bytes": 0,
                "succeeded_bytes": 0
              }
            }
          }
        },
        "request_cache": {
          "memory_size_in_bytes": 0,
          "evictions": 0,
          "hit_count": 0,
          "miss_count": 0
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      },
      "total": {
        "docs": {
          "count": 4,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 5172,
          "reserved_in_bytes": 0
        },
        "indexing": {
          "index_total": 4,
          "index_time_in_millis": 1,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0,
          "max_last_index_request_timestamp": 1792186272652
        },
        "get": {
          "total": 2,
          "getTime": "0s",
          "time_in_millis": 0,
          "exists_total": 1,
          "exists_time_in_millis": 0,
          "missing_total": 1,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 3,
          "query_time_in_millis": 2,
          "query_current": 0,
          "query_failed": 0,
          "concurrent_query_total": 0,
          "concurrent_query_time_in_millis": 0,
          "concurrent_query_current": 0,
          "concurrent_avg_slice_count": 0.0,
          "startree_query_total": 0,
          "startree_query_time_in_millis": 0,
          "startree_query_current": 0,
          "startree_query_failed": 0,
          "fetch_total": 3,
          "fetch_time_in_millis": 0,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "point_in_time_total": 0,
          "point_in_time_time_in_millis": 0,
          "point_in_time_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0,
          "search_idle_reactivate_count_total": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 0,
          "total_time_in_millis": 0,
          "total_docs": 0,
          "total_size_in_bytes": 0,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 0,
          "total_auto_throttle_in_bytes": 20971520,
          "unreferenced_file_cleanups_performed": 0,
          "warmer": {
            "total_invocations_count": 0,
            "total_time_millis": 0,
            "total_failure_count": 0,
            "total_bytes_sent": 0,
            "total_bytes_received": 0,
            "total_send_time_millis": 0,
            "total_receive_time_millis": 0,
            "ongoing_count": 0
          }
        },
        "refresh": {
          "total": 3,
          "total_time_in_millis": 13,
          "external_total": 3,
          "external_total_time_in_millis": 13,
          "listeners": 0
        },
        "flush": {
          "total": 0,
          "periodic": 0,
          "total_time_in_millis": 0
        },
        "warmer": {
          "current": 0,
          "total": 2,
          "total_time_in_millis": 0
        },
        "query_cache": {
          "memory_size_in_bytes": 0,
          "total_count": 0,
          "hit_count": 0,
          "miss_count": 0,
          "cache_size": 0,
          "cache_count": 0,
          "evictions": 0
        },
        "fielddata": {
          "memory_size_in_bytes": 0,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 1,
          "memory_in_bytes": 0,
          "terms_memory_in_bytes": 0,
          "stored_fields_memory_in_bytes": 0,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 0,
          "points_memory_in_bytes": 0,
          "doc_values_memory_in_bytes": 0,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "remote_store": {
            "upload": {
              "total_upload_size": {
                "started_bytes": 0,
                "succeeded_bytes": 0,
                "failed_bytes": 0
              },
              "refresh_size_lag": {
                "total_bytes": 0,
                "max_bytes": 0
              },
              "max_refresh_time_lag_in_millis": 0,
              "total_time_spent_in_millis": 0,
              "pressure": {
                "total_rejections": 0
              }
            },
            "download": {
              "total_download_size": {
                "started_bytes": 0,
                "succeeded_bytes": 0,
                "failed_bytes": 0
              },
              "total_time_spent_in_millis": 0
            }
          },
          "segment_replication": {
            "max_bytes_behind": 0,
            "total_bytes_behind": 0,
            "max_replication_lag": 0
          },
          "file_sizes": {}
        },
        "translog": {
          "operations": 4,
          "size_in_bytes": 363,
          "uncommitted_operations": 4,
          "uncommitted_size_in_bytes": 363,
          "earliest_last_modified_age": 300,
          "remote_store": {
            "upload": {
              "total_uploads": {
                "started": 0,
                "failed": 0,
                "succeeded": 0
              },
              "total_upload_size": {
                "started_bytes": 0,
                "failed_bytes": 0,
                "succeeded_bytes": 0
              }
            }
          }
        },
        "request_cache": {
          "memory_size_in_bytes": 0,
          "evictions": 0,
          "hit_count": 0,
          "miss_count": 0
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      }
    }
  }
}
```
</details>

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_shards` | 物件 | 包含此請求的 `total`、`successful` 和 `failed` 分片數。 |
| `_all` | 物件 | 彙總所有符合請求之索引的統計資料。 |
| `indices` | 物件 | 每個符合請求之索引的統計資料，以索引名稱作為鍵。若 `level` 為 `cluster`，則不會傳回。 |

`_all` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `primaries` | 物件 | 僅針對主要分片計算的統計資料。 |
| `total` | 物件 | 跨主要分片與副本分片累計的統計資料。 |

`indices` 中的每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `uuid` | 字串 | 索引的通用唯一識別碼 (UUID)。 |
| `primaries` | 物件 | 僅針對主要分片計算的索引統計資料。 |
| `total` | 物件 | 跨主要分片與副本分片累計的索引統計資料。 |
| `shards` | 物件 | 索引中每個分片的統計資料，以分片編號作為鍵。每個鍵包含一個分片複本物件陣列。僅在 `level` 為 `shards` 時傳回。 |

`shards` 中的每個分片複本物件包含該分片複本的統計資料群組，以及下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `routing` | 物件 | 分片複本的路由資訊。 |
| `commit` | 物件 | 分片複本最近一次 Lucene 提交 (commit) 的相關資訊。 |
| `seq_no` | 物件 | 分片複本的序號資訊。 |
| `retention_leases` | 物件 | 分片複本的保留租約 (retention lease)。 |
| `shard_path` | 物件 | 分片複本的檔案系統路徑。 |

`routing` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `state` | 字串 | 分片複本的狀態，例如 `STARTED` 或 `RELOCATING`。 |
| `primary` | 布林值 | 分片複本是否為主要分片。 |
| `node` | 字串 | 存放此分片複本之節點的 ID。 |
| `relocating_node` | 字串 | 分片複本正在重新配置前往之節點的 ID；若分片複本未在重新配置，則為 `null`。 |

`commit` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `id` | 字串 | 提交的 ID。 |
| `generation` | 整數 | 提交的世代編號。 |
| `user_data` | 物件 | 與提交一起儲存的中繼資料，例如 translog UUID 以及提交當時的本機檢查點。 |
| `num_docs` | 整數 | 提交中的文件數。 |

`seq_no` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `max_seq_no` | 整數 | 為分片複本核發的最高序號。 |
| `local_checkpoint` | 整數 | 分片複本已處理完所有作業的最高序號。 |
| `global_checkpoint` | 整數 | 所有作用中分片複本皆已處理的最高序號。 |

`retention_leases` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `primary_term` | 整數 | 分片的主要分片任期。 |
| `version` | 整數 | 保留租約集合的版本。 |
| `leases` | 物件陣列 | 保留租約。每個租約包含 `id`、`retaining_seq_no`、`timestamp` 和 `source` 欄位。 |

`shard_path` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `state_path` | 字串 | 儲存分片狀態之節點資料目錄的路徑。 |
| `data_path` | 字串 | 儲存分片資料之節點資料目錄的路徑。 |
| `is_custom_data_path` | 布林值 | 索引是否使用自訂資料路徑。 |

如需各統計資料群組（例如 `docs`、`indexing` 和 `search`）中欄位的相關資訊，請參閱 [Nodes Stats API 回應欄位]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/#indices)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:monitor/stats`。
