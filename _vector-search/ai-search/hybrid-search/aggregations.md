---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "結合混合搜尋與彙總"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 50
---

# 結合混合搜尋與彙總
**於 2.13 版推出**
{: .label .label-purple }

您可以將混合查詢子句與 OpenSearch 支援的任何彙總結合，以強化搜尋結果。彙總可讓您將 OpenSearch 當作分析引擎使用。如需彙總的詳細資訊，請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。

大多數彙總都是在混合查詢所傳回的文件子集上執行。唯一會對所有文件執行的彙總是 [`global`]({{site.url}}{{site.baseurl}}/aggregations/bucket/global/) 彙總。

若要將彙總與混合查詢搭配使用，請先建立索引。彙總通常用於特殊類型的欄位，例如 `keyword` 或 `integer`。下列範例會建立包含數個這類欄位的索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "number_of_shards": 2
  },
  "mappings": {
    "properties": {
      "doc_index": {
        "type": "integer"
      },
      "doc_keyword": {
        "type": "keyword"
      },
      "category": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列請求會將六份文件匯入您的新索引：

```json
POST /_bulk
{ "index": { "_index": "my-nlp-index" } }
{ "category": "permission", "doc_keyword": "workable", "doc_index": 4976, "doc_price": 100}
{ "index": { "_index": "my-nlp-index" } }
{ "category": "sister", "doc_keyword": "angry", "doc_index": 2231, "doc_price": 200 }
{ "index": { "_index": "my-nlp-index" } }
{ "category": "hair", "doc_keyword": "likeable", "doc_price": 25 }
{ "index": { "_index": "my-nlp-index" } }
{ "category": "editor", "doc_index": 9871, "doc_price": 30 }
{ "index": { "_index": "my-nlp-index" } }
{ "category": "statement", "doc_keyword": "entire", "doc_index": 8242, "doc_price": 350  } 
{ "index": { "_index": "my-nlp-index" } }
{ "category": "statement", "doc_keyword": "idea", "doc_index": 5212, "doc_price": 200  } 
{ "index": { "_index": "index-test" } }
{ "category": "editor", "doc_keyword": "bubble", "doc_index": 1298, "doc_price": 130 } 
{ "index": { "_index": "index-test" } }
{ "category": "editor", "doc_keyword": "bubble", "doc_index": 521, "doc_price": 75  } 
```
{% include copy-curl.html %}

現在您可以將混合查詢子句與 `min` 彙總結合：

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
  "aggs": {
    "total_price": {
      "sum": {
        "field": "doc_price"
      }
    },
    "keywords": {
      "terms": {
        "field": "doc_keyword",
        "size": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含相符的文件與彙總結果：

```json
{
  "took": 9,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
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
        "_id": "mHRPNY4BlN82W_Ar9UMY",
        "_score": 0.5,
        "_source": {
          "doc_price": 100,
          "doc_index": 4976,
          "doc_keyword": "workable",
          "category": "permission"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "m3RPNY4BlN82W_Ar9UMY",
        "_score": 0.5,
        "_source": {
          "doc_price": 30,
          "doc_index": 9871,
          "category": "editor"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "nXRPNY4BlN82W_Ar9UMY",
        "_score": 0.5,
        "_source": {
          "doc_price": 200,
          "doc_index": 5212,
          "doc_keyword": "idea",
          "category": "statement"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "nHRPNY4BlN82W_Ar9UMY",
        "_score": 0.5,
        "_source": {
          "doc_price": 350,
          "doc_index": 8242,
          "doc_keyword": "entire",
          "category": "statement"
        }
      }
    ]
  },
  "aggregations": {
    "total_price": {
      "value": 680
    },
    "doc_keywords": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "entire",
          "doc_count": 1
        },
        {
          "key": "idea",
          "doc_count": 1
        },
        {
          "key": "workable",
          "doc_count": 1
        }
      ]
    }
  }
}
```