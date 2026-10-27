---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得記憶容器"
parent: Agentic memory APIs
grand_parent: ML APIs
nav_order: 20
---

# 取得記憶容器 API
**於 3.3 版推出**
{: .label .label-purple }


使用此 API 依 ID 擷取記憶容器。

## 端點

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 要擷取的記憶容器 ID。 |

## 範例請求

```json
GET /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name": "agentic memory test",
  "description": "Store conversations with semantic search and summarization",
  "created_time": 1792070644500,
  "last_updated_time": 1792070644500,
  "configuration": {
    "index_prefix": "default",
    "llm_id": "aFouy5kBrfmzAZ6R6wo-",
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "uXZAtJkBvHNmcp1JAROh",
    "embedding_dimension": 1024,
    "max_infer_size": 5,
    "strategies": [
      {
        "id": "semantic_53d1751c",
        "enabled": true,
        "type": "SEMANTIC",
        "namespace": [
          "user_id"
        ]
      }
    ],
    "disable_history": false,
    "disable_session": false,
    "use_system_index": true
  }
}
```

## 回應本文欄位

如需回應欄位的說明，請參閱 [Create Memory Container API 請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container#request-body-fields)。

回應中的每個[策略]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-processing-strategies)也包含 OpenSearch 產生的 `id`。若要更新策略，請在 [Update Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory-container/) 請求中提供此 `id`。
