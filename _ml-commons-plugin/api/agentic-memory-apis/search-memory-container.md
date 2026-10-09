---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋記憶容器"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 25
---

# 搜尋記憶容器 API
**3.3 版新增**
{: .label .label-purple }

使用此 API，透過 OpenSearch Query DSL 搜尋記憶容器。

## 端點

```json
GET /_plugins/_ml/memory_containers/_search
POST /_plugins/_ml/memory_containers/_search
```

## 請求欄位

請求本文支援標準的 OpenSearch Query DSL。如需更多資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

## 請求範例

```json
GET /_plugins/_ml/memory_containers/_search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "took": 5,
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
        "_index": ".plugins-ml-memory-meta",
        "_id": "HudqiJkB1SltqOcZusVU",
        "_score": 1.0,
        "_source": {
          "name": "agentic memory test",
          "description": "Store conversations with semantic search and summarization",
          "configuration": {
            "embedding_model_type": "TEXT_EMBEDDING",
            "embedding_model_id": "uXZAtJkBvHNmcp1JAROh",
            "embedding_dimension": 1024,
            "llm_id": "aFouy5kBrfmzAZ6R6wo-",
            "strategies": [
              {
                "type": "SEMANTIC",
                "namespace": ["user_id"]
              }
            ]
          },
          "created_time": 1757956737699,
          "last_updated_time": 1757956737699
        }
      }
    ]
  }
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | 字串 | 記憶容器的名稱。 |
| `description` | 字串 | 記憶容器的描述。 |
| `configuration` | 物件 | 記憶容器的組態，包括模型與策略。 |
| `created_time` | Long | 容器建立的時間戳記。 |
| `last_updated_time` | Long | 容器最後更新的時間戳記。 |
