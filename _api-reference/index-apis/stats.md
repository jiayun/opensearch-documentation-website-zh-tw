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
`_all` | 傳回所有統計資訊。 
`completion` | 完成建議器的統計資訊。 
`docs` | 傳回文件數目，以及尚未合併的已刪除文件數目。索引重新整理作業可能會影響此統計資訊。 
`fielddata` | Field data 統計資訊。 
`flush` | 排清統計資訊。 
`get` | 取得作業的統計資訊，包括找不到文件時的統計資訊。 
`indexing` | 索引編製統計資訊。 
`merge` | 合併統計資訊。 
`query_cache` | 查詢快取統計資訊。 
`refresh` | 重新整理統計資訊。 
`request_cache` | 分片請求快取統計資訊。 
`search` | 搜尋統計資訊，包括建議作業的統計資訊。搜尋作業可與一個或多個群組相關聯。您可以提供 `groups` 參數來包含自訂群組的統計資訊，該參數接受以逗號分隔的群組名稱清單。若要傳回所有群組的統計資訊，請使用 `_all`。 
`segments` | 所有開啟分段的記憶體使用統計資訊。若 `include_segment_file_sizes` 參數為 `true`，此指標會包含每個 Lucene 索引檔案的彙總磁碟用量。
`store` | 以位元組為單位的索引大小。 
`translog` | Translog 統計資訊。 
`warmer` | Warmer 統計資訊。 

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：展開至所有開啟與關閉的索引，包括隱藏索引。<br> - `open`：展開至開啟的索引。<br> - `closed`：展開至關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。
`fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要包含在統計資訊中的欄位。若未提供 `completion_fields` 與 `fielddata_fields`，則指定預設欄位清單。
`completion_fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要包含在欄位層級 `completion` 統計資訊中的欄位。
`fielddata_fields` | 字串 | 以逗號分隔的清單或萬用字元運算式，指定要包含在欄位層級 `fielddata` 統計資訊中的欄位。
`forbid_closed_indices` | 布林值 | 指定不收集已關閉索引的統計資訊。預設為 `true`。
`groups` | 字串 | 以逗號分隔的搜尋群組清單，用於包含在 `search` 統計資訊中。搜尋群組是透過 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#search-stats-groups) 的 `stats` 參數指派給搜尋請求的自訂標籤。使用 `_all` 可傳回所有群組的統計資訊。
`level` | 字串 | 指定用於彙總統計資訊的層級。有效值為：<br> - `cluster`：叢集層級統計資訊。<br> - `indices`：索引層級統計資訊。<br> - `shards`：分片層級統計資訊。<br> 預設為 `indices`。
`include_segment_file_sizes` | 布林值 | 指定是否回報每個 Lucene 索引檔案的彙總磁碟用量。僅適用於 `segments` 統計資訊。預設為 `false`。
`include_unloaded_segments` | 布林值 | 指定是否包含未載入記憶體之分段的資訊。預設為 `false`。

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

### 特定統計資訊

以下範例傳回與索引及排清作業相關的索引統計資訊：

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

以下範例展開所有與索引統計資訊相關的萬用字元：

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

## 範例回應

