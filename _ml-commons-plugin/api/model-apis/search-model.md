---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋模型"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 35
---

# Search Model API

您可以使用此命令來搜尋您已建立的模型。

回應只會包含您有權存取的模型版本。例如，如果您傳送 `match_all` 查詢，將會傳回下列模型群組類型的模型版本：

- 索引中的所有公開模型群組
- 您是模型擁有者的私人模型群組
- 與您的後端角色至少共用一個後端角色的模型群組

如需此 API 的使用者存取相關資訊，請參閱[模型存取控制考量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
GET /_plugins/_ml/models/_search
POST /_plugins/_ml/models/_search
```

## 範例請求：搜尋所有模型

```json
POST /_plugins/_ml/models/_search
{
  "query": {
    "match_all": {}
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例請求：搜尋演算法為「FIT_RCF」的模型

```json
POST /_plugins/_ml/models/_search
{
  "query": {
    "term": {
      "algorithm": {
        "value": "FIT_RCF"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例：排除模型區塊

```json
GET /_plugins/_ml/models/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "chunk_number"
        }
      }
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

#### 範例：搜尋所有模型區塊

下列查詢會搜尋 ID 為 `979y9YwBjWKCe6KgNGTm` 的模型的所有區塊，並以遞增順序排序這些區塊：

```json
GET /_plugins/_ml/models/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "model_id": "9r9w9YwBjWKCe6KgyGST"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "chunk_number": {
        "order": "asc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 範例：依描述搜尋模型

```json
GET _plugins/_ml/models/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "description": "sentence transformer"
          }
        }
      ],
      "must_not": {
        "exists": {
          "field": "chunk_number"
        }
      }
    }
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
    "took" : 8,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 2,
        "relation" : "eq"
      },
      "max_score" : 2.4159138,
      "hits" : [
        {
          "_index" : ".plugins-ml-model",
          "_id" : "-QkKJX8BvytMh9aUeuLD",
          "_version" : 1,
          "_seq_no" : 12,
          "_primary_term" : 15,
          "_score" : 2.4159138,
          "_source" : {
            "name" : "FIT_RCF",
            "version" : 1,
            "content" : "xxx",
            "algorithm" : "FIT_RCF"
          }
        },
        {
          "_index" : ".plugins-ml-model",
          "_id" : "OxkvHn8BNJ65KnIpck8x",
          "_version" : 1,
          "_seq_no" : 2,
          "_primary_term" : 8,
          "_score" : 2.4159138,
          "_source" : {
            "name" : "FIT_RCF",
            "version" : 1,
            "content" : "xxx",
            "algorithm" : "FIT_RCF"
          }
        }
      ]
    }
  }
```