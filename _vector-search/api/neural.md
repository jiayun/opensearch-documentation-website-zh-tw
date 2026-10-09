---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Neural Search API
parent: Vector search API
nav_order: 20
has_children: false
---

# Neural Search API

Neural Search 外掛程式提供多個 API，用於監視語意搜尋與混合搜尋功能。

## 統計

Neural Search Stats API 提供 Neural Search 外掛程式目前狀態的相關資訊。這包括叢集層級與節點層級的統計資料。叢集層級的統計資料在整個叢集中只有單一值。節點層級的統計資料在叢集中的每個節點各有一個值。

根據預設，Neural Search Stats API 會透過叢集設定停用。若要啟用統計資料收集，請使用下列命令：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.neural_search.stats_enabled": true
  }
}
```
{% include copy-curl.html %}

若要停用統計資料收集，請將叢集設定設為 `false`。停用時，所有值都會重設，且不會收集新的統計資料。

### 端點

```json
GET /_plugins/_neural/stats
GET /_plugins/_neural/stats/{stats}
GET /_plugins/_neural/{nodes}/stats
GET /_plugins/_neural/{nodes}/stats/{stats}
```

### 路徑參數

下表列出可用的路徑參數。所有路徑參數都是選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `nodes` | 字串 | 用來篩選統計資料的節點或節點清單 (以逗號分隔)。預設為所有節點。 |
| `stats` | 字串 | 要傳回的統計資料名稱，可為單一名稱或多個名稱 (以逗號分隔)。預設為所有統計資料。 |

### 查詢參數

下表列出可用的查詢參數。所有查詢參數都是選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `include_metadata` | 布林值 | 當 `true` 時，會為每項統計資料加入額外的中繼資料欄位 (請參閱[可用的中繼資料](#available-metadata))。預設為 `false`。 |
| `flat_stat_paths` | 布林值 | 當 `true` 時，會扁平化 JSON 回應結構，以便更容易解析。預設為 `false`。 |
| `include_individual_nodes` | 布林值 | 當 `true` 時，會包含 `nodes` 類別中各個節點的統計資料。當 `false` 時，會從回應中排除 `nodes` 類別。預設為 `true`。 |
| `include_all_nodes` | 布林值 | 當 `true` 時，會包含 `all_nodes` 類別中所有節點的彙總統計資料。當 `false` 時，會從回應中排除 `all_nodes` 類別。預設為 `true`。 |
| `include_info` | 布林值 | 當 `true` 時，會包含 `info` 類別中的叢集範圍資訊。當 `false` 時，會從回應中排除 `info` 類別。預設為 `true`。 |

#### 範例請求

```json
GET /_plugins/_neural/node1,node2/stats/stat1,stat2?include_metadata=true,flat_stat_paths=true
```
{% include copy-curl.html %}

#### 範例回應

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
GET /_plugins/_neural/stats/
{
	"_nodes": {
		"total": 1,
		"successful": 1,
		"failed": 0
	},
	"cluster_name": "integTest",
	"info": {
		"cluster_version": "3.1.0",
		"processors": {
			"search": {
				"hybrid": {
					"comb_geometric_processors": 0,
					"comb_rrf_processors": 0,
					"norm_l2_processors": 0,
					"norm_minmax_processors": 0,
					"comb_harmonic_processors": 0,
					"comb_arithmetic_processors": 0,
					"norm_zscore_processors": 0,
					"rank_based_normalization_processors": 0,
					"normalization_processors": 0
				},
				"rerank_ml_processors": 0,
				"rerank_by_field_processors": 0,
				"neural_sparse_two_phase_processors": 0,
				"neural_query_enricher_processors": 0
			},
			"ingest": {
				"sparse_encoding_processors": 0,
				"skip_existing_processors": 0,
				"text_image_embedding_processors": 0,
				"text_chunking_delimiter_processors": 0,
				"text_embedding_processors_in_pipelines": 0,
				"text_chunking_fixed_token_length_processors": 0,
				"text_chunking_fixed_char_length_processors": 0,
				"text_chunking_processors": 0
			}
		}
	},
	"all_nodes": {
		"query": {
			"hybrid": {
				"hybrid_query_with_pagination_requests": 0,
				"hybrid_query_with_filter_requests": 0,
				"hybrid_query_with_inner_hits_requests": 0,
				"hybrid_query_requests": 0
			},
			"neural": {
				"neural_query_against_semantic_sparse_requests": 0,
				"neural_query_requests": 0,
				"neural_query_against_semantic_dense_requests": 0,
				"neural_query_against_knn_requests": 0
			},
			"neural_sparse": {
				"neural_sparse_query_requests": 0,
                "seismic_query_requests": 0
			}
		},
		"semantic_highlighting": {
			"semantic_highlighting_request_count": 0,
			"semantic_highlighting_batch_request_count": 0
		},
		"processors": {
			"search": {
				"neural_sparse_two_phase_executions": 0,
				"hybrid": {
					"comb_harmonic_executions": 0,
					"norm_zscore_executions": 0,
					"comb_rrf_executions": 0,
					"norm_l2_executions": 0,
					"rank_based_normalization_processor_executions": 0,
					"comb_arithmetic_executions": 0,
					"normalization_processor_executions": 0,
					"comb_geometric_executions": 0,
					"norm_minmax_executions": 0
				},
				"rerank_by_field_executions": 0,
				"neural_query_enricher_executions": 0,
				"rerank_ml_executions": 0
			},
			"ingest": {
				"skip_existing_executions": 0,
				"text_chunking_fixed_token_length_executions": 0,
				"sparse_encoding_executions": 0,
				"text_chunking_fixed_char_length_executions": 0,
				"text_chunking_executions": 0,
				"text_embedding_executions": 0,
				"semantic_field_executions": 0,
				"semantic_field_chunking_executions": 0,
				"text_chunking_delimiter_executions": 0,
				"text_image_embedding_executions": 0
			}
		},
        "memory": {
            "sparse": {
                "sparse_memory_usage": 0.13,
                "clustered_posting_usage": 0.06,
                "forward_index_usage": 0.06
            }
        }
	},
	"nodes": {
		"_cONimhxS6KdedymRZr6xg": {
			"query": {
				"hybrid": {
					"hybrid_query_with_pagination_requests": 0,
					"hybrid_query_with_filter_requests": 0,
					"hybrid_query_with_inner_hits_requests": 0,
					"hybrid_query_requests": 0
				},
				"neural": {
					"neural_query_against_semantic_sparse_requests": 0,
					"neural_query_requests": 0,
					"neural_query_against_semantic_dense_requests": 0,
					"neural_query_against_knn_requests": 0
				},
				"neural_sparse": {
					"neural_sparse_query_requests": 0,
                    "seismic_query_requests": 0
				},
                "memory": {
                    "sparse": {
                        "sparse_memory_usage_percentage": 0,
                        "sparse_memory_usage": 0.13,
                        "clustered_posting_usage": 0.06,
                        "forward_index_usage": 0.06
                    }
                }
			},
			"semantic_highlighting": {
				"semantic_highlighting_request_count": 0,
				"semantic_highlighting_batch_request_count": 0
			},
			"processors": {
				"search": {
					"neural_sparse_two_phase_executions": 0,
					"hybrid": {
						"comb_harmonic_executions": 0,
						"norm_zscore_executions": 0,
						"comb_rrf_executions": 0,
						"norm_l2_executions": 0,
						"rank_based_normalization_processor_executions": 0,
						"comb_arithmetic_executions": 0,
						"normalization_processor_executions": 0,
						"comb_geometric_executions": 0,
						"norm_minmax_executions": 0
					},
					"rerank_by_field_executions": 0,
					"neural_query_enricher_executions": 0,
					"rerank_ml_executions": 0
				},
				"ingest": {
					"skip_existing_executions": 0,
					"text_chunking_fixed_token_length_executions": 0,
					"sparse_encoding_executions": 0,
					"text_chunking_fixed_char_length_executions": 0,
					"text_chunking_executions": 0,
					"text_embedding_executions": 0,
					"semantic_field_executions": 0,
					"semantic_field_chunking_executions": 0,
					"text_chunking_delimiter_executions": 0,
					"text_image_embedding_executions": 0
				}
			}
		}
	}
}
```

