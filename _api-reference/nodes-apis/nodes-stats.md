---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Nodes stats
parent: Nodes APIs
nav_order: 20
---

# Nodes Stats API
**於 1.0 版導入**
{: .label .label-purple }

Nodes Stats API 會傳回叢集的統計資訊。

## 端點

```json
GET /_nodes/stats
GET /_nodes/{node_id}/stats
GET /_nodes/stats/{metric}
GET /_nodes/{node_id}/stats/{metric}
GET /_nodes/stats/{metric}/{index_metric}
GET /_nodes/{node_id}/stats/{metric}/{index_metric}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`node_id` | 字串 | 以逗號分隔的節點 ID 清單，用於篩選結果。支援[節點篩選器]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。預設為 `_all`。
`metric` | 字串 | 以逗號分隔、要包含在回應中的指標群組清單。例如 `jvm,fs`。請參閱下列所有索引指標的清單。預設為所有指標。
`index_metric` | 字串 | 以逗號分隔、要包含在回應中的索引指標群組清單。例如 `docs,store`。請參閱下列所有索引指標的清單。預設為所有索引指標。

下表列出所有可用的指標群組。

指標 | 說明
:--- |:----
`indices` | 索引統計資訊，例如大小、文件數量，以及文件的搜尋、編製索引與刪除時間。
`os` | 主機作業系統的統計資訊，包括負載、記憶體與交換。
`process` | 程序的統計資訊，包括記憶體消耗、開啟的檔案描述符與 CPU 使用率。
`jvm` | JVM 的統計資訊，包括記憶體集區、緩衝集區、垃圾回收，以及已載入的類別數量。
`thread_pool` | 節點每個執行緒集區的統計資訊。
`fs` | 檔案系統統計資訊，例如讀取/寫入統計、資料路徑與可用磁碟空間。
`transport` | 叢集通訊中傳送/接收的傳輸層統計資訊。
`http` | HTTP 層的統計資訊。
`breaker` | 欄位資料斷路器的統計資訊。
`script` | 指令碼的統計資訊，例如編譯與快取驅逐。
`discovery` | 叢集狀態的統計資訊。
`ingest` | 資料匯入管線的統計資訊。
`adaptive_selection` | 自適應副本選擇的統計資訊，其使用分片配置感知來選取合適的節點。
`script_cache` | 指令碼快取的統計資訊。
`indexing_pressure` | 節點索引壓力的統計資訊。
`shard_indexing_pressure` | 分片索引壓力的統計資訊。
`search_backpressure` | 與搜尋回壓相關的統計資訊。
`cluster_manager_throttling` | 與叢集管理員節點上被節流任務相關的統計資訊。
`task_cancellation` | 取消後仍繼續執行之任務的統計資訊。
`weighted_routing` | 與加權輪詢請求相關的統計資訊。
`resource_usage_stats` | 節點層級的資源使用統計資訊，例如 CPU 與 JVM 記憶體。
`admission_control` | 准入控制的統計資訊。
`concurrency_limiter` | 自適應並行限制器的統計資訊。
`caches` | 快取的統計資訊。

若要篩選 `indices` 指標傳回的資訊，您可以使用特定的 `index_metric` 值。這些值只能在您使用下列查詢類型時使用：

```json
GET _nodes/stats/
GET _nodes/stats/_all
GET _nodes/stats/indices
```

支援下列索引指標：

- `docs`
- `store`
- `indexing`
- `get`
- `search`
- `merge`
- `refresh`
- `flush`
- `warmer`
- `query_cache`
- `fielddata`
- `completion`
- `segments`
- `translog`
- `request_cache`

例如，下列查詢會請求 `docs` 與 `search` 的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/stats/indices/docs,search
-->
{% capture step1_rest %}
GET /_nodes/stats/indices/docs,search
{% endcapture %}

{% capture step1_python %}


response = client.nodes.stats(
  metric = "indices",
  index_metric = "docs,search"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您也可以在 `caches` 指標中使用特定的 `index_metric` 值，指定要傳回哪些快取的統計資訊。
支援下列索引指標：

- request_cache

例如，下列查詢會請求 `request_cache` 的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/stats/caches/request_cache
-->
{% capture step1_rest %}
GET /_nodes/stats/caches/request_cache
{% endcapture %}

{% capture step1_python %}


response = client.nodes.stats(
  metric = "caches",
  index_metric = "request_cache"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`completion_fields` | 字串 | 要包含在完成統計中的欄位。支援以逗號分隔的清單與萬用字元運算式。
`fielddata_fields` | 字串 | 要包含在 `fielddata` 統計中的欄位。支援以逗號分隔的清單與萬用字元運算式。
`fields` | 字串 | 要包含的欄位。支援以逗號分隔的清單與萬用字元運算式。
`groups` | 字串 | 以逗號分隔、要包含在搜尋統計中的搜尋群組清單。
`level` | 字串 | 指定 `indices` 指標的統計資訊要在叢集、索引或分片層級彙總。有效值為 `indices`、`node` 與 `shard`。用於 `caches` 指標時，`indices`、`shard` 與 `tier` 為有效值。若未使用[分層溢出快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/tiered-cache/)，`tier` 值會被忽略。
`timeout` | 時間 | 設定節點回應的時間限制。預設為 `30s`。
`include_segment_file_sizes` | 布林值 | 若請求分段統計資訊，此欄位指定要傳回每個 Lucene 索引檔案的彙總磁碟使用量。預設為 `false`。

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/stats
-->
{% capture step1_rest %}
GET /_nodes/stats
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  node_id_or_metric = "stats"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

選取箭頭以檢視範例回應。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "docker-cluster",
  "nodes" : {
    "F-ByTQzVQ3GQeYzQJArJGQ" : {
      "timestamp" : 1664484195257,
      "name" : "opensearch",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1:9300",
      "roles" : [
        "cluster_manager",
        "data",
        "ingest",
        "remote_cluster_client"
      ],
      "attributes" : {
        "shard_indexing_pressure_enabled" : "true"
      },
      "indices" : {
        "docs" : {
          "count" : 13160,
          "deleted" : 12
        },
        "store" : {
          "size_in_bytes" : 6263461,
          "reserved_in_bytes" : 0
        },
        "indexing" : {
          "index_total" : 0,
          "index_time_in_millis" : 0,
          "index_current" : 0,
          "index_failed" : 0,
          "delete_total" : 204,
          "delete_time_in_millis" : 427,
          "delete_current" : 0,
          "noop_update_total" : 0,
          "is_throttled" : false,
          "throttle_time_in_millis" : 0
        },
        "get" : {
          "total" : 4,
          "time_in_millis" : 18,
          "exists_total" : 4,
          "exists_time_in_millis" : 18,
          "missing_total" : 0,
          "missing_time_in_millis" : 0,
          "current" : 0
        },
        "search" : {
          "open_contexts": 4,
          "query_total": 194,
          "query_time_in_millis": 467,
          "query_current": 0,
          "fetch_total": 194,
          "fetch_time_in_millis": 143,
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
          "search_idle_reactivate_count_total": 0,
          "request" : {
            "dfs_pre_query" : {
              "time_in_millis" : 0,
              "current" : 0,
              "total" : 0
            },
            "query" : {
              "time_in_millis" : 200,
              "current" : 2,
              "total" : 12
            },
            "fetch" : {
              "time_in_millis" : 37,
              "current" : 3,
              "total" : 4
            },
            "dfs_query" : {
              "time_in_millis" : 0,
              "current" : 0,
              "total" : 0
            },
            "expand" : {
              "time_in_millis" : 9,
              "current" : 1,
              "total" : 0
            },
            "can_match" : {
              "time_in_millis" : 0,
              "current" : 0,
              "total" : 0
            }
          }
        },
        "merges" : {
          "current" : 0,
          "current_docs" : 0,
          "current_size_in_bytes" : 0,
          "total" : 1,
          "total_time_in_millis" : 5,
          "total_docs" : 12,
          "total_size_in_bytes" : 3967,
          "total_stopped_time_in_millis" : 0,
          "total_throttled_time_in_millis" : 0,
          "total_auto_throttle_in_bytes" : 251658240
        },
        "refresh" : {
          "total" : 74,
          "total_time_in_millis" : 201,
          "external_total" : 57,
          "external_total_time_in_millis" : 314,
          "listeners" : 0
        },
        "flush" : {
          "total" : 28,
          "periodic" : 28,
          "total_time_in_millis" : 1261
        },
        "warmer" : {
          "current" : 0,
          "total" : 45,
          "total_time_in_millis" : 99
        },
        "query_cache" : {
          "memory_size_in_bytes" : 0,
          "total_count" : 0,
          "hit_count" : 0,
          "miss_count" : 0,
          "cache_size" : 0,
          "cache_count" : 0,
          "evictions" : 0
        },
        "fielddata" : {
          "memory_size_in_bytes" : 356,
          "evictions" : 0,
          "item_count": 1
        },
        "completion" : {
          "size_in_bytes" : 0,
          "fields" : { }
        },
        "segments" : {
          "count" : 17,
          "memory_in_bytes" : 0,
          "terms_memory_in_bytes" : 0,
          "stored_fields_memory_in_bytes" : 0,
          "term_vectors_memory_in_bytes" : 0,
          "norms_memory_in_bytes" : 0,
          "points_memory_in_bytes" : 0,
          "doc_values_memory_in_bytes" : 0,
          "index_writer_memory_in_bytes" : 0,
          "version_map_memory_in_bytes" : 0,
          "fixed_bit_set_memory_in_bytes" : 288,
          "max_unsafe_auto_id_timestamp" : -1,
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
          "file_sizes" : { }
        },
        "translog" : {
          "operations" : 12,
          "size_in_bytes" : 1452,
          "uncommitted_operations" : 12,
          "uncommitted_size_in_bytes" : 1452,
          "earliest_last_modified_age" : 164160,
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
        "request_cache" : {
          "memory_size_in_bytes" : 1649,
          "evictions" : 0,
          "hit_count" : 0,
          "miss_count" : 18
        },
        "recovery" : {
          "current_as_source" : 0,
          "current_as_target" : 0,
          "throttle_time_in_millis" : 0
        }
      },
      "os" : {
        "timestamp" : 1664484195263,
        "cpu" : {
          "percent" : 0,
          "load_average" : {
            "1m" : 0.0,
            "5m" : 0.0,
            "15m" : 0.0
          }
        },
        "mem" : {
          "total_in_bytes" : 13137076224,
          "free_in_bytes" : 9265442816,
          "used_in_bytes" : 3871633408,
          "free_percent" : 71,
          "used_percent" : 29
        },
        "swap" : {
          "total_in_bytes" : 4294967296,
          "free_in_bytes" : 4294967296,
          "used_in_bytes" : 0
        },
        "cgroup" : {
          "cpuacct" : {
            "control_group" : "/",
            "usage_nanos" : 338710071600
          },
          "cpu" : {
            "control_group" : "/",
            "cfs_period_micros" : 100000,
            "cfs_quota_micros" : -1,
            "stat" : {
              "number_of_elapsed_periods" : 0,
              "number_of_times_throttled" : 0,
              "time_throttled_nanos" : 0
            }
          },
          "memory" : {
            "control_group" : "/",
            "limit_in_bytes" : "9223372036854771712",
            "usage_in_bytes" : "1432346624"
          }
        }
      },
      "process" : {
        "timestamp" : 1664484195263,
        "open_file_descriptors" : 556,
        "max_file_descriptors" : 65536,
        "cpu" : {
          "percent" : 0,
          "total_in_millis" : 170870
        },
        "mem" : {
          "total_virtual_in_bytes" : 6563344384
        }
      },
      "jvm" : {
        "timestamp" : 1664484195264,
        "uptime_in_millis" : 21232111,
        "mem" : {
          "heap_used_in_bytes" : 308650480,
          "heap_used_percent" : 57,
          "heap_committed_in_bytes" : 536870912,
          "heap_max_in_bytes" : 536870912,
          "non_heap_used_in_bytes" : 147657128,
          "non_heap_committed_in_bytes" : 152502272,
          "pools" : {
            "young" : {
              "used_in_bytes" : 223346688,
              "max_in_bytes" : 0,
              "peak_used_in_bytes" : 318767104,
              "peak_max_in_bytes" : 0,
              "last_gc_stats" : {
                "used_in_bytes" : 0,
                "max_in_bytes" : 0,
                "usage_percent" : -1
              }
            },
            "old" : {
              "used_in_bytes" : 67068928,
              "max_in_bytes" : 536870912,
              "peak_used_in_bytes" : 67068928,
              "peak_max_in_bytes" : 536870912,
              "last_gc_stats" : {
                "used_in_bytes" : 34655744,
                "max_in_bytes" : 536870912,
                "usage_percent" : 6
              }
            },
            "survivor" : {
              "used_in_bytes" : 18234864,
              "max_in_bytes" : 0,
              "peak_used_in_bytes" : 32721280,
              "peak_max_in_bytes" : 0,
              "last_gc_stats" : {
                "used_in_bytes" : 18234864,
                "max_in_bytes" : 0,
                "usage_percent" : -1
              }
            }
          }
        },
        "threads" : {
          "count" : 80,
          "peak_count" : 80
        },
        "gc" : {
          "collectors" : {
            "young" : {
              "collection_count" : 18,
              "collection_time_in_millis" : 199
            },
            "old" : {
              "collection_count" : 0,
              "collection_time_in_millis" : 0
            }
          }
        },
        "buffer_pools" : {
          "mapped" : {
            "count" : 23,
            "used_in_bytes" : 6232113,
            "total_capacity_in_bytes" : 6232113
          },
          "direct" : {
            "count" : 63,
            "used_in_bytes" : 9050069,
            "total_capacity_in_bytes" : 9050068
          },
          "mapped - 'non-volatile memory'" : {
            "count" : 0,
            "used_in_bytes" : 0,
            "total_capacity_in_bytes" : 0
          }
        },
        "classes" : {
          "current_loaded_count" : 20693,
          "total_loaded_count" : 20693,
          "total_unloaded_count" : 0
        }
      },
      "thread_pool" : {
        "OPENSEARCH_ML_TASK_THREAD_POOL" : {
          "threads" : 0,
          "queue" : 0,
          "active" : 0,
          "rejected" : 0,
          "largest" : 0,
          "completed" : 0
        },
        "ad-batch-task-threadpool" : {
          "threads" : 0,
          "queue" : 0,
          "active" : 0,
          "rejected" : 0,
          "largest" : 0,
          "completed" : 0
        },
        ...
      },
      "fs" : {
        "timestamp" : 1664484195264,
        "total" : {
          "total_in_bytes" : 269490393088,
          "free_in_bytes" : 261251477504,
          "available_in_bytes" : 247490805760
        },
        "data" : [
          {
            "path" : "/usr/share/opensearch/data/nodes/0",
            "mount" : "/ (overlay)",
            "type" : "overlay",
            "total_in_bytes" : 269490393088,
            "free_in_bytes" : 261251477504,
            "available_in_bytes" : 247490805760
          }
        ],
        "io_stats" : { }
      },
      "transport" : {
        "server_open" : 0,
        "total_outbound_connections" : 0,
        "rx_count" : 0,
        "rx_size_in_bytes" : 0,
        "tx_count" : 0,
        "tx_size_in_bytes" : 0
      },
      "http" : {
        "current_open" : 5,
        "total_opened" : 1108
      },
      "breakers" : {
        "request" : {
          "limit_size_in_bytes" : 322122547,
          "limit_size" : "307.1mb",
          "estimated_size_in_bytes" : 0,
          "estimated_size" : "0b",
          "overhead" : 1.0,
          "tripped" : 0
        },
        "fielddata" : {
          "limit_size_in_bytes" : 214748364,
          "limit_size" : "204.7mb",
          "estimated_size_in_bytes" : 356,
          "estimated_size" : "356b",
          "overhead" : 1.03,
          "tripped" : 0
        },
        "in_flight_requests" : {
          "limit_size_in_bytes" : 536870912,
          "limit_size" : "512mb",
          "estimated_size_in_bytes" : 0,
          "estimated_size" : "0b",
          "overhead" : 2.0,
          "tripped" : 0
        },
        "parent" : {
          "limit_size_in_bytes" : 510027366,
          "limit_size" : "486.3mb",
          "estimated_size_in_bytes" : 308650480,
          "estimated_size" : "294.3mb",
          "overhead" : 1.0,
          "tripped" : 0
        }
      },
      "script" : {
        "compilations" : 0,
        "cache_evictions" : 0,
        "compilation_limit_triggered" : 0
      },
      "discovery" : {
        "cluster_state_queue" : {
          "total" : 0,
          "pending" : 0,
          "committed" : 0
        },
        "published_cluster_states" : {
          "full_states" : 2,
          "incompatible_diffs" : 0,
          "compatible_diffs" : 10
        },
        "cluster_state_stats" : {
          "overall" : {
            "update_count" : 9,
            "total_time_in_millis" : 807,
            "failed_count" : 0
          },
          "remote_upload" : {
            "success_count" : 9,
            "failed_count" : 0,
            "total_time_in_millis" : 116,
            "cleanup_attempt_failed_count" : 0
          }
        }
      },
      "ingest" : {
        "total" : {
          "count" : 0,
          "time_in_millis" : 0,
          "current" : 0,
          "failed" : 0
        },
        "pipelines" : { }
      },
      "search_pipeline" : {
        "total_request" : {
          "count" : 5,
          "time_in_millis" : 158,
          "current" : 0,
          "failed" : 0
        },
        "total_response" : {
          "count" : 2,
          "time_in_millis" : 1,
          "current" : 0,
          "failed" : 0
        },
        "pipelines" : {
          "public_info" : {
            "request" : {
              "count" : 3,
              "time_in_millis" : 71,
              "current" : 0,
              "failed" : 0
            },
            "response" : {
              "count" : 0,
              "time_in_millis" : 0,
              "current" : 0,
              "failed" : 0
            },
            "request_processors" : [
              {
                "filter_query:abc" : {
                  "type" : "filter_query",
                  "stats" : {
                    "count" : 1,
                    "time_in_millis" : 0,
                    "current" : 0,
                    "failed" : 0
                  }
                }
              },
            ]
              ...
            "response_processors" : [
              {
                "rename_field" : {
                  "type" : "rename_field",
                  "stats" : {
                    "count" : 2,
                    "time_in_millis" : 1,
                    "current" : 0,
                    "failed" : 0
                  }
                }
              }
            ]
          },
          ...
        }
      },
      "adaptive_selection" : {
        "F-ByTQzVQ3GQeYzQJArJGQ" : {
          "outgoing_searches" : 0,
          "avg_queue_size" : 0,
          "avg_service_time_ns" : 501024,
          "avg_response_time_ns" : 794105,
          "rank" : "0.8"
        }
      },
      "script_cache" : {
        "sum" : {
          "compilations" : 0,
          "cache_evictions" : 0,
          "compilation_limit_triggered" : 0
        },
        "contexts" : [
          {
            "context" : "aggregation_selector",
            "compilations" : 0,
            "cache_evictions" : 0,
            "compilation_limit_triggered" : 0
          },
          {
            "context" : "aggs",
            "compilations" : 0,
            "cache_evictions" : 0,
            "compilation_limit_triggered" : 0
          },
          ...
        ]
      },
      "indexing_pressure" : {
        "memory" : {
          "current" : {
            "combined_coordinating_and_primary_in_bytes" : 0,
            "coordinating_in_bytes" : 0,
            "primary_in_bytes" : 0,
            "replica_in_bytes" : 0,
            "all_in_bytes" : 0
          },
          "total" : {
            "combined_coordinating_and_primary_in_bytes" : 40256,
            "coordinating_in_bytes" : 40256,
            "primary_in_bytes" : 45016,
            "replica_in_bytes" : 0,
            "all_in_bytes" : 40256,
            "coordinating_rejections" : 0,
            "primary_rejections" : 0,
            "replica_rejections" : 0
          },
          "limit_in_bytes" : 53687091
        }
      },
      "shard_indexing_pressure" : {
        "stats" : { },
        "total_rejections_breakup_shadow_mode" : {
          "node_limits" : 0,
          "no_successful_request_limits" : 0,
          "throughput_degradation_limits" : 0
        },
        "enabled" : false,
        "enforced" : false
      },
      "resource_usage_stats": {
        "nxLWtMdXQmWA-ZBVWU8nwA": {
          "timestamp": 1698401391000,
          "cpu_utilization_percent": "0.1",
          "memory_utilization_percent": "3.9",
          "io_usage_stats": {
            "max_io_utilization_percent": "99.6"
          }
        }
      },
      "admission_control": {
        "global_cpu_usage": {
          "transport": {
            "rejection_count": {
              "search": 3,
              "indexing": 1
            }
          }
        },
        "global_io_usage": {
          "transport": {
            "rejection_count": {
              "search": 3,
              "indexing": 1
            }
          }
        }
      },
      "caches" : {
        "request_cache" : {
          "size_in_bytes" : 1649,
          "evictions" : 0,
          "hit_count" : 0,
          "miss_count" : 18,
          "item_count" : 18,
          "store_name" : "opensearch_onheap"
        }
      }
    }
  }
}
```
</details>

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_nodes` | 物件 | 所傳回節點的相關統計資料。 |
| `_nodes.total` | 整數 | 此請求的節點總數。 |
| `_nodes.successful` | 整數 | 請求成功的節點數。 |
| `_nodes.failed` | 整數 | 請求失敗的節點數。若有請求失敗的節點，會包含失敗訊息。 |
| `cluster_name` | 字串 | 叢集的名稱。 |
| [`nodes`](#nodes) | 物件 | 此請求所含節點的統計資料。 |

### `nodes`

`nodes` 物件包含請求所傳回的所有節點及其 ID。每個節點具有下列屬性。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`timestamp` | 整數 | 收集節點統計資料的時間，以自 epoch 起算的毫秒數表示。
`name` | 字串 | 節點的名稱。
`transport_address` | IP 位址 | 叢集中的節點用來在內部通訊的傳輸層主機與連接埠。
`host` | IP 位址 | 節點的網路主機。
`ip` | IP 位址 | 節點的 IP 位址與連接埠。
`roles` | 陣列 | 節點的角色 (例如 `cluster_manager`、`data` 或 `ingest`)。
`attributes` | 物件 | 節點的屬性 (例如 `shard_indexing_pressure_enabled`)。
[`indices`](#indices) | 物件 | 節點上具有分片的每個索引的索引統計資料。
[`os`](#os) | 物件 | 節點作業系統的相關統計資料。
[`process`](#process) | 物件 | 節點的處理程序統計資料。
[`jvm`](#jvm) | 物件 | 節點 JVM 的相關統計資料。
[`thread_pool`](#thread_pool)| 物件 | 節點各執行緒集區的相關統計資料。
[`fs`](#fs) | 物件 | 節點檔案儲存區的相關統計資料。
[`transport`](#transport) | 物件 | 節點的傳輸統計資料。
`http` | 物件 | 節點的 HTTP 統計資料。
`http.current_open` | 整數 | 節點目前開啟的 HTTP 連線數。
`http.total_opened` | 整數 | 節點自啟動以來開啟的 HTTP 連線總數。
[`breakers`](#breakers) | 物件 | 節點斷路器的相關統計資料。
[`script`](#script-and-script_cache)| 物件 | 節點的指令碼統計資料。
[`script_cache`](#script-and-script_cache)| 物件 | 節點的指令碼快取統計資料。
[`discovery`](#discovery) | 物件 | 節點的節點探索統計資料。
[`ingest`](#ingest) | 物件 | 節點的匯入統計資料。
[`search_pipeline`](#search_pipeline) | 物件 | [搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/) 的相關統計資料。
[`adaptive_selection`](#adaptive_selection) | 物件 | 節點調適性選取的相關統計資料。
[`indexing_pressure`](#indexing_pressure) | 物件 | 節點索引編製壓力的相關統計資料。
[`shard_indexing_pressure`](#shard_indexing_pressure) | 物件 | 分片層級索引編製壓力的相關統計資料。
[`search_backpressure`]({{site.url}}{{site.baseurl}}/opensearch/search-backpressure#search-backpressure-stats-api) | 物件 | 搜尋背壓的相關統計資料。
[`cluster_manager_throttling`](#cluster_manager_throttling) | 物件 | 叢集管理員節點上受節流工作的相關統計資料。
[`task_cancellation`](#task_cancellation) | 物件 | 取消後仍繼續執行之工作的相關統計資料。
[`weighted_routing`](#weighted_routing) | 物件 | 加權輪詢請求的相關統計資料。
[`resource_usage_stats`](#resource_usage_stats) | 物件 | 節點資源使用量的相關統計資料。
[`admission_control`](#admission_control) | 物件 | 節點准入控制的相關統計資料。
[`concurrency_limiters`](#concurrency_limiters) | 物件 | 節點調適性並行限制器的相關統計資料。當您請求 `concurrency_limiter` 指標時傳回。
[`caches`](#caches) | 物件 | 節點上快取的相關統計資料。

### `indices`

`indices` 物件包含此節點上具有分片的每個索引的索引統計資料。每個索引具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`docs` | `Object` | 節點上所有現存主要分片的文件統計資料。
`docs.count` | `Integer` | Lucene 回報的文件數量。排除已刪除的文件，以及尚未指派至分段的最近編製索引文件。巢狀文件會分開計算。
`docs.deleted` | `Integer` | Lucene 回報的已刪除文件數量。排除尚未影響分段的最近刪除作業。
`store` | `Object` | 節點上各分片大小的統計資料。
`store.size_in_bytes` | `Integer` | 節點上所有分片的總大小。
`store.reserved_in_bytes` | `Integer` | 因還原快照與對等復原等活動，分片儲存空間預計將成長的位元組數。
`indexing` | `Object` | 節點的編製索引作業統計資料。
`indexing.index_total` | `Integer` | 節點上編製索引作業的總數。
`indexing.index_time_in_millis` | `Integer` | 所有編製索引作業的總時間，單位為毫秒。
`indexing.index_current` | `Integer` | 目前正在執行的編製索引作業數量。
`indexing.index_failed` | `Integer` | 已失敗的編製索引作業數量。
`indexing.delete_total` | `Integer` | 刪除作業的總數。
`indexing.delete_time_in_millis` | `Integer` | 所有刪除作業的總時間，單位為毫秒。
`indexing.delete_current` | `Integer` | 目前正在執行的刪除作業數量。
`indexing.noop_update_total` | `Integer` | 無作業 (no-op) 的總數。
`indexing.is_throttled` | `Boolean` | 指定是否有任何作業受到節流。
`indexing.throttle_time_in_millis` | `Integer` | 節流作業的總時間，單位為毫秒。
`get` | `Object` | 節點的 get 作業統計資料。
`get.total` | `Integer` | get 作業的總數。
`get.time_in_millis` | `Integer` | 所有 get 作業的總時間，單位為毫秒。
`get.exists_total` | `Integer` | 成功的 get 作業總數。
`get.exists_time_in_millis` | `Integer` | 所有成功 get 作業的總時間，單位為毫秒。
`get.missing_total` | `Integer` | 失敗的 get 作業數量。
`get.missing_time_in_millis` | `Integer` | 所有失敗 get 作業的總時間，單位為毫秒。
`get.current` | `Integer` | 目前正在執行的 get 作業數量。
`search` | `Object` | 節點的搜尋作業統計資料。
`search.concurrent_avg_slice_count` | `Integer` | 所有搜尋請求的平均切片數。計算方式為切片總數除以並行搜尋請求的總數。
`search.concurrent_query_total` | `Integer` | 使用並行分段搜尋的查詢作業總數。
`search.concurrent_query_time_in_millis` | `Integer` | 所有使用並行分段搜尋的查詢作業所花費的總時間，單位為毫秒。
`search.concurrent_query_current` | `Integer` | 目前正在執行且使用並行分段搜尋的查詢作業數量。
`search.startree_query_total` | `Integer` | 使用 star tree 進行搜尋的查詢作業總數。
`search.startree_query_time_in_millis` | `Integer` | 所有使用 star tree 進行搜尋的查詢作業所花費的總時間，單位為毫秒。
`search.startree_query_current` | `Integer` | 目前正在執行且使用 star tree 進行搜尋的查詢作業數量。
`search.startree_query_failed` | `Integer` | 使用 star tree 進行搜尋且失敗的查詢作業數量。
`search.open_contexts` | `Integer` | 開啟中的搜尋情境數量。
`search.query_total` | `Integer` | 分片查詢作業的總數。
`search.query_time_in_millis` | `Integer` | 所有分片查詢作業的總時間，單位為毫秒。
`search.query_current` | `Integer` | 目前正在執行的分片查詢作業數量。
`search.query_failed` | `Integer` | 失敗的分片查詢作業總數。
`search.fetch_total` | `Integer` | 分片擷取作業的總數。
`search.fetch_time_in_millis` | `Integer` | 所有分片擷取作業的總時間，單位為毫秒。
`search.fetch_current` | `Integer` | 目前正在執行的分片擷取作業數量。
`search.scroll_total` | `Integer` | 分片捲動 (scroll) 作業的總數。
`search.scroll_time_in_millis` | `Integer` | 所有分片捲動作業的總時間，單位為毫秒。
`search.scroll_current` | `Integer` | 目前正在執行的分片捲動作業數量。
`search.point_in_time_total` | `Integer` | 自節點上次重新啟動以來，已建立 (已完成與作用中) 的分片 Point in Time (PIT) 情境總數。
`search.point_in_time_time_in_millis` | `Integer` | 自節點上次重新啟動以來，分片 PIT 情境保持開啟的時間長度，單位為毫秒。
`search.point_in_time_current` | `Integer` | 目前開啟中的分片 PIT 情境數量。
`search.suggest_total` | `Integer` | 分片建議 (suggest) 作業的總數。
`search.suggest_time_in_millis` | `Integer` | 所有分片建議作業的總時間，單位為毫秒。
`search.suggest_current` | `Integer` | 目前正在執行的分片建議作業數量。
`search.search_idle_reactivate_count_total` | `Integer` | 所有分片從閒置狀態被啟用的總次數。
`search.request` | `Object` | 節點的協調器搜尋作業統計資料。
`search.request.took.time_in_millis` | `Integer` | 所有搜尋請求所花費的總時間，單位為毫秒。
`search.request.took.current` | `Integer` | 目前正在執行的搜尋請求數量。
`search.request.took.total` | `Integer` | 已完成的搜尋請求總數。
`search.request.dfs_pre_query.time_in_millis` | `Integer` | 所有協調器深度優先搜尋 (DFS) 查詢前置作業的總時間，單位為毫秒。
`search.request.dfs_pre_query.current` | `Integer` | 目前正在執行的協調器 DFS 查詢前置作業數量。
`search.request.dfs_pre_query.total` | `Integer` | 已完成的協調器 DFS 查詢前置作業總數。
`search.request.query.time_in_millis` | `Integer` | 所有協調器查詢作業的總時間，單位為毫秒。
`search.request.query.current` | `Integer` | 目前正在執行的協調器查詢作業數量。
`search.request.query.total` | `Integer` | 已完成的協調器查詢作業總數。
`search.request.fetch.time_in_millis` | `Integer` | 所有協調器擷取作業的總時間，單位為毫秒。
`search.request.fetch.current` | `Integer` | 目前正在執行的協調器擷取作業數量。
`search.request.fetch.total` | `Integer` | 已完成的協調器擷取作業總數。
`search.request.dfs_query.time_in_millis` | `Integer` | 所有協調器 DFS 查詢前置作業的總時間，單位為毫秒。
`search.request.dfs_query.current` | `Integer` | 目前正在執行的協調器 DFS 查詢前置作業數量。
`search.request.dfs_query.total` | `Integer` | 已完成的協調器 DFS 查詢前置作業總數。
`search.request.expand.time_in_millis` | `Integer` | 所有協調器展開作業的總時間，單位為毫秒。
`search.request.expand.current` | `Integer` | 目前正在執行的協調器展開作業數量。
`search.request.expand.total` | `Integer` | 已完成的協調器展開作業總數。
`search.request.can_match.time_in_millis` | `Integer` | 所有協調器比對作業的總時間，單位為毫秒。
`search.request.can_match.current` | `Integer` | 目前正在執行的協調器比對作業數量。
`search.request.can_match.total` | `Integer` | 已完成的協調器比對作業總數。
`merges` | `Object` | 節點的合併作業統計資料。
`merges.current` | `Integer` | 目前正在執行的合併作業數量。
`merges.current_docs` | `Integer` | 目前正在執行的文件合併數量。
`merges.current_size_in_bytes` | `Integer` | 用於執行目前合併作業的記憶體大小，單位為位元組。
`merges.total` | `Integer` | 合併作業的總數。
`merges.total_time_in_millis` | `Integer` | 合併的總時間，單位為毫秒。
`merges.total_docs` | `Integer` | 已合併的文件總數。
`merges.total_size_in_bytes` | `Integer` | 所有已合併文件的總大小，單位為位元組。
`merges.total_stopped_time_in_millis` | `Integer` | 花費在停止合併作業的總時間，單位為毫秒。
`merges.total_throttled_time_in_millis` | `Integer` | 花費在節流合併作業的總時間，單位為毫秒。
`merges.total_auto_throttle_in_bytes` | `Integer` | 自動節流的合併作業總大小，單位為位元組。
`refresh` | `Object` | 節點的重新整理作業統計資料。
`refresh.total` | `Integer` | 重新整理作業的總數。
`refresh.total_time_in_millis` | `Integer` | 所有重新整理作業的總時間，單位為毫秒。
`refresh.external_total` | `Integer` | 外部重新整理作業的總數。
`refresh.external_total_time_in_millis` | `Integer` | 所有外部重新整理作業的總時間，單位為毫秒。
`refresh.listeners` | `Integer` | 重新整理監聽器的數量。
`flush` | `Object` | 節點的排清作業統計資料。
`flush.total` | `Integer` | 排清作業的總數。
`flush.periodic` | `Integer` | 週期性排清作業的總數。
`flush.total_time_in_millis` | `Integer` | 所有排清作業的總時間，單位為毫秒。
`warmer` | `Object` | 節點的索引預熱作業統計資料。
`warmer.current` | `Integer` | 目前的索引預熱作業數量。
`warmer.total` | `Integer` | 索引預熱作業的總數。
`warmer.total_time_in_millis` | `Integer` | 所有索引預熱作業的總時間，單位為毫秒。
`query_cache` | 節點的查詢快取作業統計資料。
`query_cache.memory_size_in_bytes` | 整數 | 節點中所有分片的查詢快取所使用的記憶體量。
`query_cache.total_count` | 整數 | 查詢快取中的命中與未命中總數。
`query_cache.hit_count` | 整數 | 查詢快取中的命中總數。
`query_cache.miss_count` | 整數 | 查詢快取中的未命中總數。
`query_cache.cache_size` | 整數 | 目前位於查詢快取中的查詢數量。
`query_cache.cache_count` | 整數 | 已加入查詢快取的查詢總數，包括其後已被驅離的查詢。
`query_cache.evictions` | 整數 | 從查詢快取驅離的數量。
`fielddata` | 物件 | 節點中所有分片的欄位資料快取統計資料。
`fielddata.memory_size_in_bytes` | 整數 | 節點中所有分片的欄位資料快取所使用的記憶體總量。
`fielddata.evictions` | 整數 | 欄位資料快取中的驅離次數。
`fielddata.item_count` | 整數 | 欄位資料快取中的項目數量。
`fielddata.fields` | 物件 | 包含所有欄位資料欄位。
`completion` | 物件 | 節點中所有分片的自動完成 (completion) 統計資料。
`completion.size_in_bytes` | 整數 | 節點中所有分片的 completion 所使用的記憶體總量，單位為位元組。
`completion.fields` | 物件 | 包含完成欄位。
`segments` | 物件 | 節點中所有分片的分段統計資料。
`segments.count` | 整數 | 分段總數。
`segments.memory_in_bytes` | 整數 | 記憶體總量，以位元組為單位。
`segments.terms_memory_in_bytes` | 整數 | 用於詞彙的記憶體總量，以位元組為單位。
`segments.stored_fields_memory_in_bytes` | 整數 | 用於已儲存欄位的記憶體總量，以位元組為單位。
`segments.term_vectors_memory_in_bytes` | 整數 | 用於詞彙向量的記憶體總量，以位元組為單位。
`segments.norms_memory_in_bytes` | 整數 | 用於正規化因子的記憶體總量，以位元組為單位。
`segments.points_memory_in_bytes` | 整數 | 用於 points 的記憶體總量，以位元組為單位。
`segments.doc_values_memory_in_bytes` | 整數 | 用於 doc values 的記憶體總量，以位元組為單位。
`segments.index_writer_memory_in_bytes` | 整數 | 所有索引寫入器使用的記憶體總量，以位元組為單位。
`segments.version_map_memory_in_bytes` | 整數 | 所有版本對應使用的記憶體總量，以位元組為單位。
`segments.fixed_bit_set_memory_in_bytes` | 整數 | 固定位元集使用的記憶體總量，以位元組為單位。固定位元集用於巢狀物件與 join 欄位。
`segments.max_unsafe_auto_id_timestamp` | 整數 | 最近一次退役的索引請求的時間戳記，以自 epoch 起算的毫秒數為單位。
`segments.segment_replication` | 物件 | 當節點上啟用分段複寫時，所有主要分片的分段複寫統計資料。
`segments.segment_replication.max_bytes_behind` | long | 落後主要分片的最大位元組數。
`segments.segment_replication.total_bytes_behind` | long | 落後主要分片的總位元組數。
`segments.segment_replication.max_replication_lag` | long | 副本追上其主要分片所花費的最長時間，以毫秒為單位。 
`segments.remote_store` | 物件 | 遠端分段存放區作業的統計資料。
`segments.remote_store.upload` | 物件 | 與上傳至遠端分段存放區相關的統計資料。
`segments.remote_store.upload.total_upload_size` | 物件 | 上傳至遠端分段存放區的資料量，以位元組為單位。
`segments.remote_store.upload.total_upload_size.started_bytes` | 整數 | 上傳開始後，要上傳至遠端分段存放區的位元組數。
`segments.remote_store.upload.total_upload_size.succeeded_bytes` | 整數 | 成功上傳至遠端分段存放區的位元組數。
`segments.remote_store.upload.total_upload_size.failed_bytes` | 整數 | 上傳至遠端分段存放區失敗的位元組數。
`segments.remote_store.upload.refresh_size_lag` | 物件 | 上傳期間，遠端分段存放區與本機存放區之間的延遲量。
`segments.remote_store.upload.refresh_size_lag.total_bytes` | 整數 | 上傳重新整理期間，遠端分段存放區與本機存放區之間延遲的總位元組數。
`segments.remote_store.upload.refresh_size_lag.max_bytes` | 整數 | 上傳重新整理期間，遠端分段存放區與本機存放區之間延遲的最大位元組數。
`segments.remote_store.upload.max_refresh_time_lag_in_millis` | 整數 | 遠端重新整理落後本機重新整理的最大持續時間，以毫秒為單位。
`segments.remote_store.upload.total_time_spent_in_millis` | 整數 | 花費在上傳至遠端分段存放區的總時間，以毫秒為單位。
`segments.remote_store.upload.pressure` | 物件 | 與分段存放區上傳背壓相關的統計資料。
`segments.remote_store.upload.pressure.total_rejections` | 整數 | 因分段存放區上傳背壓而遭拒絕的請求總數。
`segments.remote_store.download` | 物件 | 與從遠端分段存放區下載相關的統計資料。
`segments.remote_store.download.total_download_size` | 物件 | 從遠端分段存放區下載的資料總量。
`segments.remote_store.download.total_download_size.started_bytes` | 整數 | 下載開始後，從遠端分段存放區下載的位元組數。
`segments.remote_store.download.total_download_size.succeeded_bytes` | 整數 | 成功從遠端分段存放區下載的位元組數。
`segments.remote_store.download.total_download_size.failed_bytes` | 整數 | 從遠端分段存放區下載失敗的位元組數。
`segments.remote_store.download.total_time_spent_in_millis` | 整數 | 花費在從遠端分段存放區下載的總持續時間，以毫秒為單位。
`segments.file_sizes` | 整數 | 分段檔案大小的統計資料。
`translog` | 物件 | 節點的交易記錄檔作業統計資料。
`translog.operations` | 整數 | translog 作業數。
`translog.size_in_bytes` | 整數 | translog 的大小，以位元組為單位。
`translog.uncommitted_operations` | 整數 | 未提交的 translog 作業數。
`translog.uncommitted_size_in_bytes` | 整數 | 未提交的 translog 作業大小，以位元組為單位。
`translog.earliest_last_modified_age` | 整數 | translog 最早的最後修改時間長度。
`translog.remote_store` | 物件 | 與遠端 translog 存放區作業相關的統計資料。
`translog.remote_store.upload` | 物件 | 與上傳至遠端 translog 存放區相關的統計資料。
`translog.remote_store.upload.total_uploads` | 物件 | 與遠端 translog 存放區同步的次數。
`translog.remote_store.upload.total_uploads.started` | 整數 | 已開始之遠端 translog 存放區上傳同步的次數。
`translog.remote_store.upload.total_uploads.failed` | 整數 | 遠端 translog 存放區上傳同步失敗的次數。
`translog.remote_store.upload.total_uploads.succeeded` | 整數 | 遠端 translog 存放區上傳同步成功的次數。
`translog.remote_store.upload.total_upload_size` | 物件 | 上傳至遠端 translog 存放區的資料總量。
`translog.remote_store.upload.total_upload_size.started_bytes` | 整數 | 上傳開始後，正主動上傳至遠端 translog 存放區的位元組數。
`translog.remote_store.upload.total_upload_size.failed_bytes` | 整數 | 上傳至遠端 translog 存放區失敗的位元組數。
`translog.remote_store.upload.total_upload_size.succeeded_bytes` | 整數 | 成功上傳至遠端 translog 存放區的位元組數。
`request_cache` | 物件 | 節點之請求快取的統計資料。
`request_cache.memory_size_in_bytes` | 整數 | 請求快取使用的記憶體大小，以位元組為單位。
`request_cache.evictions` | 整數 | 請求快取逐出的次數。
`request_cache.hit_count` | 整數 | 請求快取命中的次數。
`request_cache.miss_count` | 整數 | 請求快取未命中的次數。
`recovery` | 物件 | 節點之復原作業的統計資料。
`recovery.current_as_source` | 整數 | 已使用索引分片作為來源的復原作業數。
`recovery.current_as_target` | 整數 | 已使用索引分片作為目標的復原作業數。
`recovery.throttle_time_in_millis` | 整數 | 因節流而導致的復原作業延遲，以毫秒為單位。

### `os`

`os` 物件包含節點的作業系統統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`timestamp` | `Integer` | 作業系統統計資料的上次重新整理時間，以自紀元起算的毫秒數表示。
`cpu` | `Object` | 節點的 CPU 使用量統計資料。
`cpu.percent` | `Integer` | 系統最近的 CPU 使用量。
`cpu.load_average` | `Object` | 系統的平均負載統計資料。
`cpu.load_average.1m` | `Float` | 系統在 1 分鐘期間內的平均負載。
`cpu.load_average.5m` | `Float` | 系統在 5 分鐘期間內的平均負載。
`cpu.load_average.15m` | `Float` | 系統在 15 分鐘期間內的平均負載。
`mem` | `Object` | 節點的記憶體使用量統計資料。
`mem.total_in_bytes` | `Integer` | 實體記憶體總量，以位元組為單位。
`mem.free_in_bytes` | `Integer` | 可用實體記憶體總量，以位元組為單位。
`mem.used_in_bytes` | `Integer` | 已使用的實體記憶體總量，以位元組為單位。
`mem.free_percent` | `Integer` | 可用記憶體的百分比。
`mem.used_percent` | `Integer` | 已使用記憶體的百分比。
`swap` | `Object` | 節點的交換空間統計資料。
`swap.total_in_bytes` | `Integer` | 交換空間總量，以位元組為單位。
`swap.free_in_bytes` | `Integer` | 可用交換空間總量，以位元組為單位。
`swap.used_in_bytes` | `Integer` | 已使用的交換空間總量，以位元組為單位。
`cgroup` | `Object` | 包含節點的 `cgroup` 統計資料。僅在 Linux 上傳回。
`cgroup.cpuacct` | `Object` | 節點的 `cpuacct` 控制群組統計資料。
`cgroup.cpu` | `Object` | 節點的 CPU 控制群組統計資料。
`cgroup.memory` | `Object` | 節點的記憶體控制群組統計資料。

### `process`

`process` 物件包含節點的處理程序統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`timestamp` | `Integer` | 處理程序統計資料的上次重新整理時間，以自紀元起算的毫秒數表示。
`open_file_descriptors` | `Integer` |  與目前處理程序相關聯的已開啟檔案描述元數量。
`max_file_descriptors` | `Integer` | 系統的檔案描述元數量上限。
`cpu` | `Object` | 節點的 CPU 統計資料。
`cpu.percent` | `Integer` | 處理程序的 CPU 使用率百分比。
`cpu.total_in_millis` | `Integer` | 執行 JVM 的處理程序所使用的 CPU 時間總計，以毫秒為單位。
`mem` | `Object` | 節點的記憶體統計資料。
`mem.total_virtual_in_bytes` | `Integer` | 保證可供目前執行中處理程序使用的虛擬記憶體總量，以位元組為單位。

### `jvm`

`jvm` 物件包含節點的 JVM 統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`timestamp` | `Integer` | JVM 統計資料的上次重新整理時間，以自紀元起算的毫秒數表示。
`uptime_in_millis` | `Integer` | JVM 的運作時間，以毫秒為單位。
`mem` | `Object` | 節點上 JVM 的記憶體使用量統計資料。
`mem.heap_used_in_bytes` | `Integer` | 目前使用的記憶體量，以位元組為單位。
`mem.heap_used_percent` | `Integer` | 堆積目前使用的記憶體百分比。
`mem.heap_committed_in_bytes` | `Integer` | 可供堆積使用的記憶體量，以位元組為單位。
`mem.heap_max_in_bytes` | `Integer` | 可供堆積使用的記憶體量上限，以位元組為單位。
`mem.non_heap_used_in_bytes` | `Integer` | 目前使用的非堆積記憶體量，以位元組為單位。
`mem.non_heap_committed_in_bytes` | `Integer` | 可供使用的非堆積記憶體量上限，以位元組為單位。
`mem.pools` | `Object` | 節點的堆積記憶體使用量統計資料。
`mem.pools.young` | `Object` | 節點的新生代堆積記憶體使用量統計資料。包含已使用的記憶體量、可用記憶體量上限，以及記憶體使用量峰值。
`mem.pools.old` | `Object` | 節點的老年代堆積記憶體使用量統計資料。包含已使用的記憶體量、可用記憶體量上限，以及記憶體使用量峰值。
`mem.pools.survivor` | `Object` | 節點的存活區記憶體使用量統計資料。包含已使用的記憶體量、可用記憶體量上限，以及記憶體使用量峰值。
`threads` | `Object` | 節點的 JVM 執行緒使用量統計資料。
`threads.count` | `Integer` | JVM 中目前作用中的執行緒數量。
`threads.peak_count` | `Integer` | JVM 中的執行緒數量上限。
`gc.collectors` | `Object` | 節點的 JVM 垃圾回收器統計資料。
`gc.collectors.young` | `Integer` | 回收新生代物件的 JVM 垃圾回收器統計資料。
`gc.collectors.young.collection_count` | `Integer` | 回收新生代物件的垃圾回收器數量。
`gc.collectors.young.collection_time_in_millis` | `Integer` | 對新生代物件進行垃圾回收所花費的總時間，以毫秒為單位。
`gc.collectors.old` | `Integer` | 回收老年代物件的 JVM 垃圾回收器統計資料。
`gc.collectors.old.collection_count` | `Integer` | 回收老年代物件的垃圾回收器數量。
`gc.collectors.old.collection_time_in_millis` | `Integer` | 對老年代物件進行垃圾回收所花費的總時間，以毫秒為單位。
`buffer_pools` | `Object` | 節點的 JVM 緩衝區集區統計資料。
`buffer_pools.mapped` | `Object` | 節點的 JVM 對應緩衝區集區統計資料。
`buffer_pools.mapped.count` | `Integer` | 對應緩衝區集區的數量。
`buffer_pools.mapped.used_in_bytes` | `Integer` | 對應緩衝區集區使用的記憶體量，以位元組為單位。
`buffer_pools.mapped.total_capacity_in_bytes` | `Integer` | 對應緩衝區集區的總容量，以位元組為單位。
`buffer_pools.direct` | `Object` | 節點的 JVM 直接緩衝區集區統計資料。
`buffer_pools.direct.count` | `Integer` | 直接緩衝區集區的數量。
`buffer_pools.direct.used_in_bytes` | `Integer` | 直接緩衝區集區使用的記憶體量，以位元組為單位。
`buffer_pools.direct.total_capacity_in_bytes` | `Integer` | 直接緩衝區集區的總容量，以位元組為單位。
`classes` | `Object` | 節點上 JVM 載入的類別統計資料。
`classes.current_loaded_count` | `Integer` | JVM 目前載入的類別數量。
`classes.total_loaded_count` | `Integer` | JVM 自啟動以來載入的類別總數。
`classes.total_unloaded_count` | `Integer` | JVM 自啟動以來卸載的類別總數。

### `thread_pool`

`thread_pool` 物件包含所有執行緒集區的清單。每個執行緒集區都是以其 ID 指定的巢狀物件，並包含下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`threads` | `Integer` | 集區中的執行緒數量。
`queue` | `Integer` | 佇列中的執行緒數量。
`active` | `Integer` | 集區中作用中的執行緒數量。
`rejected` | `Integer` | 已拒絕的工作數量。
`largest` | `Integer` | 集區中的執行緒數量峰值。
`completed` | `Integer` | 已完成的工作數量。
`total_wait_time_in_nanos` | `Integer` | 工作在執行緒集區佇列中等待的總時間。只有 `search`、`search_throttled` 和 `index_searcher` 執行緒集區支援此指標。

### `fs`

`fs` 物件代表節點檔案存放區的統計資料。它具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`timestamp` | `Integer` | 檔案存放區統計資料的上次重新整理時間，以自 epoch 起算的毫秒數表示。
`total` | `Object` | 節點所有檔案存放區的統計資料。
`total.total_in_bytes` | `Integer` | 所有檔案存放區的記憶體總大小，以位元組為單位。
`total.free_in_bytes` | `Integer` | 所有檔案存放區中未配置的磁碟空間總量，以位元組為單位。
`total.available_in_bytes` | `Integer` | 所有檔案存放區中可供 JVM 使用的磁碟空間總量。代表 OpenSearch 實際可使用的記憶體量，以位元組為單位。
`data` | `Array` | 所有檔案存放區的清單。每個檔案存放區具有下列屬性。
`data.path` | `String` | 檔案存放區的路徑。
`data.mount` | `String` | 檔案存放區的掛載點。
`data.type` | `String` | 檔案存放區的類型（例如 overlay）。
`data.total_in_bytes` | `Integer` | 檔案存放區的總大小，以位元組為單位。
`data.free_in_bytes` | `Integer` | 檔案存放區中未配置的磁碟空間總量，以位元組為單位。
`data.available_in_bytes` | `Integer` | 檔案存放區中可供 JVM 使用的磁碟空間總量，以位元組為單位。
`io_stats` | `Object` | 節點的 I/O 統計資料（僅限 Linux）。包括裝置、讀取與寫入作業，以及 I/O 作業時間。

### `transport`

`transport` 物件具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`server_open` | `Integer` | OpenSearch 節點用於內部通訊的已開啟傳入 TCP 連線數。
`total_outbound_connections` | `Integer` | 節點自啟動以來已開啟的傳出傳輸連線總數。
`rx_count` | `Integer` | 節點在內部通訊期間收到的 RX（接收）封包總數。
`rx_size_in_bytes` | `Integer` | 節點在內部通訊期間收到的 RX 封包總大小，以位元組為單位。
`tx_count` | `Integer` | 節點在內部通訊期間傳送的 TX（傳送）封包總數。
`tx_size_in_bytes` | `Integer` | 節點在內部通訊期間傳送的 TX（傳送）封包總大小，以位元組為單位。

### `breakers`

`breakers` 物件包含節點斷路器的統計資料。每個斷路器都是依名稱列出的巢狀物件，並包含下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`limit_size_in_bytes` | `Integer` | 斷路器的記憶體限制，以位元組為單位。
`limit_size` | `Byte value` | 以人類可讀格式表示的斷路器記憶體限制（例如 `307.1mb`）。
`estimated_size_in_bytes` | `Integer` | 作業的預估記憶體使用量，以位元組為單位。
`estimated_size` | `Byte value` | 以人類可讀格式表示的作業預估記憶體使用量（例如 `356b`）。
`overhead` | `Float` | 所有預估值都會乘以此係數，以計算最終預估值。
`tripped` | `Integer` | 斷路器為防止記憶體不足錯誤而觸發的總次數。

### `script` 和 `script_cache`

`script` 和 `script_cache` 物件具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`script` | `Object` | 節點的指令碼統計資料。
`script.compilations` | `Integer` | 節點的指令碼編譯總次數。
`script.cache_evictions` | `Integer` | 指令碼快取清除舊資料的總次數。
`script.compilation_limit_triggered` | `Integer` | 指令碼編譯受到斷路器限制的總次數。
`script_cache` | `Object` | 節點的指令碼快取統計資料。
`script_cache.sum.compilations` | `Integer` | 節點快取中的指令碼編譯總次數。
`script_cache.sum.cache_evictions` | `Integer` | 指令碼快取清除舊資料的總次數。
`script_cache.sum.compilation_limit_triggered` | `Integer` | 快取中的指令碼編譯受到斷路器限制的總次數。
`script_cache.contexts` | `Array of objects` | 指令碼快取的情境清單。每個情境都包含其名稱、編譯次數、快取移出次數，以及指令碼受到斷路器限制的次數。

### `discovery`

`discovery` 物件包含節點探索統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`cluster_state_queue` | `Object` | 節點的叢集狀態佇列統計資料。
`cluster_state_queue.total` | `Integer` | 佇列中的叢集狀態總數。
`cluster_state_queue.pending` | `Integer` | 佇列中待處理的叢集狀態數。
`cluster_state_queue.committed` | `Integer` | 佇列中已認可的叢集狀態數。
`published_cluster_states` | `Object` | 節點已發布叢集狀態的統計資料。
`published_cluster_states.full_states` | `Integer` | 已發布的叢集狀態數。
`published_cluster_states.incompatible_diffs` | `Integer` | 已發布叢集狀態之間不相容的差異數。
`published_cluster_states.compatible_diffs` | `Integer` | 已發布叢集狀態之間相容的差異數。
`cluster_state_stats` | `Object` | 由作用中領導者發布的叢集狀態更新統計資料。
`cluster_state_stats.overall` | `Object` | 整體叢集狀態更新統計資料。
`cluster_state_stats.overall.update_count` | `Integer` | 成功的叢集狀態更新總數。
`cluster_state_stats.overall.total_time_in_millis` | `Integer` | 所有叢集狀態更新所花費的總時間，以毫秒為單位。
`cluster_state_stats.overall.failed_count` | `Integer` | 失敗的叢集狀態更新總數。
`cluster_state_stats.remote_upload` | `Object` | 與遠端上傳相關的叢集狀態更新統計資料。
`cluster_state_stats.remote_upload.success_count` | `Integer` | 成功上傳至遠端存放區的叢集狀態更新總數。
`cluster_state_stats.remote_upload.failed_count` | `Integer` | 上傳至遠端存放區失敗的叢集狀態更新總數。
`cluster_state_stats.remote_upload.total_time_in_millis` | `Integer` | 所有上傳至遠端存放區的叢集狀態更新所花費的總時間，以毫秒為單位。
`cluster_state_stats.remote_upload.cleanup_attempt_failed_count` | `Integer` | 嘗試從遠端存放區清除較舊叢集狀態時發生的失敗總數。

### `ingest`

`ingest` 物件包含匯入統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`total` | `Integer` | 節點整個生命週期的匯入統計資料。
`total.count` | `Integer` | 節點匯入的文件總數。
`total.time_in_millis` | `Integer` | 預先處理匯入文件所花費的總時間，以毫秒為單位。
`total.current` | `Integer` | 節點目前正在匯入的文件總數。
`total.failed` | `Integer` | 節點失敗的匯入作業總數。
`pipelines` | `Object` | 節點的資料匯入管線統計資料。每個管線都是以其 ID 指定的巢狀物件，並具有下列屬性。
`pipelines._id_.count` | `Integer` | 資料匯入管線預先處理的文件數。
`pipelines._id_.time_in_millis` | `Integer` | 在資料匯入管線中預先處理文件所花費的總時間，以毫秒為單位。
`pipelines._id_.failed` | `Integer` | 資料匯入管線失敗的匯入作業總數。
`pipelines._id_.processors` | `Array of objects` | 匯入處理器的統計資料。包括目前正在轉換的文件數、已轉換的文件總數、轉換失敗次數，以及轉換文件所花費的時間。

### `search_pipeline`

`search_pipeline` 物件包含與[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)相關的統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`total_request` | `Object` | 與所有搜尋請求處理器相關的累計統計資料。
`total_request.count` | `Integer` | 搜尋請求處理器執行的總次數。
`total_request.time_in_millis` | `Integer` | 所有搜尋請求處理器執行所花費的總時間，單位為毫秒。
`total_request.current` | `Integer` | 目前正在進行的搜尋請求處理器執行總次數。
`total_request.failed` | `Integer` | 失敗的搜尋請求處理器執行總次數。
`total_response` | `Object` | 與所有搜尋回應處理器相關的累計統計資料。
`total_response.count` | `Integer` | 搜尋回應處理器執行的總次數。
`total_response.time_in_millis` | `Integer` | 所有搜尋回應處理器執行所花費的總時間，單位為毫秒。
`total_response.current` | `Integer` | 目前正在進行的搜尋回應處理器執行總次數。
`total_response.failed` | `Integer` | 失敗的搜尋回應處理器執行總次數。
`pipelines` | `Object` | 搜尋管線統計資料。每個管線都是以 ID 指定的巢狀物件，其屬性列於後續各列。如果處理器具有 `tag`，則該處理器的統計資料會提供在名稱為 `<processor_type>:<tag>` 的物件中 (例如 `filter_query:abc`)。沒有 `tag` 的同類型所有處理器的統計資料會彙總後提供在名稱為 `<processor-type>` 的物件中 (例如 `filter_query`)。
`pipelines._id_.request.count` | `Integer` | 搜尋管線執行的搜尋請求處理器執行次數。
`pipelines._id_.request.time_in_millis` | `Integer` | 搜尋管線中搜尋請求處理器執行所花費的總時間，單位為毫秒。
`pipelines._id_.request.current` | `Integer` | 搜尋管線目前正在進行的搜尋請求處理器執行次數。
`pipelines._id_.request.failed` | `Integer` | 搜尋管線失敗的搜尋請求處理器執行次數。
`pipelines._id_.request_processors` | `Array of objects` | 搜尋請求處理器的統計資料。包含執行總次數、執行所花費的總時間、目前正在進行的執行總次數，以及失敗的執行次數。
`pipelines._id_.response.count` | `Integer` | 搜尋管線執行的搜尋回應處理器執行次數。
`pipelines._id_.response.time_in_millis` | `Integer` | 搜尋管線中搜尋回應處理器執行所花費的總時間，單位為毫秒。
`pipelines._id_.response.current` | `Integer` | 搜尋管線目前正在進行的搜尋回應處理器執行次數。
`pipelines._id_.response.failed` | `Integer` | 搜尋管線失敗的搜尋回應處理器執行次數。
`pipelines._id_.response_processors` | `Array of objects` | 搜尋回應處理器的統計資料。包含執行總次數、執行所花費的總時間、目前正在進行的執行總次數，以及失敗的執行次數。

### `adaptive_selection`

`adaptive_selection` 物件包含自適應選取統計資料。每個項目都是以節點 ID 指定，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`outgoing_searches` | `Integer` | 該節點的傳出搜尋請求數量。
`avg_queue_size` | `Integer` | 該節點搜尋請求的滾動平均佇列大小 (指數加權)。
`avg_service_time_ns` | `Integer` | 搜尋請求的滾動平均服務時間，單位為奈秒 (指數加權)。
`avg_response_time_ns` | `Integer` | 搜尋請求的滾動平均回應時間，單位為奈秒 (指數加權)。
`rank` | `String` | 在路由請求時用於選擇分片的節點排名。

### `indexing_pressure`

`indexing_pressure` 物件包含索引壓力統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`memory` | `Object` | 與索引負載的記憶體消耗相關的統計資料。
`memory.current` | `Object` | 與目前索引負載的記憶體消耗相關的統計資料。
`memory.current.combined_coordinating_and_primary_in_bytes` | `Integer` | 協調或主要階段中索引請求所使用的總記憶體，單位為位元組。如果主要階段在本機執行，節點可以重複使用協調記憶體，因此總記憶體不一定等於協調與主要階段記憶體使用量的總和。
`memory.current.coordinating_in_bytes` | `Integer` | 協調階段中索引請求所消耗的總記憶體，單位為位元組。
`memory.current.primary_in_bytes` | `Integer` | 主要階段中索引請求所消耗的總記憶體，單位為位元組。
`memory.current.replica_in_bytes` | `Integer` | 副本階段中索引請求所消耗的總記憶體，單位為位元組。
`memory.current.all_in_bytes` | `Integer` | 協調、主要或副本階段中索引請求所消耗的總記憶體。

### `shard_indexing_pressure`

`shard_indexing_pressure` 物件包含[分片索引壓力]({{site.url}}{{site.baseurl}}/opensearch/shard-indexing-backpressure)統計資料，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
[`stats`]({{site.url}}{{site.baseurl}}/opensearch/stats-api/) | `Object` | 關於分片索引壓力的統計資料。
`total_rejections_breakup_shadow_mode` | `Object` | 如果在影子模式下執行，`total_rejections_breakup_shadow_mode` 物件包含節點中所有分片的請求拒絕條件相關統計資料。
`total_rejections_breakup_shadow_mode.node_limits` | `Integer` | 因節點記憶體限制而拒絕的總次數。當所有分片達到指派給節點的記憶體限制 (例如堆積大小的 10%) 時，分片便無法在節點上接收更多流量，索引請求會被拒絕。
`total_rejections_breakup_shadow_mode.no_successful_request_limits` | `Integer` | 當節點佔用率突破其軟性限制，且分片有多個等待執行的未完成請求時的拒絕總次數。在這種情況下，系統會持續拒絕額外的索引請求，直到系統復原為止。
`total_rejections_breakup_shadow_mode.throughput_degradation_limits` | `Integer` | 當節點佔用率突破其軟性限制，且分片層級的請求周轉時間持續惡化時的拒絕總次數。在這種情況下，系統會持續拒絕額外的索引請求，直到系統復原為止。
`enabled` | `Boolean` | 指定節點是否已開啟分片索引壓力功能。
`enforced` | `Boolean` | 若為 true，分片索引壓力會以強制模式執行 (會有拒絕)。若為 false，分片索引壓力會以影子模式執行 (不會有拒絕，但會記錄統計資料，並可在 `total_rejections_breakup_shadow_mode` 物件中擷取)。僅在啟用分片索引壓力時適用。 

### `cluster_manager_throttling`

`cluster_manager_throttling` 物件包含叢集管理員節點上受節流工作的統計資料。僅會為目前獲選為叢集管理員的節點填入此資料。  

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`stats` | `Object` | 叢集管理員節點上受節流工作的統計資料。
`stats.total_throttled_tasks` | `Long` | 受節流工作的總數。
`stats.throttled_tasks_per_task_type` | `Object` | 依個別工作類型細分的統計資料，以鍵值對指定。鍵為個別工作類型，其值代表遭節流的請求數。

### `task_cancellation`
於 2.9 版推出
{: .label .label-purple }

`task_cancellation` 物件包含在標記為取消後仍繼續執行之工作的統計資料。這有助於監控工作取消的成效，並找出未正確回應取消請求的工作。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`search_task` | `Object` | 取消後仍繼續執行之父搜尋工作的統計資料。
`search_task.current_count_post_cancel` | `Long` | 取消後仍在執行之搜尋工作的目前數量。
`search_task.total_count_post_cancel` | `Long` | 自節點上次重新啟動以來，取消後仍繼續執行之搜尋工作的總數。
`search_shard_task` | `Object` | 取消後仍繼續執行之搜尋分片工作的統計資料。
`search_shard_task.current_count_post_cancel` | `Long` | 取消後仍在執行之搜尋分片工作的目前數量。
`search_shard_task.total_count_post_cancel` | `Long` | 自節點上次重新啟動以來，取消後仍繼續執行之搜尋分片工作的總數。

### `weighted_routing`

`weighted_routing` 物件包含加權輪詢請求的統計資料。具體來說，它包含此節點在「被劃出區域 (zoned out)」時仍處理請求的次數計數。

欄位 | 欄位類型 | 說明
:--- |:-----------| :---
`stats` | `Object` | 加權路由的統計資料。
`fail_open_count` | `Integer` | 當節點的路由權重設為零時，此節點上的分片處理請求的次數。

### `resource_usage_stats`

`resource_usage_stats` 物件包含資源使用量統計資料。每個項目由節點 ID 指定，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- |:-----------| :---
`timestamp` | `Integer` | 資源使用量統計資料的上次重新整理時間，以自 epoch 起算的毫秒數表示。
`cpu_utilization_percent` | `Float` | 在 `node.resource.tracker.global_cpu_usage.window_duration` 設定中所設定時間範圍內，任何 OpenSearch 處理程序平均 CPU 使用量的統計資料。
`memory_utilization_percent` | `Float` | 在 `node.resource.tracker.global_jvmmp.window_duration` 設定中所設定時間範圍內，節點 JVM 記憶體使用量的統計資料。
`max_io_utilization_percent` | `Float` | （僅限 Linux）在 `node.resource.tracker.global_io_usage.window_duration` 設定中所設定時間範圍內，任何 OpenSearch 處理程序平均 IO 使用量的統計資料。

### `admission_control`

`admission_control` 物件包含根據資源耗用量而拒絕搜尋與編製索引請求的計數，並具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`admission_control.global_cpu_usage.transport.rejection_count.search` | `Integer` | 達到節點 CPU 使用量上限時，傳輸層中搜尋遭拒的總數。在此情況下，會拒絕其他搜尋請求，直到系統復原為止。CPU 使用量上限設定於 `admission_control.search.cpu_usage.limit` 設定中。
`admission_control.global_cpu_usage.transport.rejection_count.indexing` | `Integer` | 達到節點 CPU 使用量上限時，傳輸層中編製索引遭拒的總數。任何其他編製索引請求都會遭到拒絕，直到系統復原為止。CPU 使用量上限設定於 `admission_control.indexing.cpu_usage.limit` 設定中。
`admission_control.global_io_usage.transport.rejection_count.search` | `Integer` | 達到節點 IO 使用量上限時，傳輸層中搜尋遭拒的總數。任何其他搜尋請求都會遭到拒絕，直到系統復原為止。CPU 使用量上限設定於 `admission_control.search.io_usage.limit` 設定中（僅限 Linux）。
`admission_control.global_io_usage.transport.rejection_count.indexing` | `Integer` | 達到節點 IO 使用量上限時，傳輸層中編製索引遭拒的總數。任何其他編製索引請求都會遭到拒絕，直到系統復原為止。IO 使用量上限設定於 `admission_control.indexing.io_usage.limit` 設定中（僅限 Linux）。

### `concurrency_limiters`

`concurrency_limiters` 物件包含每個已設定之[並行限制器]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/concurrency-limits/)的一個項目，並以限制器名稱作為鍵。當您請求 `concurrency_limiter` 指標時會傳回此物件。每個項目具有下列屬性。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`action_name` | `String` | 限制器所套用的傳輸動作。
`mode` | `String` | 限制器的[模式]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/concurrency-limits/#modes)。有效值為 `disabled`、`monitor_only` 及 `enforced`。
`algorithm` | `String` | 用於調整限制的[演算法]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/concurrency-limits/#algorithms)。有效值為 `vegas`、`gradient2` 及 `aimd`。
`current_limit` | `Integer` | 目前的自適應並行限制，不包含[暴衝容量]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/concurrency-limits/#burst-capacity)。
`in_flight` | `Integer` | 目前正在處理的請求數。
`total_rejected` | `Integer` | 遭拒請求的累計數量。在 `monitor_only` 模式下，這會計入原本會遭拒的請求。
`last_rtt_millis` | `Integer` | 最近觀察到的來回時間，以毫秒為單位。在限制器記錄到完成的請求之前會省略此項。
`rtt_no_load_millis` | `Integer` | 在無負載下測得的來回時間，以毫秒為單位，用作延遲基準。在限制器記錄到完成的請求之前會省略此項。

### `caches`

由於此 API 支援實驗性的[分層快取功能]({{site.url}}{{site.baseurl}}/search-plugins/caching/tiered-cache/)，本節中的回應可能會有所變更。若未啟用分層快取功能旗標，API 會對所有值傳回 `0`。
{: .warning}

`caches` 物件包含快取統計資料，例如 `request_cache` 統計資料。無論查詢參數 `level` 的值為何，一律會傳回每個子指標內的總計值。 

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`request_cache` | `Object` | 請求快取的統計資料。
`request_cache.size_in_bytes` | `Integer` | 請求快取的總大小，以位元組為單位。
`request_cache.evictions` | `Integer` | 請求快取遭逐出的總次數。
`request_cache.hit_count` | `Integer` | 請求快取的總命中次數。
`request_cache.miss_count` | `Integer` | 請求快取的總未命中次數。
`request_cache.item_count` | `Integer` | 請求快取中的項目總數。
`request_cache.store_name` | `String` | 請求快取所使用之存放區類型的名稱。如需詳細資訊，請參閱[分層快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/tiered-cache/)。 

若將 `level` 查詢參數設為其有效值之一，即 `indices`、`shard` 或 `tier`，則 `caches.request_cache` 中會出現其他欄位，依這些層級將值分類。 
例如，若 `level=indices,tier`、正在使用分層快取，且節點具有名為 `index0` 與 `index1` 的索引，則 `caches` 物件會針對每個層級值組合包含相同的五個指標，如下表所示。

欄位 | 欄位類型 | 說明
:--- | :--- | :---
`request_cache.indices.index0.tier.on_heap` | `Object` | 包含堆積層上 `index0` 的五個指標。
`request_cache.indices.index0.tier.disk` | `Object` | 包含磁碟層上 `index0` 的五個指標。
`request_cache.indices.index1.tier.on_heap` | `Object` | 包含堆積層上 `index1` 的五個指標。
`request_cache.indices.index1.tier.disk` | `Object` | 包含磁碟層上 `index1` 的五個指標。 

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:monitor/nodes/stats`。
