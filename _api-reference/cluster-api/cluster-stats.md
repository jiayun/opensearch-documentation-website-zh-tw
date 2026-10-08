---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集統計"
nav_order: 60
parent: Cluster APIs
has_children: false
redirect_from:
  - /api-reference/cluster-stats/
  - /opensearch/rest-api/cluster-stats/
---

# Cluster Stats API
**1.0 版新增**
{: .label .label-purple }

Cluster Stats API 會傳回叢集的高階統計資訊，包括分片數量、儲存空間大小與記憶體使用量等關鍵索引指標。此外，它還提供叢集節點的詳細資訊，包括節點數量、節點角色、作業系統、JVM 版本、資源使用情況（記憶體與 CPU）以及已安裝的外掛程式。

<!-- spec_insert_start
api: cluster.stats
component: endpoints
-->
## 端點
```json
GET /_cluster/stats
GET /_cluster/stats/nodes/{node_id}
GET /_cluster/stats/{metric}/nodes/{node_id}
GET /_cluster/stats/{metric}/{index_metric}/nodes/{node_id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cluster.stats
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index_metric` | List | 以逗號分隔的[索引指標群組]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-stats/#index-metric-groups)清單，例如 `docs,store`。 |
| `metric` | List | 將傳回的資訊限制為指定的指標。 |
| `node_id` | List or String | 以逗號分隔的節點 ID 清單，用於篩選結果。支援[節點篩選器]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。 |

<!-- spec_insert_end -->

