---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在混合查詢中使用排序"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 10
---

# 在混合查詢中使用排序
**於 2.16 版導入**
{: .label .label-purple }

預設情況下，混合搜尋會以分數遞減順序傳回結果。您可以在搜尋請求中提供 `sort` 準則，為混合查詢結果套用排序。如需排序準則的更多資訊，請參閱 [排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。
當排序套用於混合搜尋時，系統會依據指定的排序準則從分片取得結果。因此，搜尋結果會據此排序，而文件分數為 `null`。只有當文件依 `_score` 排序時，混合搜尋排序結果中才會包含分數。

從 OpenSearch 3.5 開始，[`min_score`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#request-body) 參數會在分數正規化與合併之後套用。此參數只能在依 `_score` 排序或未指定明確排序順序時使用。若 `min_score` 與任何其他排序準則一起使用，請求將導致錯誤。
{: .important}

在下列範例中，混合查詢搜尋請求依 `doc_price` 套用排序：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "term": {
            "category": "permission"
          }
        },
        {
          "bool": {
            "should": [
              {
                "term": {
                  "category": "editor"
                }
              },
              {
                "term": {
                  "category": "statement"
                }
              }
            ]
          }
        }
      ]
    }
  }, 
    "sort":[
       {
         "doc_price": {
             "order": "desc"
         }
       }
    ]
}
```
{% include copy-curl.html %}

回應包含依 `doc_price` 遞減排序的相符文件：

```json
{
    "took": 35,
    "timed_out": false,
    "_shards": {
        "total": 3,
        "successful": 3,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 4,
            "relation": "eq"
        },
        "max_score": 0.5,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "7yaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "entire",
                    "doc_index": 8242,
                    "doc_price": 350
                },
                "sort": [
                    350
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "8CaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "idea",
                    "doc_index": 5212,
                    "doc_price": 200
                },
                "sort": [
                    200
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "6yaM4JABZkI1FQv8AwoM",
                "_score": null,
                "_source": {
                    "category": "permission",
                    "doc_keyword": "workable",
                    "doc_index": 4976,
                    "doc_price": 100
                },
                "sort": [
                    100
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "7iaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "editor",
                    "doc_index": 9871,
                    "doc_price": 30
                },
                "sort": [
                    30
                ]
            }
        ]
    }
}
```

在下列範例中，排序依 `_id` 套用：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "term": {
            "category": "permission"
          }
        },
        {
          "bool": {
            "should": [
              {
                "term": {
                  "category": "editor"
                }
              },
              {
                "term": {
                  "category": "statement"
                }
              }
            ]
          }
        }
      ]
    }
  },
  "sort":[
     {
        "_id": {
          "order": "desc"   
        }
     } 
  ]
}
```
{% include copy-curl.html %}

回應包含依 `_id` 遞減排序的相符文件：

```json
{
    "took": 33,
    "timed_out": false,
    "_shards": {
        "total": 3,
        "successful": 3,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 4,
            "relation": "eq"
        },
        "max_score": 0.5,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "8CaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "idea",
                    "doc_index": 5212,
                    "doc_price": 200
                },
                "sort": [
                    "8CaM4JABZkI1FQv8AwoN"
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "7yaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "entire",
                    "doc_index": 8242,
                    "doc_price": 350
                },
                "sort": [
                    "7yaM4JABZkI1FQv8AwoN"
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "7iaM4JABZkI1FQv8AwoN",
                "_score": null,
                "_source": {
                    "category": "editor",
                    "doc_index": 9871,
                    "doc_price": 30
                },
                "sort": [
                    "7iaM4JABZkI1FQv8AwoN"
                ]
            },
            {
                "_index": "my-nlp-index",
                "_id": "6yaM4JABZkI1FQv8AwoM",
                "_score": null,
                "_source": {
                    "category": "permission",
                    "doc_keyword": "workable",
                    "doc_index": 4976,
                    "doc_price": 100
                },
                "sort": [
                    "6yaM4JABZkI1FQv8AwoM"
                ]
            }
        ]
    }
}
```
