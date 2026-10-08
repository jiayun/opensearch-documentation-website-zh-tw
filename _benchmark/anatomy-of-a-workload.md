---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載的結構"
nav_order: 22
has_children: true
has_toc: false
redirect_from:
  - /benchmark/user-guide/understanding-workloads/anatomy-of-a-workload/
  - /benchmark/reference/workloads/
  - /benchmark/reference/workloads/index/
  - /benchmark/workloads/
  - /benchmark/workloads/index/
  - /benchmark/user-guide/understanding-workloads/
---

# 工作負載的結構

工作負載是一或多個基準測試情境的規格。所有工作負載都包含下列檔案和目錄：

- [`workload.json`](#workloadjson)：包含所有工作負載設定。
- [`index.json`](#indexjson)：包含文件對應和參數，以及索引設定。
- [`files.txt`](#filestxt)：包含資料語料庫的檔案名稱。
- [`_test-procedures`](#_operations-and-_test-procedures)：大多數工作負載只包含一個預設的測試程序，該程序在 `default.json` 中設定。
- [`_operations`](#_operations-and-_test-procedures)：包含測試程序中使用的所有操作。
- `workload.py`：為測試新增更多動態功能。

<!-- vale off -->
## workload.json
<!-- vale on -->

`workload.json` 檔案通常包含下列元素：

- [`indices`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/indices/)：定義工作負載所使用的相關索引和索引範本。若要建立索引，請指定其 `name`。若要為索引新增定義，請使用 `body` 選項，並將其指向包含索引定義的 JSON 檔案。
- [`corpora`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/corpora/)：定義工作負載所使用的所有文件語料庫，包括包含文件的來源檔案，以及每個檔案中的文件數量。
- [`operations`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/operations/)：**選用**。列出工作負載所執行的 OpenSearch API 操作，以及這些操作的參數化方式。例如，您可以列出名為 `create-index` 的操作，該操作會在基準測試叢集中建立一個索引，供 OpenSearch Benchmark 寫入文件。
- [`schedule`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/schedule/)：以內嵌方式定義操作及操作的執行順序。或者，您也可以使用 `operations` 將操作分組，並使用 [`test_procedures`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/test-procedures/) 參數指定操作的順序。

下列範例工作負載展示了這些元素如何搭配運作。您可以在自己的基準測試組態中執行此工作負載：

```json
{
  "description": "Tutorial benchmark for OpenSearch Benchmark",
  "indices": [
    {
      "name": "movies",
      "body": "index.json"
    }
  ],
  "corpora": [
    {
      "name": "movies",
      "documents": [
        {
          "source-file": "movies-documents.json",
          "document-count": 11658903, # Fetch document count from command line
          "uncompressed-bytes": 1544799789 # Fetch uncompressed bytes from command line
        }
      ]
    }
  ],
  "schedule": [
    {
      "operation": {
        "operation-type": "create-index"
      }
    },
    {
      "operation": {
        "operation-type": "cluster-health",
        "request-params": {
          "wait_for_status": "green"
        },
        "retry-until-success": true
      }
    },
    {
      "operation": {
        "operation-type": "bulk",
        "bulk-size": 5000
      },
      "warmup-time-period": 120,
      "clients": 8
    },
    {
      "operation": {
        "name": "query-match-all",
        "operation-type": "search",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "iterations": 1000,
      "target-throughput": 100
    }
  ]
}
```

<!-- vale off -->
## index.json
<!-- vale on -->

`index.json` 檔案定義了在 `create-index` 操作期間，工作負載文件的資料對應、索引編製參數和索引設定。

當 OpenSearch Benchmark 為工作負載建立索引時，會使用 `index.json` 檔案中的索引設定和對應範本。`index.json` 檔案中的對應是根據工作負載語料庫中單一文件的對應而來，該語料庫儲存在 `files.txt` 檔案中。以下是 `nyc_taxis` 工作負載的 `index.json` 檔案範例。您可以自訂欄位，例如 `number_of_shards`、`number_of_replicas`、`query_cache_enabled` 和 `requests_cache_enabled`。

```json
{
  "settings": {
    "index.number_of_shards": {% raw %}{{number_of_shards | default(1)}}{% endraw %},
    "index.number_of_replicas": {% raw %}{{number_of_replicas | default(0)}}{% endraw %},
    "index.queries.cache.enabled": {% raw %}{{query_cache_enabled | default(false) | tojson}}{% endraw %},
    "index.requests.cache.enable": {% raw %}{{requests_cache_enabled | default(false) | tojson}}{% endraw %}
  },
  "mappings": {
    "_source": {
      "enabled": {% raw %}{{ source_enabled | default(true) | tojson }}{% endraw %}
    },
    "properties": {
      "surcharge": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "dropoff_datetime": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "trip_type": {
        "type": "keyword"
      },
      "mta_tax": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "rate_code_id": {
        "type": "keyword"
      },
      "passenger_count": {
        "type": "integer"
      },
      "pickup_datetime": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "tolls_amount": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "tip_amount": {
        "type": "half_float"
      },
      "payment_type": {
        "type": "keyword"
      },
      "extra": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "vendor_id": {
        "type": "keyword"
      },
      "store_and_fwd_flag": {
        "type": "keyword"
      },
      "improvement_surcharge": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "fare_amount": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "ehail_fee": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "cab_color": {
        "type": "keyword"
      },
      "dropoff_location": {
        "type": "geo_point"
      },
      "vendor_name": {
        "type": "text"
      },
      "total_amount": {
        "scaling_factor": 100,
        "type": "scaled_float"
      },
      "trip_distance": {% raw %}{%- if trip_distance_mapping is defined %} {{ trip_distance_mapping | tojson }} {%- else %}{% endraw %} {
        "scaling_factor": 100,
        "type": "scaled_float"
      }{% raw %}{%- endif %}{% endraw %},
      "pickup_location": {
        "type": "geo_point"
      }
    },
    "dynamic": "strict"
  }
}
```

<!-- vale off -->
## files.txt
<!-- vale on -->

`files.txt` 檔案列出儲存工作負載資料的檔案，這些資料通常儲存在壓縮的 JSON 檔案中。

<!-- vale off -->
## _operations 與 _test-procedures
<!-- vale on -->

為了讓工作負載更易於閱讀，`_operations` 和 `_test-procedures` 被分成兩個目錄。

`_operations` 目錄包含一個 `default.json` 檔案，其中列出測試程序可使用的所有受支援操作。部分工作負載（例如 `nyc_taxis`）包含額外的 `.json` 檔案，其中列出特定功能的操作，例如 `snapshot` 操作。下列 JSON 範例顯示 `nyc_taxis` 工作負載中的操作清單：

```json
    {
      "name": "index",
      "operation-type": "bulk",
      "bulk-size": {% raw %}{{bulk_size | default(10000)}}{% endraw %},
      "ingest-percentage": {% raw %}{{ingest_percentage | default(100)}}{% endraw %}
    },
    {
      "name": "update",
      "operation-type": "bulk",
      "bulk-size": {% raw %}{{bulk_size | default(10000)}},
      "ingest-percentage": {{ingest_percentage | default(100)}},
      "conflicts": "{{conflicts | default('random')}}",
      "on-conflict": "{{on_conflict | default('update')}}",
      "conflict-probability": {{conflict_probability | default(25)}},
      "recency": {{recency | default(0)}}{% endraw %}
    },
    {
      "name": "wait-until-merges-finish",
      "operation-type": "index-stats",
      "index": "_all",
      "condition": {
        "path": "_all.total.merges.current",
        "expected-value": 0
      },
      "retry-until-success": true,
      "include-in-reporting": false
    },
    {
      "name": "default",
      "operation-type": "search",
      "body": {
        "query": {
          "match_all": {}
        }
      }
    },
    {
      "name": "range",
      "operation-type": "search",
      "body": {
        "query": {
          "range": {
            "total_amount": {
              "gte": 5,
              "lt": 15
            }
          }
        }
      }
    },
    {
      "name": "distance_amount_agg",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "bool": {
            "filter": {
              "range": {
                "trip_distance": {
                  "lt": 50,
                  "gte": 0
                }
              }
            }
          }
        },
        "aggs": {
          "distance_histo": {
            "histogram": {
              "field": "trip_distance",
              "interval": 1
            },
            "aggs": {
              "total_amount_stats": {
                "stats": {
                  "field": "total_amount"
                }
              }
            }
          }
        }
      }
    },
    {
      "name": "autohisto_agg",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "01/01/2015",
              "lte": "21/01/2015",
              "format": "dd/MM/yyyy"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "auto_date_histogram": {
              "field": "dropoff_datetime",
              "buckets": 20
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_agg",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
              "dropoff_datetime": {
              "gte": "01/01/2015",
              "lte": "21/01/2015",
              "format": "dd/MM/yyyy"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "calendar_interval": "day"
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_calendar_interval",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "calendar_interval": "month"
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_calendar_interval_with_tz",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "calendar_interval": "month",
              "time_zone": "America/New_York"
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_fixed_interval",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "fixed_interval": "60d"
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_fixed_interval_with_tz",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "fixed_interval": "60d",
              "time_zone": "America/New_York"
            }
          }
        }
      }
    },
    {
      "name": "date_histogram_fixed_interval_with_metrics",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "date_histogram": {
              "field": "dropoff_datetime",
              "fixed_interval": "60d"
            },
            "aggs": {
              "total_amount": { "stats": { "field": "total_amount" } },
              "tip_amount": { "stats": { "field": "tip_amount" } },
              "trip_distance": { "stats": { "field": "trip_distance" } }
            }
          }
        }
      }
    },
    {
      "name": "auto_date_histogram",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "auto_date_histogram": {
              "field": "dropoff_datetime",
              "buckets": "12"
            }
          }
        }
      }
    },
    {
      "name": "auto_date_histogram_with_tz",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "auto_date_histogram": {
              "field": "dropoff_datetime",
              "buckets": "13",
              "time_zone": "America/New_York"
            }
          }
        }
      }
    },
    {
      "name": "auto_date_histogram_with_metrics",
      "operation-type": "search",
      "body": {
        "size": 0,
        "query": {
          "range": {
            "dropoff_datetime": {
              "gte": "2015-01-01 00:00:00",
              "lt": "2016-01-01 00:00:00"
            }
          }
        },
        "aggs": {
          "dropoffs_over_time": {
            "auto_date_histogram": {
              "field": "dropoff_datetime",
              "buckets": "12"
            },
            "aggs": {
              "total_amount": { "stats": { "field": "total_amount" } },
              "tip_amount": { "stats": { "field": "tip_amount" } },
              "trip_distance": { "stats": { "field": "trip_distance" } }
            }
          }
        }
      }
    },
    {
      "name": "desc_sort_tip_amount",
      "operation-type": "search",
      "index": "nyc_taxis",
      "body": {
        "query": {
          "match_all": {}
        },
        "sort" : [
          {"tip_amount" : "desc"}
        ]
      }
    },
    {
      "name": "asc_sort_tip_amount",
      "operation-type": "search",
      "index": "nyc_taxis",
      "body": {
        "query": {
          "match_all": {}
        },
        "sort" : [
          {"tip_amount" : "asc"}
        ]
      }
    }
```

`_test-procedures` 目錄包含一個 `default.json` 檔案，用來設定工作負載執行的操作順序。與 `_operations` 目錄類似，`_test-procedures` 目錄也可以包含特定功能的測試程序，例如用於 `nyc_taxis` 的 `searchable_snapshots.json`。下列範例顯示 `nyc_taxis` 的可搜尋快照測試程序：

```json
 {
      "name": "searchable-snapshot",
      "description": "Measuring performance for Searchable Snapshot feature. Based on the default test procedure 'append-no-conflicts'.",
      "schedule": [
        {
          "operation": "delete-index"
        },
        {
          "operation": {
            "operation-type": "create-index",
            "settings": {% raw %}{%- if index_settings is defined %} {{ index_settings | tojson }} {%- else %}{
              "index.codec": "best_compression",
              "index.refresh_interval": "30s",
              "index.translog.flush_threshold_size": "4g"
            }{%- endif %}{% endraw %}
          }
        },
        {
          "name": "check-cluster-health",
          "operation": {
            "operation-type": "cluster-health",
            "index": "nyc_taxis",
            "request-params": {
              "wait_for_status": {% raw %}"{{ cluster_health | default('green') }}"{% endraw %},
              "wait_for_no_relocating_shards": "true"
            },
            "retry-until-success": true
          }
        },
        {
          "operation": "index",
          "warmup-time-period": 240,
          "clients": {% raw %}{{ bulk_indexing_clients | default(8) }},
          "ignore-response-error-level": "{{ error_level | default('non-fatal') }}"{% endraw %}
        },
        {
          "name": "refresh-after-index",
          "operation": "refresh"
        },
        {
          "operation": {
            "operation-type": "force-merge",
            "request-timeout": 7200
            {% raw %}{%- if force_merge_max_num_segments is defined %}{% endraw %},
            "max-num-segments": {% raw %}{{ force_merge_max_num_segments | tojson }}{% endraw %}
            {% raw %}{%- endif %}{% endraw %}
          }
        },
        {
          "name": "refresh-after-force-merge",
          "operation": "refresh"
        },
        {
          "operation": "wait-until-merges-finish"
        },
        {
          "operation": "create-snapshot-repository"
        },
        {
          "operation": "delete-snapshot"
        },
        {
          "operation": "create-snapshot"
        },
        {
          "operation": "wait-for-snapshot-creation"
        },
        {
          "operation": {
            "name": "delete-local-index",
            "operation-type": "delete-index"
          }
        },
        {
          "operation": "restore-snapshot"
        },
        {
          "operation": "default",
          "warmup-iterations": 50,
          "iterations": 100
          {% raw %}{%- if not target_throughput %}{% endraw %}
          ,"target-throughput": 3
          {% raw %}{%- elif target_throughput is string and target_throughput.lower() == 'none' %}{% endraw %}
          {% raw %}{%- else %}{% endraw %}
          ,"target-throughput": {% raw %}{{ target_throughput | tojson }}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
          {% raw %}{%-if search_clients is defined and search_clients %}{% endraw %}
          ,"clients": {% raw %}{{ search_clients | tojson}}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
        },
        {
          "operation": "range",
          "warmup-iterations": 50,
          "iterations": 100
          {% raw %}{%- if not target_throughput %}{% endraw %}
          ,"target-throughput": 0.7
          {% raw %}{%- elif target_throughput is string and target_throughput.lower() == 'none' %}{% endraw %}
          {% raw %}{%- else %}{% endraw %}
          ,"target-throughput": {% raw %}{{ target_throughput | tojson }}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
          {% raw %}{%-if search_clients is defined and search_clients %}{% endraw %}
          ,"clients": {% raw %}{{ search_clients | tojson}}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
        },
        {
          "operation": "distance_amount_agg",
          "warmup-iterations": 50,
          "iterations": 50
          {% raw %}{%- if not target_throughput %}{% endraw %}
          ,"target-throughput": 2
          {% raw %}{%- elif target_throughput is string and target_throughput.lower() == 'none' %}{% endraw %}
          {% raw %}{%- else %}{% endraw %}
          ,"target-throughput": {% raw %}{{ target_throughput | tojson }}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
          {% raw %}{%-if search_clients is defined and search_clients %}{% endraw %}
          ,"clients": {% raw %}{{ search_clients | tojson}}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
        },
        {
          "operation": "autohisto_agg",
          "warmup-iterations": 50,
          "iterations": 100
          {% raw %}{%- if not target_throughput %}{% endraw %}
          ,"target-throughput": 1.5
          {% raw %}{%- elif target_throughput is string and target_throughput.lower() == 'none' %}{% endraw %}
          {% raw %}{%- else %}{% endraw %}
          ,"target-throughput": {% raw %}{{ target_throughput | tojson }}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
          {% raw %}{%-if search_clients is defined and search_clients %}{% endraw %}
          ,"clients": {% raw %}{{ search_clients | tojson}}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
        },
        {
          "operation": "date_histogram_agg",
          "warmup-iterations": 50,
          "iterations": 100
          {% raw %}{%- if not target_throughput %}{% endraw %}
          ,"target-throughput": 1.5
          {% raw %}{%- elif target_throughput is string and target_throughput.lower() == 'none' %}{% endraw %}
          {% raw %}{%- else %}{% endraw %}
          ,"target-throughput": {% raw %}{{ target_throughput | tojson }}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
          {% raw %}{%-if search_clients is defined and search_clients %}{% endraw %}
          ,"clients": {% raw %}{{ search_clients | tojson}}{% endraw %}
          {% raw %}{%- endif %}{% endraw %}
        }
      ]
    }
```

## 工作負載範例

下列範例展示完整的 `workload.json` 檔案，您可以依自己的工作負載加以調整。

### 不限速執行

在下列範例中，OpenSearch Benchmark 針對 `movies` 索引執行不限速的大量索引操作，持續 1 小時：

```json
{
  "description": "Tutorial benchmark for OpenSearch Benchmark",
  "indices": [
    {
      "name": "movies",
      "body": "index.json"
    }
  ],
  "corpora": [
    {
      "name": "movies",
      "documents": [
        {
          "source-file": "movies-documents.json",
          "document-count": 11658903, # Fetch document count from command line
          "uncompressed-bytes": 1544799789 # Fetch uncompressed bytes from command line
        }
      ]
    }
  ],
  "schedule": [
  {
    "operation": "bulk",
    "warmup-time-period": 120,
    "time-period": 3600,
    "clients": 8
  }
]
}
```

### 單一工作的工作負載

下列工作負載以單一工作執行基準測試：一個 `match_all` 查詢。由於未指定 `clients`，因此只使用一個用戶端。根據 [`schedule`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/schedule/)，此工作負載以每秒 10 個操作、1 個用戶端執行 `match_all` 查詢，使用前 100 次迭代暖機，並使用接下來的 100 次迭代測量基準測試結果：

```json
{
  "description": "Tutorial benchmark for OpenSearch Benchmark",
  "indices": [
    {
      "name": "movies",
      "body": "index.json"
    }
  ],
  "corpora": [
    {
      "name": "movies",
      "documents": [
        {
          "source-file": "movies-documents.json",
          "document-count": 11658903, # Fetch document count from command line
          "uncompressed-bytes": 1544799789 # Fetch uncompressed bytes from command line
        }
      ]
    }
  ],
  "schedule": [
    {
      "operation": {
        "operation-type": "search",
        "index": "_all",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "warmup-iterations": 100,
      "iterations": 100,
      "target-throughput": 10
    }
  ]
}
```

## 後續步驟

- 如需了解各個預先封裝工作負載的資料、叢集需求和查詢類型，請參閱[工作負載類型]({{site.url}}{{site.baseurl}}/benchmark/workload-types/)。
- 如需了解如何建立您自己的工作負載，請參閱[建立自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)。