根據預設，傳回的統計資料會分成兩個群組：`primaries` 與 `total`。`primaries` 群組包含僅針對主要分片計算的值，而 `total` 群組則包含主要分片與副本分片累計的值。以下是 Index Stats API 回應的範例：

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
        "size_in_bytes": 15531,
        "reserved_in_bytes": 0
      },
      "indexing": {
        "index_total": 4,
        "index_time_in_millis": 10,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 12,
        "query_time_in_millis": 11,
        "query_current": 0,
        "fetch_total": 12,
        "fetch_time_in_millis": 5,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "point_in_time_total": 0,
        "point_in_time_time_in_millis": 0,
        "point_in_time_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
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
        "total_auto_throttle_in_bytes": 20971520
      },
      "refresh": {
        "total": 8,
        "total_time_in_millis": 58,
        "external_total": 7,
        "external_total_time_in_millis": 60,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "periodic": 1,
        "total_time_in_millis": 21
      },
      "warmer": {
        "current": 0,
        "total": 6,
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
        "evictions": 0,
        "item_count": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 4,
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
        "remote_store" : {
          "upload" : {
            "total_upload_size" : {
              "started_bytes" : 152419,
              "succeeded_bytes" : 152419,
              "failed_bytes" : 0
            },
            "refresh_size_lag" : {
              "total_bytes" : 0,
              "max_bytes" : 0
            },
            "max_refresh_time_lag_in_millis" : 0,
            "total_time_spent_in_millis" : 516,
            "pressure" : {
              "total_rejections" : 0
            }
          },
          "download" : {
            "total_download_size" : {
              "started_bytes" : 0,
              "succeeded_bytes" : 0,
              "failed_bytes" : 0
            },
            "total_time_spent_in_millis" : 0
          }
        },
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 55,
        "uncommitted_operations": 0,
        "uncommitted_size_in_bytes": 55,
        "earliest_last_modified_age": 142622215,
        "remote_store" : {
          "upload" : {
            "total_uploads" : {
              "started" : 57,
              "failed" : 0,
              "succeeded" : 57
            },
            "total_upload_size" : {
              "started_bytes" : 16830,
              "failed_bytes" : 0,
              "succeeded_bytes" : 16830
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
        "size_in_bytes": 15531,
        "reserved_in_bytes": 0
      },
      "indexing": {
        "index_total": 4,
        "index_time_in_millis": 10,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 12,
        "query_time_in_millis": 11,
        "query_current": 0,
        "fetch_total": 12,
        "fetch_time_in_millis": 5,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "point_in_time_total": 0,
        "point_in_time_time_in_millis": 0,
        "point_in_time_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
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
        "total_auto_throttle_in_bytes": 20971520
      },
      "refresh": {
        "total": 8,
        "total_time_in_millis": 58,
        "external_total": 7,
        "external_total_time_in_millis": 60,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "periodic": 1,
        "total_time_in_millis": 21
      },
      "warmer": {
        "current": 0,
        "total": 6,
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
        "evictions": 0,
        "item_count": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 4,
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
        "remote_store" : {
          "upload" : {
            "total_upload_size" : {
              "started_bytes" : 152419,
              "succeeded_bytes" : 152419,
              "failed_bytes" : 0
            },
            "refresh_size_lag" : {
              "total_bytes" : 0,
              "max_bytes" : 0
            },
            "max_refresh_time_lag_in_millis" : 0,
            "total_time_spent_in_millis" : 516,
            "pressure" : {
              "total_rejections" : 0
            }
          },
          "download" : {
            "total_download_size" : {
              "started_bytes" : 0,
              "succeeded_bytes" : 0,
              "failed_bytes" : 0
            },
            "total_time_spent_in_millis" : 0
          }
        },
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 55,
        "uncommitted_operations": 0,
        "uncommitted_size_in_bytes": 55,
        "earliest_last_modified_age": 142622215,
        "remote_store" : {
          "upload" : {
            "total_uploads" : {
              "started" : 57,
              "failed" : 0,
              "succeeded" : 57
            },
            "total_upload_size" : {
              "started_bytes" : 16830,
              "failed_bytes" : 0,
              "succeeded_bytes" : 16830
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
      "uuid": "0SXXSpe9Rp-FpxXXWLOD8Q",
      "primaries": {
        "docs": {
          "count": 4,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 15531,
          "reserved_in_bytes": 0
        },
        "indexing": {
          "index_total": 4,
          "index_time_in_millis": 10,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 12,
          "query_time_in_millis": 11,
          "query_current": 0,
          "fetch_total": 12,
          "fetch_time_in_millis": 5,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "point_in_time_total": 0,
          "point_in_time_time_in_millis": 0,
          "point_in_time_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
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
          "total_auto_throttle_in_bytes": 20971520
        },
        "refresh": {
          "total": 8,
          "total_time_in_millis": 58,
          "external_total": 7,
          "external_total_time_in_millis": 60,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "periodic": 1,
          "total_time_in_millis": 21
        },
        "warmer": {
          "current": 0,
          "total": 6,
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
          "evictions": 0,
          "item_count": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 4,
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
          "remote_store" : {
            "upload" : {
              "total_upload_size" : {
                "started_bytes" : 152419,
                "succeeded_bytes" : 152419,
                "failed_bytes" : 0
              },
              "refresh_size_lag" : {
                "total_bytes" : 0,
                "max_bytes" : 0
              },
              "max_refresh_time_lag_in_millis" : 0,
              "total_time_spent_in_millis" : 516,
              "pressure" : {
                "total_rejections" : 0
              }
            },
            "download" : {
              "total_download_size" : {
                "started_bytes" : 0,
                "succeeded_bytes" : 0,
                "failed_bytes" : 0
              },
              "total_time_spent_in_millis" : 0
            }
          },
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 55,
          "uncommitted_operations": 0,
          "uncommitted_size_in_bytes": 55,
          "earliest_last_modified_age": 142622215,
          "remote_store" : {
            "upload" : {
              "total_uploads" : {
                "started" : 57,
                "failed" : 0,
                "succeeded" : 57
              },
              "total_upload_size" : {
                "started_bytes" : 16830,
                "failed_bytes" : 0,
                "succeeded_bytes" : 16830
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
          "size_in_bytes": 15531,
          "reserved_in_bytes": 0
        },
        "indexing": {
          "index_total": 4,
          "index_time_in_millis": 10,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 12,
          "query_time_in_millis": 11,
          "query_current": 0,
          "fetch_total": 12,
          "fetch_time_in_millis": 5,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "point_in_time_total": 0,
          "point_in_time_time_in_millis": 0,
          "point_in_time_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
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
          "total_auto_throttle_in_bytes": 20971520
        },
        "refresh": {
          "total": 8,
          "total_time_in_millis": 58,
          "external_total": 7,
          "external_total_time_in_millis": 60,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "periodic": 1,
          "total_time_in_millis": 21
        },
        "warmer": {
          "current": 0,
          "total": 6,
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
          "evictions": 0,
          "item_count": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 4,
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
          "remote_store" : {
            "upload" : {
              "total_upload_size" : {
                "started_bytes" : 152419,
                "succeeded_bytes" : 152419,
                "failed_bytes" : 0
              },
              "refresh_size_lag" : {
                "total_bytes" : 0,
                "max_bytes" : 0
              },
              "max_refresh_time_lag_in_millis" : 0,
              "total_time_spent_in_millis" : 516,
              "pressure" : {
                "total_rejections" : 0
              }
            },
            "download" : {
              "total_download_size" : {
                "started_bytes" : 0,
                "succeeded_bytes" : 0,
                "failed_bytes" : 0
              },
              "total_time_spent_in_millis" : 0
            }
          },
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 55,
          "uncommitted_operations": 0,
          "uncommitted_size_in_bytes": 55,
          "earliest_last_modified_age": 142622215,
          "remote_store" : {
            "upload" : {
              "total_uploads" : {
                "started" : 57,
                "failed" : 0,
                "succeeded" : 57
              },
              "total_upload_size" : {
                "started_bytes" : 16830,
                "failed_bytes" : 0,
                "succeeded_bytes" : 16830
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

如需回應欄位的相關資訊，請參閱 [Nodes Stats API 回應欄位]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/#indices)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:monitor/stats`。
