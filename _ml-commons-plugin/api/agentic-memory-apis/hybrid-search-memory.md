---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合搜尋代理程式記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 70
---

# 混合搜尋代理程式記憶 API
**於 3.6 版推出**
{: .label .label-purple }

使用此 API 結合 BM25 關鍵字比對與語意搜尋來搜尋長期記憶。當您的查詢同時受益於精確的關鍵字精確度與語意理解時，這會很有用。

混合搜尋會在單一查詢中結合兩種搜尋方法：

1. **BM25 關鍵字搜尋**：對 `memory` 欄位執行 `match` 查詢，以進行精確的關鍵字比對。
2. **神經向量搜尋**：對 `memory_embedding` 欄位執行 `neural` 查詢（若為 `SPARSE_ENCODING` 模型則使用 `neural_sparse`），以進行語意相似度比對。

結果會使用內嵌正規化處理器管線來合併，該管線使用 `min_max` 正規化與 `arithmetic_mean` 組合。`bm25_weight` 與 `neural_weight` 參數控制每種搜尋方法的相對重要性。不需要預先設定的搜尋管線。

記憶容器必須設定嵌入模型以及至少一個[記憶策略]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-processing-strategies)。 
{: .note}

## 端點

```json
POST /_plugins/_ml/memory_containers/{memory_container_id}/memories/long-term/_hybrid_search
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/long-term/_hybrid_search
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 記憶容器的 ID。 |

## 請求欄位

下表列出可用的請求欄位。

| 欄位 | 資料類型 | 必要/選用 | 預設 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| `query` | 字串 | 必要 | N/A | 同時用於 BM25 關鍵字比對與語意搜尋的自然語言搜尋查詢。  |
| `k` | 整數 | 選用 | 10 | 要傳回的結果數。有效值為 `1`–`10000`（含）。 |
| `namespace` | 物件 | 選用 | N/A | 依命名空間欄位篩選結果。例如 `{"user_id": "alice"}`。 |
| `tags` | 物件 | 選用 | N/A | 依標籤欄位篩選結果。例如 `{"topic": "food"}`。 |
| `min_score` | 浮點數 | 選用 | N/A | 最低相關性分數閾值。低於此分數的結果會被排除。 |
| `filter` | 物件 | 選用 | N/A | 與混合查詢一併套用的額外 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 篩選條件。 |
| `bm25_weight` | 浮點數 | 選用 | 0.5 | BM25 關鍵字搜尋元件的權重。有效值為 `0.0`–`1.0`。`bm25_weight` 與 `neural_weight` 的總和必須等於 `1.0`。 |
| `neural_weight` | 浮點數 | 選用 | 0.5 | 神經向量搜尋元件的權重。有效值為 `0.0`–`1.0`。`bm25_weight` 與 `neural_weight` 的總和必須等於 `1.0`。 |

## 範例請求：基本混合搜尋

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_hybrid_search
{
  "query": "retirement timeline five years portfolio rebalancing",
  "k": 10,
  "namespace": {
    "user_id": "bob"
  }
}
```
{% include copy-curl.html %}

## 範例請求：自訂權重

您可以針對每個請求調整關鍵字搜尋與語意搜尋之間的平衡。提高 `neural_weight` 會優先考量語意相似度，而提高 `bm25_weight` 則會優先考量精確的關鍵字比對：

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_hybrid_search
{
  "query": "machine learning outdoor activities",
  "k": 5,
  "namespace": {
    "user_id": "alice"
  },
  "bm25_weight": 0.3,
  "neural_weight": 0.7
}
```
{% include copy-curl.html %}

## 範例請求：最低分數與標籤篩選

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_hybrid_search
{
  "query": "LGBTQ workshop therapeutic methods",
  "k": 10,
  "namespace": {
    "user_id": "caroline"
  },
  "tags": {
    "topic": "wellness"
  },
  "min_score": 0.3
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 15,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "test-memory-long-term",
        "_id": "abc123",
        "_score": 1.0,
        "_source": {
          "memory": "Caroline attended an LGBTQ+ counseling workshop focused on therapeutic methods",
          "strategy_type": "SEMANTIC",
          "namespace": {
            "user_id": "caroline"
          },
          "memory_container_id": "HudqiJkB1SltqOcZusVU",
          "created_time": 1700000000000,
          "last_updated_time": 1700000000000
        }
      },
      {
        "_index": "test-memory-long-term",
        "_id": "def456",
        "_score": 0.52,
        "_source": {
          "memory": "Caroline attended an LGBTQ conference on community building",
          "strategy_type": "SEMANTIC",
          "namespace": {
            "user_id": "caroline"
          },
          "memory_container_id": "HudqiJkB1SltqOcZusVU",
          "created_time": 1700000000000,
          "last_updated_time": 1700000000000
        }
      }
    ]
  }
}
```

## 回應欄位

回應使用標準的 OpenSearch 搜尋回應格式。如需欄位說明，請參閱[語意搜尋記憶回應欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/semantic-search-memory/#response-fields)。

`memory_embedding` 欄位不會包含在回應中。

## 相關文件

- [混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/)
