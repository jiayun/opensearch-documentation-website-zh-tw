---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋記憶"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 25
---

# 搜尋記憶 API
**2.12 版新增**
{: .label .label-purple }

此 API 會擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)所使用的對話記憶。請使用此命令搜尋記憶。

當 Security 外掛程式啟用時，所有記憶都存在於 `private` 安全模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}

## 端點

```json
GET /_plugins/_ml/memory/_search
POST /_plugins/_ml/memory/_search
```

## 範例請求：搜尋所有記憶

```json
POST /_plugins/_ml/memory/_search
{
  "query": {
    "match_all": {}
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例請求：依名稱搜尋記憶

```json
POST /_plugins/_ml/memory/_search
{
  "query": {
    "term": {
      "name": {
        "value": "conversation"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.2195382,
    "hits": [
      {
        "_index": ".plugins-ml-memory-meta",
        "_id": "znCqcI0BfUsSoeNTntd7",
        "_version": 3,
        "_seq_no": 39,
        "_primary_term": 1,
        "_score": 0.2195382,
        "_source": {
          "updated_time": "2024-02-03T20:36:10.252213029Z",
          "create_time": "2024-02-03T20:30:46.395829411Z",
          "application_type": null,
          "name": "Conversation about NYC population",
          "user": "admin"
        }
      },
      {
        "_index": ".plugins-ml-memory-meta",
        "_id": "iXC4bI0BfUsSoeNTjS30",
        "_version": 4,
        "_seq_no": 11,
        "_primary_term": 1,
        "_score": 0.20763937,
        "_source": {
          "updated_time": "2024-02-03T02:59:39.862347093Z",
          "create_time": "2024-02-03T02:07:30.804554275Z",
          "application_type": null,
          "name": "Test conversation for RAG pipeline",
          "user": "admin"
        }
      },
      {
        "_index": ".plugins-ml-memory-meta",
        "_id": "gW8Aa40BfUsSoeNTvOKI",
        "_version": 4,
        "_seq_no": 6,
        "_primary_term": 1,
        "_score": 0.19754036,
        "_source": {
          "updated_time": "2024-02-02T19:01:32.121444968Z",
          "create_time": "2024-02-02T18:07:06.887061463Z",
          "application_type": null,
          "name": "Conversation for a RAG pipeline",
          "user": "admin"
        }
      }
    ]
  }
}
```

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `create_time` | 字串 | 記憶建立的時間。 |
| `updated_time` | 字串 | 記憶最後更新的時間。 |
| `name` | 字串 | 記憶名稱。 |
| `user` | 字串 | 建立記憶之使用者的使用者名稱。 |