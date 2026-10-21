---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語意搜尋代理記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 60
---

# 語意搜尋代理記憶 API
**3.6 版新增**
{: .label .label-purple }

使用此 API 以自然語言查詢搜尋長期記憶。OpenSearch 會自動從您的查詢文字產生嵌入，並對已儲存的記憶嵌入執行向量相似度搜尋。這樣就不需要使用預先產生的嵌入手動建構 k-NN 查詢。

記憶容器必須已設定嵌入模型，且至少有一個[記憶策略]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-processing-strategies)。
{: .note}

## 端點

```json
POST /_plugins/_ml/memory_containers/{memory_container_id}/memories/long-term/_semantic_search
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/long-term/_semantic_search
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
| `query` | 字串 | 必要 | N/A | 自然語言搜尋查詢。OpenSearch 會使用記憶容器所設定的嵌入模型自動產生嵌入。 |
| `k` | 整數 | 選用 | 10 | 要傳回的結果數量。有效值為 1–10,000。 |
| `namespace` | 物件 | 選用 | N/A | 依命名空間欄位篩選結果。例如 `{"user_id": "alice"}`。 |
| `tags` | 物件 | 選用 | N/A | 依標籤欄位篩選結果。例如 `{"topic": "food"}`。 |
| `min_score` | 浮點數 | 選用 | N/A | 最低相關性分數門檻。低於此分數的結果會被排除。 |
| `filter` | 物件 | 選用 | N/A | 與語意查詢一併套用的額外 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 篩選條件。 |

## 請求範例：基本語意搜尋

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_semantic_search
{
  "query": "retirement planning portfolio rebalancing",
  "k": 5,
  "namespace": {
    "user_id": "bob"
  }
}
```
{% include copy-curl.html %}

## 請求範例：最低分數與標籤篩選

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_semantic_search
{
  "query": "client risk tolerance and investment preferences",
  "k": 5,
  "namespace": {
    "user_id": "bob"
  },
  "tags": {
    "topic": "finance"
  },
  "min_score": 0.6
}
```
{% include copy-curl.html %}

## 請求範例：Query DSL 篩選

```json
POST /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_semantic_search
{
  "query": "programming languages for data science",
  "k": 10,
  "namespace": {
    "user_id": "alice"
  },
  "filter": {
    "range": {
      "created_time": {
        "gte": 1700000000000
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 12,
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
    "max_score": 0.87,
    "hits": [
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "abc123",
        "_score": 0.87,
        "_source": {
          "created_time": 1700000000000,
          "memory": "Client plans to retire in five years with a gradual rebalancing strategy",
          "last_updated_time": 1700000000000,
          "namespace_size": 1,
          "namespace": {
            "user_id": "bob"
          },
          "strategy_id": "semantic_53d1751c",
          "strategy_type": "SEMANTIC",
          "memory_container_id": "HudqiJkB1SltqOcZusVU"
        }
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "def456",
        "_score": 0.82,
        "_source": {
          "created_time": 1700000000000,
          "memory": "Client prefers conservative investments and wants to shift away from equities",
          "last_updated_time": 1700000000000,
          "namespace_size": 1,
          "namespace": {
            "user_id": "bob"
          },
          "strategy_id": "user_preference_0771b88e",
          "strategy_type": "USER_PREFERENCE",
          "memory_container_id": "HudqiJkB1SltqOcZusVU"
        }
      }
    ]
  }
}
```

## 回應欄位

回應使用標準的 OpenSearch 搜尋回應格式。`hits.hits` 陣列中的每個命中結果都在 `_source` 中包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory` | 字串 | 擷取出的記憶文字。 |
| `strategy_type` | 字串 | 產生此記憶的策略（`SEMANTIC`、`USER_PREFERENCE` 或 `SUMMARY`）。 |
| `namespace` | 物件 | 與此記憶相關聯的命名空間欄位。 |
| `namespace_size` | 整數 | 命名空間欄位的數量。 |
| `strategy_id` | 字串 | 產生此記憶的策略 ID。 |
| `tags` | 物件 | 與此記憶相關聯的標籤。僅在記憶具有標籤時才會出現。 |
| `memory_container_id` | 字串 | 記憶容器的 ID。 |
| `created_time` | Long | 建立記憶的時間戳記。 |
| `last_updated_time` | Long | 記憶最後一次更新的時間戳記。 |

回應中不包含 `memory_embedding` 欄位。

## 相關文件

- [語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)