---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋模型群組"
parent: Model group APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 搜尋模型群組 API

當您搜尋模型群組時，只會傳回您有權存取的模型群組。例如，對於 match all 查詢，會傳回的模型群組包括：

- 索引中的所有公開模型群組
- 您是擁有者的私人模型群組
- 與您共用至少一個 `backend_roles` 的模型群組

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 路徑與 HTTP 方法

```json
POST /_plugins/_ml/model_groups/_search
GET /_plugins/_ml/model_groups/_search
```

## 範例請求：Match all

下列請求由具有 `IT` 與 `HR` 角色的 `user1` 傳送：

```json
POST /_plugins/_ml/model_groups/_search
{
  "query": {
    "match_all": {}
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 31,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".plugins-ml-model-group",
        "_id": "TRqZfYgBD7s2oEFdvrQj",
        "_version": 1,
        "_seq_no": 2,
        "_primary_term": 1,
        "_score": 1,
        "_source": {
          "backend_roles": [
            "HR",
            "IT"
          ],
          "owner": {
            "backend_roles": [
              "HR",
              "IT"
            ],
            "custom_attribute_names": [],
            "roles": [
              "ml_full_access",
              "own_index",
              "test_ml"
            ],
            "name": "user1",
            "user_requested_tenant": "__user__"
          },
          "created_time": 1685734407714,
          "access": "restricted",
          "latest_version": 0,
          "last_updated_time": 1685734407714,
          "name": "model_group_test",
          "description": "This is an example description"
        }
      },
      {
        "_index": ".plugins-ml-model-group",
        "_id": "URqZfYgBD7s2oEFdyLTm",
        "_version": 1,
        "_seq_no": 3,
        "_primary_term": 1,
        "_score": 1,
        "_source": {
          "backend_roles": [
            "IT"
          ],
          "owner": {
            "backend_roles": [
              "HR",
              "IT"
            ],
            "custom_attribute_names": [],
            "roles": [
              "ml_full_access",
              "own_index",
              "test_ml"
            ],
            "name": "user1",
            "user_requested_tenant": "__user__"
          },
          "created_time": 1685734410470,
          "access": "restricted",
          "latest_version": 0,
          "last_updated_time": 1685734410470,
          "name": "model_group_test",
          "description": "This is an example description"
        }
      },
      ...
    ]
  }
}
```

## 範例請求：依擁有者名稱搜尋模型群組

下列依 `user` 搜尋模型群組的請求，由具有 `IT` 後端角色的 `user2` 傳送：

```json
GET /_plugins/_ml/model_groups/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "nested": {
            "query": {
              "term": {
                "owner.name.keyword": {
                  "value": "user1",
                  "boost": 1
                }
              }
            },
            "path": "owner",
            "ignore_unmapped": false,
            "score_mode": "none",
            "boost": 1
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": ".plugins-ml-model-group",
        "_id": "TRqZfYgBD7s2oEFdvrQj",
        "_version": 1,
        "_seq_no": 2,
        "_primary_term": 1,
        "_score": 0,
        "_source": {
          "backend_roles": [
            "HR",
            "IT"
          ],
          "owner": {
            "backend_roles": [
              "HR",
              "IT"
            ],
            "custom_attribute_names": [],
            "roles": [
              "ml_full_access",
              "own_index",
              "test_ml"
            ],
            "name": "user1",
            "user_requested_tenant": "__user__"
          },
          "created_time": 1685734407714,
          "access": "restricted",
          "latest_version": 0,
          "last_updated_time": 1685734407714,
          "name": "model_group_test",
          "description": "This is an example description"
        }
      },
      ...
    ]
  }
}
```

## 範例請求：依模型群組 ID 搜尋模型群組

```json
GET /_plugins/_ml/model_groups/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "_id": [
              "HyPNK4gBwNxGowI0AtDk"
            ]
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 2,
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
    "max_score": 1,
    "hits": [
      {
        "_index": ".plugins-ml-model-group",
        "_id": "HyPNK4gBwNxGowI0AtDk",
        "_version": 3,
        "_seq_no": 16,
        "_primary_term": 5,
        "_score": 1,
        "_source": {
          "backend_roles": [
            "IT"
          ],
          "owner": {
            "backend_roles": [
              "",
              "HR",
              "IT"
            ],
            "custom_attribute_names": [],
            "roles": [
              "ml_full_access",
              "own_index",
              "test-ml"
            ],
            "name": "user1",
            "user_requested_tenant": null
          },
          "created_time": 1684362035938,
          "latest_version": 2,
          "last_updated_time": 1684362571300,
          "name": "model_group_test",
          "description": "This is an example description"
        }
      }
    ]
  }
}
```