雖然 `master` 一詞在 OpenSearch 2.0 之後已被 `cluster_manager` 取代而棄用，但 `master` 欄位仍為了回溯相容性而保留。如果您的節點具有 `master` 角色或 `cluster_manager` 角色，則 `count` 會為這兩個欄位各增加 1。關於節點數量增加的範例，請參閱[範例回應](#example-response)。
{: .note }

<!-- spec_insert_start
api: cluster.stats
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `flat_settings` | Boolean | 是否以扁平形式傳回設定，這可提升可讀性，特別是對於深度巢狀的設定。例如，`"cluster": { "max_shards_per_node": 500 }` 的扁平形式為 `"cluster.max_shards_per_node": "500"`。_(預設：`false`)_ |
| `timeout` | String | 等待每個節點回應的時間量。如果節點在其逾時時間到期前未回應，回應將不包含其統計資訊。不過，逾時的節點仍會包含在回應的 `_nodes.failed` 屬性中。預設為不逾時。 |

<!-- spec_insert_end -->

### 指標群組

下表列出所有可用的指標群組。

Metric | 說明
:--- |:----
`indices` | 叢集中索引的統計資訊。
`os` | 作業系統的統計資訊，包括負載與記憶體。
`process` | 程序的統計資訊，包括開啟的檔案描述元與 CPU 使用量。
`jvm` | JVM 的統計資訊，包括堆積使用量與執行緒。
`fs` | 檔案系統使用情況的統計資訊。
`plugins` | 與節點整合的 OpenSearch 外掛程式的統計資訊。
`network_types` | 連接到節點的傳輸與 HTTP 網路的統計資訊。
`discovery_type` | 節點用來尋找叢集中其他節點的探索方法的統計資訊。
`packaging_types` | 每個節點的 OpenSearch 發行版本的統計資訊。
`ingest` | 資料匯入管線的統計資訊。

### 索引指標群組

若要篩選 `indices` 指標所傳回的資訊，您可以使用特定的 `index_metric` 值。這些值僅在使用下列查詢類型時受支援：

```json
GET _cluster/stats/_all/{index_metric}/nodes/{node_id}
GET _cluster/stats/indices/{index_metric}/nodes/{node_id}
```

支援下列索引指標：

- `shards`
- `docs`
- `store`
- `fielddata`
- `query_cache`
- `completion`
- `segments`
- `mappings`
- `analysis`

## 範例請求：擷取特定索引指標

下列範例請求會擷取所有節點的 `docs` 與 `segments` 索引指標的統計資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/stats/indices/docs,segments/nodes/_all
body: 
-->
{% capture step1_rest %}
GET /_cluster/stats/indices/docs,segments/nodes/_all

{% endcapture %}

{% capture step1_python %}


response = client.cluster.stats(
  index_metric = "docs,segments",
  metric = "indices",
  node_id = "_all"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：擷取特定節點的統計資訊

下列範例請求會傳回叢集管理員節點的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/stats/nodes/_cluster_manager
body: 
-->
{% capture step1_rest %}
GET /_cluster/stats/nodes/_cluster_manager

{% endcapture %}

{% capture step1_python %}


response = client.cluster.stats(
  node_id = "_cluster_manager"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：使用人類可讀的輸出

下列範例請求包含 `human` 查詢參數，以人類可讀的格式傳回位元組與大小值：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/stats?human&pretty
-->
{% capture step1_rest %}
GET /_cluster/stats?human&pretty
{% endcapture %}

{% capture step1_python %}


response = client.cluster.stats(
  params = { "human": "true", "pretty": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

`human` 參數會在回應中新增人類可讀的欄位，同時保留原始數值。例如，`jvm.max_uptime_in_millis` 欄位在預設回應中只顯示數值：

```json
"jvm": {
    "max_uptime_in_millis": 21476787
}
```

當您包含 `human` 參數時，回應會同時包含人類可讀的 `max_uptime` 欄位與原始數值欄位：

```json
"jvm": {
    "max_uptime": "5.9h",
    "max_uptime_in_millis": 21480995
}
```

## 範例回應

<details open markdown="block">
  <summary>
    Response
  </summary>
  {: .text-delta}

```json
{
    "_nodes": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "cluster_name": "opensearch-cluster",
    "cluster_uuid": "QravFieJS_SlZJyBMcDMqQ",
    "timestamp": 1644607845054,
    "status": "yellow",
    "indices": {
        "count": 114,
        "shards": {
            "total": 121,
            "primaries": 60,
            "replication": 1.0166666666666666,
            "index": {
                "shards": {
                    "min": 1,
                    "max": 2,
                    "avg": 1.0614035087719298
                },
                "primaries": {
                    "min": 0,
                    "max": 2,
                    "avg": 0.5263157894736842
                },
                "replication": {
                    "min": 0.0,
                    "max": 1.0,
                    "avg": 0.008771929824561403
                }
            }
        },
        "docs": {
            "count": 134263,
            "deleted": 115
        },
        "store": {
            "size_in_bytes": 70466547,
            "reserved_in_bytes": 0
        },
        "fielddata": {
            "memory_size_in_bytes": 664,
            "evictions": 0,
            "item_count": 1
        },
        "query_cache": {
            "memory_size_in_bytes": 0,
            "total_count": 1,
            "hit_count": 0,
            "miss_count": 1,
            "cache_size": 0,
            "cache_count": 0,
            "evictions": 0
        },
        "completion": {
            "size_in_bytes": 0
        },
        "segments": {
            "count": 341,
            "memory_in_bytes": 3137244,
            "terms_memory_in_bytes": 2488992,
            "stored_fields_memory_in_bytes": 167672,
            "term_vectors_memory_in_bytes": 0,
            "norms_memory_in_bytes": 346816,
            "points_memory_in_bytes": 0,
            "doc_values_memory_in_bytes": 133764,
            "index_writer_memory_in_bytes": 0,
            "version_map_memory_in_bytes": 0,
            "fixed_bit_set_memory_in_bytes": 1112,
            "max_unsafe_auto_id_timestamp": 1644269449096,
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
        "mappings": {
            "field_types": [
                {
                    "name": "alias",
                    "count": 1,
                    "index_count": 1
                },
                {
                    "name": "binary",
                    "count": 1,
                    "index_count": 1
                },
                {
                    "name": "boolean",
                    "count": 87,
                    "index_count": 22
                },
                {
                    "name": "date",
                    "count": 185,
                    "index_count": 91
                },
                {
                    "name": "double",
                    "count": 5,
                    "index_count": 2
                },
                {
                    "name": "float",
                    "count": 4,
                    "index_count": 1
                },
                {
                    "name": "geo_point",
                    "count": 4,
                    "index_count": 3
                },
                {
                    "name": "half_float",
                    "count": 12,
                    "index_count": 1
                },
                {
                    "name": "integer",
                    "count": 144,
                    "index_count": 29
                },
                {
                    "name": "ip",
                    "count": 2,
                    "index_count": 1
                },
                {
                    "name": "keyword",
                    "count": 1939,
                    "index_count": 109
                },
                {
                    "name": "knn_vector",
                    "count": 1,
                    "index_count": 1
                },
                {
                    "name": "long",
                    "count": 158,
                    "index_count": 92
                },
                {
                    "name": "nested",
                    "count": 25,
                    "index_count": 10
                },
                {
                    "name": "object",
                    "count": 420,
                    "index_count": 91
                },
                {
                    "name": "text",
                    "count": 1768,
                    "index_count": 102
                }
            ]
        },
        "analysis": {
            "char_filter_types": [],
            "tokenizer_types": [],
            "filter_types": [],
            "analyzer_types": [],
            "built_in_char_filters": [],
            "built_in_tokenizers": [],
            "built_in_filters": [],
            "built_in_analyzers": [
                {
                    "name": "english",
                    "count": 1,
                    "index_count": 1
                }
            ]
        }
    },
    "nodes": {
        "count": {
            "total": 1,
            "coordinating_only": 0,
            "data": 1,
            "ingest": 1,
            "master": 1,
            "cluster_manager": 1,
            "remote_cluster_client": 1
        },
        "versions": [
            "1.2.4"
        ],
        "os": {
            "available_processors": 6,
            "allocated_processors": 6,
            "names": [
                {
                    "name": "Linux",
                    "count": 1
                }
            ],
            "pretty_names": [
                {
                    "pretty_name": "Amazon Linux 2",
                    "count": 1
                }
            ],
            "mem": {
                "total_in_bytes": 6232674304,
                "free_in_bytes": 1452658688,
                "used_in_bytes": 4780015616,
                "free_percent": 23,
                "used_percent": 77
            }
        },
        "process": {
            "cpu": {
                "percent": 0
            },
            "open_file_descriptors": {
                "min": 970,
                "max": 970,
                "avg": 970
            }
        },
        "jvm": {
            "max_uptime_in_millis": 108800629,
            "versions": [
                {
                    "version": "15.0.1",
                    "vm_name": "OpenJDK 64-Bit Server VM",
                    "vm_version": "15.0.1+9",
                    "vm_vendor": "AdoptOpenJDK",
                    "bundled_jdk": true,
                    "using_bundled_jdk": true,
                    "count": 1
                }
            ],
            "mem": {
                "heap_used_in_bytes": 178956256,
                "heap_max_in_bytes": 536870912
            },
            "threads": 112
        },
        "fs": {
            "total_in_bytes": 62725623808,
            "free_in_bytes": 28442726400,
            "available_in_bytes": 25226010624
        },
        "plugins": [
            {
                "name": "opensearch-index-management",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch Index Management Plugin",
                "classname": "org.opensearch.indexmanagement.IndexManagementPlugin",
                "custom_foldername": "",
                "extended_plugins": [
                    "opensearch-job-scheduler"
                ],
                "has_native_controller": false
            },
            {
                "name": "opensearch-security",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "Provide access control related features for OpenSearch 1.0.0",
                "classname": "org.opensearch.security.OpenSearchSecurityPlugin",
                "custom_foldername": "opensearch-security",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-cross-cluster-replication",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch Cross Cluster Replication Plugin",
                "classname": "org.opensearch.replication.ReplicationPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-job-scheduler",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch Job Scheduler plugin",
                "classname": "org.opensearch.jobscheduler.JobSchedulerPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-anomaly-detection",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch anomaly detector plugin",
                "classname": "org.opensearch.ad.AnomalyDetectorPlugin",
                "custom_foldername": "",
                "extended_plugins": [
                    "lang-painless",
                    "opensearch-job-scheduler"
                ],
                "has_native_controller": false
            },
            {
                "name": "opensearch-performance-analyzer",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch Performance Analyzer Plugin",
                "classname": "org.opensearch.performanceanalyzer.PerformanceAnalyzerPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-reports-scheduler",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "Scheduler for Dashboards Reports Plugin",
                "classname": "org.opensearch.reportsscheduler.ReportsSchedulerPlugin",
                "custom_foldername": "",
                "extended_plugins": [
                    "opensearch-job-scheduler"
                ],
                "has_native_controller": false
            },
            {
                "name": "opensearch-asynchronous-search",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "Provides support for asynchronous search",
                "classname": "org.opensearch.search.asynchronous.plugin.AsynchronousSearchPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-knn",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch k-NN plugin",
                "classname": "org.opensearch.knn.plugin.KNNPlugin",
                "custom_foldername": "",
                "extended_plugins": [
                    "lang-painless"
                ],
                "has_native_controller": false
            },
            {
                "name": "opensearch-alerting",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "Amazon OpenSearch alerting plugin",
                "classname": "org.opensearch.alerting.AlertingPlugin",
                "custom_foldername": "",
                "extended_plugins": [
                    "lang-painless"
                ],
                "has_native_controller": false
            },
            {
                "name": "opensearch-observability",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch Plugin for OpenSearch Dashboards Observability",
                "classname": "org.opensearch.observability.ObservabilityPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            },
            {
                "name": "opensearch-sql",
                "version": "1.2.4.0",
                "opensearch_version": "1.2.4",
                "java_version": "1.8",
                "description": "OpenSearch SQL",
                "classname": "org.opensearch.sql.plugin.SQLPlugin",
                "custom_foldername": "",
                "extended_plugins": [],
                "has_native_controller": false
            }
        ],
        "network_types": {
            "transport_types": {
                "org.opensearch.security.ssl.http.netty.SecuritySSLNettyTransport": 1
            },
            "http_types": {
                "org.opensearch.security.http.SecurityHttpServerTransport": 1
            }
        },
        "discovery_types": {
            "zen": 1
        },
        "packaging_types": [
            {
                "type": "tar",
                "count": 1
            }
        ],
        "ingest": {
            "number_of_pipelines": 0,
            "processor_stats": {}
        }
    }
}
```
</details>

## 回應本文欄位

下表列出回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_nodes` | Object | 提供節點層級請求結果的摘要。
`_nodes.total` | Integer | 請求中包含的節點總數。
`_nodes.successful` | Integer | 成功處理請求的節點數。
`_nodes.failed` | Integer | 未能回應或拒絕請求的節點數。若非零，回應中會包含失敗詳細資料。
`cluster_name` | String | 叢集的名稱。
`cluster_uuid` | String | 叢集的唯一識別碼。
`timestamp` | Long | 叢集統計資料上次更新的時間，以自 epoch 起算的毫秒數表示。
`status` | String | 叢集健康狀態：`green`、`yellow` 或 `red`。
`indices` | Object | 在指定節點上具有分片的索引的彙總統計資料。
`indices.count` | Integer | 在指定節點上具有分片的索引總數。
`indices.shards` | Object | 指定節點的分片彙總統計資料。
`indices.shards.total` | Integer | 指定節點上的分片總數。
`indices.shards.primaries` | Integer | 指定節點上的主要分片數。
`indices.shards.replication` | Float | 指定節點上副本分片與主要分片的比例。
`indices.shards.index.shards.min` | Integer | 每個索引的最小分片數 (僅計入指定節點上的分片)。
`indices.shards.index.shards.max` | Integer | 每個索引的最大分片數 (僅計入指定節點上的分片)。
`indices.shards.index.shards.avg` | Float | 每個索引的平均分片數 (僅計入指定節點上的分片)。
`indices.shards.index.primaries.min` | Integer | 每個索引的最小主要分片數 (僅計入指定節點上的分片)。
`indices.shards.index.primaries.max` | Integer | 每個索引的最大主要分片數 (僅計入指定節點上的分片)。
`indices.shards.index.primaries.avg` | Float | 每個索引的平均主要分片數 (僅計入指定節點上的分片)。
`indices.shards.index.replication.min` | Float | 每個索引的最小複寫因子 (僅計入指定節點上的分片)。
`indices.shards.index.replication.max` | Float | 每個索引的最大複寫因子 (僅計入指定節點上的分片)。
`indices.shards.index.replication.avg` | Float | 每個索引的平均複寫因子 (僅計入指定節點上的分片)。
`indices.docs` | Object | 指定節點的文件統計資料。
`indices.docs.count` | Integer | 指定節點上所有主要分片中未刪除文件的總數。包含 Lucene 區段中的文件，且可能計入巢狀文件。
`indices.docs.deleted` | Integer | 指定節點上所有主要分片中已刪除文件的總數。磁碟空間會在區段合併期間回收。
`indices.store.size_in_bytes` | Long | 指定節點上所有分片的總儲存空間大小，以位元組為單位。
`indices.store.reserved_in_bytes` | Long | 為進行中的作業 (例如區段合併) 保留的磁碟空間量，以位元組為單位。
`indices.fielddata.memory_size_in_bytes` | Long | 指定節點上欄位資料快取所使用的記憶體總量，以位元組為單位。
`indices.fielddata.evictions` | Long | 指定節點上欄位資料快取的逐出次數。
`indices.query_cache.memory_size_in_bytes` | Long | 指定節點上查詢快取所使用的記憶體總量，以位元組為單位。
`indices.query_cache.total_count` | Long | 指定節點上查詢快取的存取總次數 (命中與未命中)。
`indices.query_cache.hit_count` | Long | 指定節點上查詢快取的命中次數。
`indices.query_cache.miss_count` | Long | 指定節點上查詢快取的未命中次數。
`indices.query_cache.cache_size` | Integer | 指定節點上查詢快取目前的項目數。
`indices.query_cache.cache_count` | Long | 新增至查詢快取的項目總數，包含已逐出的項目。
`indices.query_cache.evictions` | Long | 指定節點上查詢快取的逐出次數。
`indices.completion.size_in_bytes` | Long | 指定節點上用於自動完成建議器的記憶體總量，以位元組為單位。
`indices.segments` | Object | 指定節點的區段統計資料。
`indices.segments.count` | Integer | 指定節點上所有分片的區段總數。
`indices.segments.memory_in_bytes` | Long | 指定節點上區段所使用的記憶體總量，以位元組為單位。
`indices.segments.terms_memory_in_bytes` | Long | 指定節點上用於詞典的記憶體量，以位元組為單位。
`indices.segments.stored_fields_memory_in_bytes` | Long | 指定節點上用於已儲存欄位的記憶體量，以位元組為單位。
`indices.segments.term_vectors_memory_in_bytes` | Long | 指定節點上用於詞向量的記憶體量，以位元組為單位。
`indices.segments.norms_memory_in_bytes` | Long | 指定節點上用於正規化因子的記憶體量，以位元組為單位。
`indices.segments.points_memory_in_bytes` | Long | 指定節點上用於點值 (數值或地理) 的記憶體量，以位元組為單位。
`indices.segments.doc_values_memory_in_bytes` | Long | 指定節點上用於 doc values 的記憶體量，以位元組為單位。
`indices.segments.index_writer_memory_in_bytes` | Long | 指定節點上索引寫入器所使用的記憶體量，以位元組為單位。
`indices.segments.version_map_memory_in_bytes` | Long | 指定節點上版本對應所使用的記憶體量，以位元組為單位。
`indices.segments.fixed_bit_set_memory_in_bytes` | Long | 指定節點上固定位元集 (用於巢狀與 join 欄位) 所使用的記憶體量，以位元組為單位。
`indices.segments.max_unsafe_auto_id_timestamp` | Long | 重試的索引請求最近一次的時間戳記，以毫秒為單位。
`indices.segments.file_sizes` | Object | Cluster Stats API 不會填入此物件。若要取得區段檔案的相關資訊，請使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)。
`indices.mappings.field_types` | Array | 指定節點上所用欄位資料類型的相關統計資料。
`indices.mappings.field_types.name` | String | 欄位資料類型。
`indices.mappings.field_types.count` | Integer | 對應至此資料類型的欄位數。
`indices.mappings.field_types.index_count` | Integer | 使用此資料類型的索引數。
`indices.analysis` | Object | 指定節點上所用分析器與分析元件的相關統計資料。
`nodes` | Object | 指定節點的彙總統計資料。
`nodes.count.total` | Integer | 節點總數。
`nodes.count.coordinating_only` | Integer | 未指派角色的節點數 (僅協調節點)。
`nodes.count.<role>` | Integer | 具有特定角色的節點數 (例如 `data`、`ingest`、`cluster_manager`)。
`nodes.versions` | Array | 指定節點上執行的 OpenSearch 版本。
`nodes.os.available_processors` | Integer | 指定節點上可供 JVM 使用的處理器總數。
`nodes.os.allocated_processors` | Integer | 指定節點上用於決定執行緒集區大小的處理器數 (上限為 32)。
`nodes.os.mem.total_in_bytes` | Long | 指定節點上的實體記憶體總量，以位元組為單位。
`nodes.os.mem.free_in_bytes` | Long | 指定節點上的可用實體記憶體量，以位元組為單位。
`nodes.os.mem.used_in_bytes` | Long | 指定節點上已使用的實體記憶體量，以位元組為單位。
`nodes.os.mem.free_percent` | Integer | 指定節點上可用實體記憶體的百分比。
`nodes.os.mem.used_percent` | Integer | 指定節點上已使用實體記憶體的百分比。
`nodes.process.cpu.percent` | Integer | 指定節點上的 CPU 使用率百分比。若不支援，則傳回 `-1`。
`nodes.process.open_file_descriptors.min` | Integer | 指定節點上開啟檔案描述元的最小數量。若不支援，則傳回 `-1`。
`nodes.process.open_file_descriptors.max` | Integer | 指定節點上開啟檔案描述元的最大數量。若不支援，則傳回 `-1`。
`nodes.process.open_file_descriptors.avg` | Integer | 指定節點上開啟檔案描述元的平均數量。若不支援，則傳回 `-1`。
`nodes.jvm.max_uptime_in_millis` | Long | 指定節點上 JVM 的最長運作時間，以毫秒為單位。
`nodes.jvm.versions` | Array | 指定節點上執行之 JVM 版本的相關統計資料。
`nodes.jvm.mem.heap_used_in_bytes` | Long | 指定節點上目前使用中的堆積記憶體，以位元組為單位。
`nodes.jvm.mem.heap_max_in_bytes` | Long | 指定節點上可用的最大堆積記憶體，以位元組為單位。
`nodes.jvm.threads` | Integer | 指定節點上作用中 JVM 執行緒的總數。
`nodes.fs.total_in_bytes` | Long | 指定節點上的檔案系統總容量，以位元組為單位。
`nodes.fs.free_in_bytes` | Long | 指定節點上未配置的磁碟空間總量，以位元組為單位。
`nodes.fs.available_in_bytes` | Long | 指定節點上可供 JVM 使用的磁碟空間 (可能因作業系統限制而少於可用空間)，以位元組為單位。
`nodes.plugins` | Array | 指定節點上已安裝外掛程式與模組的相關資訊。
`nodes.network_types` | Object | 指定節點所使用之傳輸與 HTTP 網路類型的相關統計資料。
`nodes.discovery_types` | Object | 指定節點所使用之探索機制的相關統計資料。
`nodes.packaging_types` | Array | 指定節點上已安裝發行版類型的相關資訊。
`nodes.ingest.number_of_pipelines` | Integer | 指定節點上資料匯入管線的總數。
`nodes.ingest.processor_stats` | Object | 指定節點上所用資料匯入處理器的相關統計資料。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/stats`。