</details>

如果 `include_metadata` 為 `true`，則每個統計物件會包含額外的中繼資料：

```json
{
    ...,
    "text_embedding_executions": {
      "value": 0,
      "stat_type": "timestamped_event_counter",
      "trailing_interval_value": 0,
      "minutes_since_last_event": 29061801
    },
    ...
}
```

如需更多資訊，請參閱[可用的中繼資料](#available-metadata)。

### 回應本文欄位

以下各節說明回應本文欄位。

#### 統計資料類別

下表列出所有統計資料類別。

| 類別 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `info` | 物件 | 包含整個叢集的資訊，以及不針對個別節點的統計資料。 |
| `all_nodes` | 物件 | 提供叢集中所有節點的彙總統計資料。 |
| `nodes` | 物件 | 包含各節點的統計資料，每個節點皆以其唯一的節點 ID 識別。 |

#### 可用的統計資料

下表列出可用的統計資料。對於路徑以 `nodes.<node_id>` 為前綴的統計資料，也可在以 `all_nodes` 為前綴的相同路徑取得叢集層級的彙總統計資料。

| 統計資料名稱 | 類別 | 類別內的統計資料路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `cluster_version` | `info` | `cluster_version` | 叢集的版本。 |

**資訊統計資料：處理器**

| 統計資料名稱 | 類別 | 類別內的統計資料路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `text_embedding_processors_in_pipelines` | `info` | `processors.ingest.text_embedding_processors_in_pipelines` | 資料匯入管線中 `text_embedding` 處理器的數量。 |
| `sparse_encoding_processors` | `info` | `processors.ingest.sparse_encoding_processors` | 資料匯入管線中 `sparse_encoding` 處理器的數量。 |
| `skip_existing_processors` | `info` | `processors.ingest.skip_existing_processors` | 資料匯入管線中將 `skip_existing` 設為 `true` 的處理器數量。 |
| `text_image_embedding_processors` | `info` | `processors.ingest.text_image_embedding_processors` | 資料匯入管線中 `text_image_embedding` 處理器的數量。 |
| `text_chunking_delimiter_processors` | `info` | `processors.ingest.text_chunking_delimiter_processors` | 資料匯入管線中使用 `delimiter` 演算法的 `text_chunking` 處理器數量。 |
| `text_chunking_fixed_token_length_processors` | `info` | `processors.ingest.text_chunking_fixed_token_length_processors` | 資料匯入管線中使用 `fixed_token_length` 演算法的 `text_chunking` 處理器數量。 |
| `text_chunking_fixed_char_length_processors` | `info` | `processors.ingest.text_chunking_fixed_char_length_processors` | 資料匯入管線中使用 `fixed_character_length` 演算法的 `text_chunking` 處理器數量。 |
| `text_chunking_processors` | `info` | `processors.ingest.text_chunking_processors` | 資料匯入管線中 `text_chunking` 處理器的數量。 |
| `rerank_ml_processors` | `info` | `processors.search.rerank_ml_processors` | 搜尋管線中 `ml_opensearch` 類型的 `rerank` 處理器數量。 |
| `rerank_by_field_processors` | `info` | `processors.search.rerank_by_field_processors` | `by_field` 類型的 `rerank` 處理器數量。 |
| `neural_sparse_two_phase_processors` | `info` | `processors.search.neural_sparse_two_phase_processors` | 搜尋管線中 `neural_sparse_two_phase_processor` 處理器的數量。 |
| `neural_query_enricher_processors` | `info` | `processors.search.neural_query_enricher_processors` | 搜尋管線中 `neural_query_enricher` 處理器的數量。 |

**資訊統計資料：混合處理器**

| 統計資料名稱 | 類別 | 類別內的統計資料路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `normalization_processors` | `info` | `processors.search.hybrid.normalization_processors` | `normalization-processor` 處理器的數量。 |
| `norm_minmax_processors` | `info` | `processors.search.hybrid.norm_minmax_processors` | 將 `normalization.technique` 設為 `min_max` 的 `normalization-processor` 處理器數量。 |
| `norm_l2_processors` | `info` | `processors.search.hybrid.norm_l2_processors` | 將 `normalization.technique` 設為 `l2` 的 `normalization-processor` 處理器數量。 |
| `norm_zscore_processors` | `info` | `processors.search.hybrid.norm_zscore_processors` | 將 `normalization.technique` 設為 `z_score` 的 `normalization-processor` 處理器數量。 |
| `comb_arithmetic_processors` | `info` | `processors.search.hybrid.comb_arithmetic_processors` | 將 `combination.technique` 設為 `arithmetic_mean` 的 `normalization-processor` 處理器數量。 |
| `comb_geometric_processors` | `info` | `processors.search.hybrid.comb_geometric_processors` | 將 `combination.technique` 設為 `geometric_mean` 的 `normalization-processor` 處理器數量。 |
| `comb_harmonic_processors` | `info` | `processors.search.hybrid.comb_harmonic_processors` | 將 `combination.technique` 設為 `harmonic_mean` 的 `normalization-processor` 處理器數量。 |
| `rank_based_normalization_processors` | `info` | `processors.search.hybrid.rank_based_normalization_processors` | `score-ranker-processor` 處理器的數量。 |
| `comb_rrf_processors` | `info` | `processors.search.hybrid.comb_rrf_processors` | 將 `combination.technique` 設為 `rrf` 的 `score-ranker-processor` 處理器數量。 |

**節點層級統計資料：處理器**

| 統計資料名稱 | 類別 | 類別內的統計資料路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `text_embedding_executions` | `nodes`, `all_nodes` | `processors.ingest.text_embedding_executions` | `text_embedding` 處理器的執行次數。 |
| `skip_existing_executions` | `nodes`, `all_nodes` | `processors.ingest.skip_existing_executions` | 將 `skip_existing` 設為 `true` 的處理器執行次數。 |
| `text_chunking_fixed_token_length_executions` | `nodes`, `all_nodes` | `processors.ingest.text_chunking_fixed_token_length_executions` | 使用 `fixed_token_length` 演算法的 `text_chunking` 處理器執行次數。 |
| `sparse_encoding_executions` | `nodes`, `all_nodes` | `processors.ingest.sparse_encoding_executions` | `sparse_encoding` 處理器的執行次數。 |
| `text_chunking_fixed_char_length_executions` | `nodes`, `all_nodes` | `processors.ingest.text_chunking_fixed_char_length_executions` | 使用 `fixed_character_length` 演算法的 `text_chunking` 處理器執行次數。 |
| `text_chunking_executions` | `nodes`, `all_nodes` | `processors.ingest.text_chunking_executions` | `text_chunking` 處理器的執行次數。 |
| `semantic_field_executions` | `nodes`, `all_nodes` | `processors.ingest.semantic_field_executions` | `semantic` 欄位系統處理器的執行次數。 |
| `semantic_field_chunking_executions` | `nodes`, `all_nodes` | `processors.ingest.semantic_field_chunking_executions` | `semantic` 欄位系統分塊處理器的執行次數。 |
| `text_chunking_delimiter_executions` | `nodes`, `all_nodes` | `processors.ingest.text_chunking_delimiter_executions` | 使用 `delimiter` 演算法的 `text_chunking` 處理器執行次數。 |
| `text_image_embedding_executions` | `nodes`, `all_nodes` | `processors.ingest.text_image_embedding_executions` | `text_image_embedding` 處理器的執行次數。 |
| `neural_sparse_two_phase_executions` | `nodes`, `all_nodes` | `processors.search.neural_sparse_two_phase_executions` | `neural_sparse_two_phase_processor` 處理器的執行次數。 |
| `rerank_by_field_executions` | `nodes`, `all_nodes` | `processors.search.rerank_by_field_executions` | `by_field` 類型的 `rerank` 處理器執行次數。 |
| `neural_query_enricher_executions` | `nodes`, `all_nodes` | `processors.search.neural_query_enricher_executions` | `neural_query_enricher` 處理器的執行次數。 |
| `rerank_ml_executions` | `nodes`, `all_nodes` | `processors.search.rerank_ml_executions` | `ml_opensearch` 類型的 `rerank` 處理器執行次數。 |

**節點層級統計資料：混合處理器**

| 統計資料名稱 | 類別 | 類別內的統計資料路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `normalization_processor_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.normalization_processor_executions` | `normalization-processor` 處理器的執行次數。 |
| `rank_based_normalization_processor_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.rank_based_normalization_processor_executions` | `score-ranker-processor` 處理器的執行次數。 |
| `comb_harmonic_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.comb_harmonic_executions` | 將 `combination.technique` 設為 `harmonic_mean` 的 `normalization-processor` 處理器執行次數。 |
| `norm_zscore_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.norm_zscore_executions` | 將 `normalization.technique` 設為 `z_score` 的 `normalization-processor` 處理器執行次數。 |
| `comb_rrf_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.comb_rrf_executions` | 將 `combination.technique` 設為 `rrf` 的 `score-ranker-processor` 處理器執行次數。 |
| `norm_l2_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.norm_l2_executions` | 將 `normalization.technique` 設為 `l2` 的 `normalization-processor` 處理器執行次數。 |
| `comb_arithmetic_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.comb_arithmetic_executions` | 將 `combination.technique` 設為 `arithmetic_mean` 的 `normalization-processor` 處理器執行次數。 |
| `comb_geometric_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.comb_geometric_executions` | 將 `combination.technique` 設為 `geometric_mean` 的 `normalization-processor` 處理器執行次數。 |
| `norm_minmax_executions` | `nodes`, `all_nodes` | `processors.search.hybrid.norm_minmax_executions` | 將 `normalization.technique` 設為 `min_max` 的 `normalization-processor` 處理器執行次數。 |

**節點層級統計資料：查詢**

| 統計名稱 | 類別 | 類別內的統計路徑 | 說明                                                                                                                                |
| :--- | :--- | :--- |:-------------------------------------------------------------------------------------------------------------------------------------------|
| `hybrid_query_with_pagination_requests` | `nodes`, `all_nodes` | `query.hybrid.hybrid_query_with_pagination_requests` | 帶有分頁的 `hybrid` 查詢請求數量。                                                                                     |
| `hybrid_query_with_filter_requests` | `nodes`, `all_nodes` | `query.hybrid.hybrid_query_with_filter_requests` | 帶有篩選條件的 `hybrid` 查詢請求數量。                                                                                        |
| `hybrid_query_with_inner_hits_requests` | `nodes`, `all_nodes` | `query.hybrid.hybrid_query_with_inner_hits_requests` | 帶有內部命中的 `hybrid` 查詢請求數量。                                                                                     |
| `hybrid_query_requests` | `nodes`, `all_nodes` | `query.hybrid.hybrid_query_requests` | `hybrid` 查詢請求的總數。                                                                                               |
| `neural_query_against_semantic_sparse_requests` | `nodes`, `all_nodes` | `query.neural.neural_query_against_semantic_sparse_requests` | 針對語意稀疏欄位的 `neural` 查詢請求數量。                                                                      |
| `neural_query_requests` | `nodes`, `all_nodes` | `query.neural.neural_query_requests` | `neural` 查詢請求的總數。                                                                                               |
| `neural_query_against_semantic_dense_requests` | `nodes`, `all_nodes` | `query.neural.neural_query_against_semantic_dense_requests` | 針對語意稠密欄位的 `neural` 查詢請求數量。                                                                       |
| `neural_query_against_knn_requests` | `nodes`, `all_nodes` | `query.neural.neural_query_against_knn_requests` | 針對 k-NN 欄位的 `neural` 查詢請求數量。                                                                                 |
| `neural_sparse_query_requests` | `nodes`, `all_nodes` | `query.neural_sparse.neural_sparse_query_requests` | 針對 `rank_features` 欄位的 `neural_sparse` 查詢請求數量 (傳統神經稀疏搜尋)。                                                                                              |
| `seismic_query_requests` | `nodes`, `all_nodes` | `query.neural_sparse.seismic_query_requests` | 針對 `sparse_vector` 欄位的 `neural_sparse` 查詢請求數量 (使用 SEISMIC 演算法的神經稀疏近似最近鄰 (ANN) 搜尋)。 |

**節點層級統計：記憶體**

| 統計名稱 | 類別             | 類別內的統計路徑                                  | 說明                                                                                                 |
| :--- |:---------------------|:----------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|
| `sparse_memory_usage_percentage` | `nodes`              | `memory.sparse.sparse_memory_usage_percentage`                  | 節點上用於儲存稀疏資料的 JVM 堆積記憶體相對於最大 JVM 記憶體的百分比。 |
| `sparse_memory_usage` | `nodes`, `all_nodes` | `memory.sparse.sparse_memory_usage`                             | 節點上用於儲存稀疏資料的 JVM 堆積記憶體量，以 KB 為單位。                           |
| `clustered_posting_usage` | `nodes`, `all_nodes` | `memory.sparse.clustered_posting_usage`                         | 節點上用於儲存叢集式張貼清單的 JVM 堆積記憶體量，以 KB 為單位。                     |
| `forward_index_usage` | `nodes`, `all_nodes` | `memory.sparse.forward_index_usage`                            | 節點上用於儲存正向索引的 JVM 堆積記憶體量，以 KB 為單位。                         |

這些記憶體統計資料僅回報 Lucene 引擎快取。原生引擎會將其索引保留在磁碟上的記憶體對應檔案中，因此原生引擎的索引記憶體不會反映在這些統計資料中。如需更多資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。
{: .note}

**節點層級統計：語意醒目提示**

| 統計名稱 | 類別 | 類別內的統計路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| `semantic_highlighting_request_count` | `nodes`, `all_nodes` | `semantic_highlighting.semantic_highlighting_request_count` | 單次推論 `semantic` 醒目提示請求數量 (每份文件一次推論呼叫)。請參閱[單次推論模式]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/#basic-usage-single-inference-mode)。 |
| `semantic_highlighting_batch_request_count` | `nodes`, `all_nodes` | `semantic_highlighting.semantic_highlighting_batch_request_count` | 批次推論 `semantic` 醒目提示請求數量 (在單次推論呼叫中處理多份文件)。請參閱[批次推論模式]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/#batch-inference-mode)。 |

#### 可用的中繼資料

當 `include_metadata` 為 `true` 時，回應中的欄位值會以其各自的中繼資料物件取代，這些物件包含有關統計類型的額外資訊，如下表所述。 

| 統計類型 | 說明 |
| :--- | :--- |
| `info_string` | 提供資訊性內容的基本字串值，例如版本或名稱。請參閱[`info_string`](#info-string)。|
| `info_counter` | 代表靜態或緩慢變化值的數值計數器。請參閱[`info_counter`](#info-counter)。|
| `timestamped_event_counter` | 追蹤一段時間內事件的計數器，包含近期活動的相關資訊。請參閱[`timestamped_event_counter`](#timestamped-event-counter)。|

<p id="info-string"></p>

`info_string` 物件包含下列中繼資料欄位。

| 中繼資料欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `value` | 字串 | 統計資料的實際字串值。 |
| `stat_type` | 字串 | 一律設為 `info_string`。 |

<p id="info-counter"></p>

`info_counter` 物件包含下列中繼資料欄位。

| 中繼資料欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `value` | 整數 | 目前的計數值。 |
| `stat_type` | 字串 | 一律設為 `info_counter`。 |

<p id="timestamped-event-counter"></p>

`timestamped_event_counter` 物件包含下列中繼資料欄位。

| 中繼資料欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `value` | 整數 | 自節點啟動以來發生的事件總數。 |
| `stat_type` | 字串 | 一律設為 `timestamped_event_counter`。 |
| `trailing_interval_value` | 整數 | 過去 5 分鐘內發生的事件數量。 |
| `minutes_since_last_event` | 整數 | 自上次記錄事件以來的時間量 (以分鐘為單位)。 |

## 暖機
**於 3.3 版導入**
{: .label .label-purple }

稀疏索引支援[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)。為了將搜尋效率最大化，OpenSearch 會將稀疏資料快取在 JVM 記憶體中。

為避免初次搜尋時出現高延遲，您可以在暖機期間執行隨機查詢。暖機期間結束後，稀疏資料會儲存在 JVM 記憶體中，您就可以開始正式工作負載。不過，這種方式較為間接，且需要額外的心力。

或者，您可以使用暖機 API 操作來避免初次搜尋時的延遲。此操作會將指定索引之主要分片與副本分片的所有稀疏資料載入 JVM 記憶體。暖機 API 操作具有冪等性：如果某個分段的稀疏資料已載入記憶體，此操作不會產生任何效果。它只會載入目前未儲存在記憶體中的檔案。

此 API 操作僅適用於稀疏索引（以 `index.sparse` 設為 `true` 建立的索引），且其欄位必須使用 Lucene 引擎。原生引擎會從記憶體對應檔案讀取其索引，而非 JVM 堆積快取，因此沒有需要暖機的內容。如需更多資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。
{: .note}

### 端點

```json
POST /_plugins/_neural/warmup/{index}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<index>` | 字串 | 要暖機的一個或多個索引名稱（以逗號分隔）。支援萬用字元 (`*`)。必要。 |

#### 範例請求

下列請求對三個索引執行暖機操作：

```json
POST /_plugins/_neural/warmup/index1,index2,index3
```
{% include copy-curl.html %}

您可以在暖機 API 操作中使用索引模式，將符合指定模式的一個或多個索引載入快取：

```json
POST /_plugins/_neural/warmup/index*
```
{% include copy-curl.html %}

#### 範例回應

API 呼叫只會在暖機操作完成或請求逾時後才傳回結果：

```json
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```

如果請求逾時，操作會繼續在叢集上執行。

若要監視暖機操作，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)：

```json
GET /_tasks
```
{% include copy-curl.html %}

操作完成後，請使用 [neural stats API 操作](#stats) 監視更新後的記憶體使用量。

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位                | 資料類型 | 說明                                                      |
| :------------------- | :-------- | :--------------------------------------------------------------- |
| `_shards.total`      | 整數   | OpenSearch 嘗試暖機的分片總數。 |
| `_shards.successful` | 整數   | 成功暖機的分片數量。           |
| `_shards.failed`     | 整數   | 暖機失敗的分片數量。                     |

### 最佳做法

為確保暖機操作正常運作，請遵循下列最佳做法：

* 避免在計畫暖機的索引上執行合併操作：在合併操作期間，OpenSearch 會建立新的分段，並可能刪除舊的分段。例如，如果暖機 API 操作將稀疏索引 A 與 B 載入原生記憶體，但合併操作從 A 與 B 建立了新的分段 C，則 A 與 B 會從記憶體中移除，而 C 尚未載入。在這種情況下，稀疏索引 C 仍會出現初次載入延遲。

* 確認您計畫暖機的所有稀疏索引都能放入 JVM 記憶體。如需記憶體限制的更多資訊，請參閱 [neural_search.circuit_breaker.limit]({{site.url}}{{site.baseurl}}/vector-search/settings#neural-search-plugin-settings)。

## 清除快取
**於 3.3 版導入**
{: .label .label-purple }

在[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)或暖機操作期間，稀疏資料會載入 JVM 記憶體。您可以透過刪除對應的索引來移除這些資料。

相對地，降低[神經搜尋斷路器限制]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann#memory-and-caching-settings)並不會立即驅逐已快取的稀疏資料。若要手動清除快取資料，請使用 neural search clear cache API 操作。此操作會移除請求中所指定索引之所有分片（主要與副本）的所有記憶體內稀疏資料。

與[暖機操作](#warm-up)類似，清除快取操作具有冪等性：如果您嘗試清除已被驅逐之索引的快取，操作不會產生額外效果。

此 API 操作僅適用於稀疏索引（以 `index.sparse` 設為 `true` 建立的索引），且其欄位必須使用 Lucene 引擎。原生引擎不使用外掛程式管理的快取，因此沒有需要清除的內容。如需更多資訊，請參閱[引擎]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/#engines)。
{: .note}

### 端點

```json
POST /_plugins/_neural/clear_cache/{index}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明                                                                                  |
| :-------- | :-------- | :------------------------------------------------------------------------------------------- |
| `<index>` | 字串    | 要清除快取的一個或多個索引名稱（以逗號分隔）。支援萬用字元 (`*`)。必要。 |

#### 範例請求

下列請求會從 JVM 記憶體中清除三個指定索引的稀疏資料：

```json
POST /_plugins/_neural/clear_cache/index1,index2,index3
```

{% include copy-curl.html %}

您也可以使用索引模式來清除符合某個模式的一個或多個索引：

```json
POST /_plugins/_neural/clear_cache/index*
```

{% include copy-curl.html %}

#### 範例回應

API 呼叫只會在清除快取操作完成或請求逾時後才傳回結果：

```json
{
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "failed" : 0
  }
}
```

如果請求逾時，操作會繼續在叢集中執行。

若要監視清除快取操作的進度，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)：

```json
GET /_tasks
```

{% include copy-curl.html %}

操作完成後，請使用 [neural stats API 操作](#stats) 檢查更新後的記憶體使用量。

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位                | 資料類型 | 說明                                                      |
| :------------------- | :-------- | :--------------------------------------------------------------- |
| `_shards.total`      | 整數   | OpenSearch 嘗試清除快取的分片總數。 |
| `_shards.successful` | 整數   | 成功清除快取的分片數量。           |
| `_shards.failed`     | 整數   | 清除快取失敗的分片數量。                     |