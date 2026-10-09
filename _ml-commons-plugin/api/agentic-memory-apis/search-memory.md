---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋代理程式記憶"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 54
---

# 搜尋代理程式記憶 API
**於 3.3 版推出**
{: .label .label-purple }

使用此 API 在記憶容器內搜尋特定類型的記憶。此統一 API 支援搜尋 `sessions`、`working`、`long-term` 和 `history` [記憶類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/#memory-types)。

## 端點

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}/memories/{type}/_search
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要/選用 | 說明 |
| :--- | :--- | :--- | :--- |
| `memory_container_id` | 字串 | 必要 | 記憶容器的 ID。 |
| `type` | 字串 | 必要 | 記憶類型。有效值為 `sessions`、`working`、`long-term` 和 `history`。 |

## 請求欄位

請求本文支援標準 OpenSearch Query DSL。如需更多資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

## 範例請求：搜尋工作階段

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/sessions/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例請求：搜尋長期記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/long-term/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "namespace.user_id": "bob"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例請求：搜尋歷史記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/history/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例請求：使用命名空間篩選條件搜尋工作記憶

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "namespace.user_id": "bob"
          }
        }
      ],
      "must_not": [
        {
          "exists": {
            "field": "tags.parent_memory_id"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例請求：依工作階段搜尋追蹤資料

```json
GET /_plugins/_ml/memory_containers/HudqiJkB1SltqOcZusVU/memories/working/_search
{
  "query": {
    "term": {
      "namespace.session_id": "123"
    }
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "test1-session",
        "_id": "CcxjTpkBvwXRq366A1aE",
        "_score": null,
        "_source": {
          "memory_container_id": "HudqiJkB1SltqOcZusVU",
          "namespace": {
            "user_id": "bob"
          },
          "created_time": "2025-09-15T17:18:55.881276939Z",
          "last_updated_time": "2025-09-15T17:18:55.881276939Z"
        },
        "sort": ["2025-09-15T17:18:55.881276939Z"]
      }
    ]
  }
}
```

## 回應欄位

回應欄位會依所搜尋的記憶類型而有所不同。如需欄位說明，請參閱[取得記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/get-memory/#response-fields)。
