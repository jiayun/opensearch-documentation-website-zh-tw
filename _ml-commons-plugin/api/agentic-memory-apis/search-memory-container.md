---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋記憶容器"
parent: Agentic memory APIs
grand_parent: ML APIs
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

## 範例回應

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
        "_index": ".plugins-ml-am-memory-container",
        "_id": "HudqiJkB1SltqOcZusVU",
        "_version": 1,
        "_seq_no": 0,
        "_primary_term": 1,
        "_score": 1.0,
        "_source": {
          "created_time": 1757956737699,
          "last_updated_time": 1757956737699,
          "configuration": {
            "embedding_model_id": "uXZAtJkBvHNmcp1JAROh",
            "strategies": [
              {
                "namespace": ["user_id"],
                "id": "semantic_53d1751c",
                "type": "SEMANTIC",
                "enabled": true
              }
            ],
            "max_infer_size": 5,
            "embedding_dimension": 1024,
            "index_prefix": "default",
            "use_system_index": true,
            "llm_id": "aFouy5kBrfmzAZ6R6wo-",
            "disable_history": false,
            "embedding_model_type": "TEXT_EMBEDDING",
            "disable_session": false
          },
          "name": "agentic memory test",
          "description": "Store conversations with semantic search and summarization"
        }
      },
      ...
    ]
  }
}
```

## 回應欄位

回應使用標準的 OpenSearch 搜尋回應格式。下表列出 `hits` 陣列中每個元素的 `_source` 物件內的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | 字串 | 記憶容器的名稱。 |
| `description` | 字串 | 記憶容器的說明。 |
| `configuration` | 物件 | 記憶容器的組態，包括模型與策略。 |
| `created_time` | Long | 容器建立的時間戳記。 |
| `last_updated_time` | Long | 容器最後更新的時間戳記。 |
| `backend_roles` | 陣列 | 可存取該容器的後端角色。僅在已設定後端角色時才會顯示。 |
