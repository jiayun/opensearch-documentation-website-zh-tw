---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "偵錯搜尋管線"
nav_order: 25
has_children: false
parent: Search pipelines
---


# 偵錯搜尋管線

`verbose_pipeline` 參數提供搜尋管線中搜尋請求、搜尋回應及搜尋階段處理器的資料流程與轉換詳細資訊。它有助於疑難排解及最佳化管線，並確保處理搜尋請求和回應時的透明度。

## 啟用偵錯

若要啟用管線偵錯，請在搜尋請求中將 `verbose_pipeline=true` 指定為查詢參數。此功能適用於全部三種搜尋管線方法：

- [預設搜尋管線](#default-search-pipeline)
- [特定搜尋管線](#specific-search-pipeline)
- [臨時搜尋管線](#temporary-search-pipeline)

### 預設搜尋管線

若要在預設搜尋管線中使用 `verbose_pipeline`，請在索引設定中將該管線設為預設，並在查詢中加入 `verbose_pipeline=true`：

```json
PUT /my_index/_settings
{
  "index.search.default_pipeline": "my_pipeline"
}
```
{% include copy-curl.html %}

```json
GET /my_index/_search?verbose_pipeline=true
```
{% include copy-curl.html %}

如需預設搜尋管線的詳細資訊，請參閱[為索引中的所有請求設定預設管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/#default-search-pipeline)。

### 特定搜尋管線

若要在特定搜尋管線中使用 `verbose_pipeline`，請指定管線 ID，並在查詢中加入 `verbose_pipeline=true`：

```json
GET /my_index/_search?search_pipeline=my_pipeline&verbose_pipeline=true
```
{% include copy-curl.html %}

如需使用特定搜尋管線的詳細資訊，請參閱[為請求指定現有管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/#specifying-an-existing-search-pipeline-for-a-request)。

### 臨時搜尋管線

若要在臨時搜尋管線中使用 `verbose_pipeline`，請直接在請求本文中定義管線，並在查詢中加入 `verbose_pipeline=true`：

```json
POST /my_index/_search?verbose_pipeline=true
{
  "query": {
    "match": { "text_field": "some search text" }
  },
  "search_pipeline": {
    "request_processors": [
      {
        "filter_query": {
          "query": { "term": { "visibility": "public" } }
        }
      }
    ],
    "response_processors": [
      {
        "collapse": {
          "field": "category"
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

如需使用臨時搜尋管線的詳細資訊，請參閱[為請求使用臨時管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/using-search-pipeline/#using-a-temporary-search-pipeline-for-a-request)。

## 回應範例

啟用 `verbose_pipeline` 參數時，回應會包含額外的 `processor_results` 欄位，提供管線中每個處理器所套用轉換的相關資訊：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
    "took": 27,
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
        "max_score": 0.18232156,
        "hits": [
            {
                "_index": "my_index",
                "_id": "1",
                "_score": 0.18232156,
                "_source": {
                    "notification": "This is a public message",
                    "visibility": "public"
                }
            }
        ]
    },
    "processor_results": [
        {
            "processor_name": "filter_query",
            "tag": "tag1",
            "duration_millis": 288541,
            "status": "success",
            "input_data": {
                "verbose_pipeline": true,
                "query": {
                    "bool": {
                        "adjust_pure_negative": true,
                        "must": [
                            {
                                "match": {
                                    "message": {
                                        "auto_generate_synonyms_phrase_query": true,
                                        "query": "this",
                                        "zero_terms_query": "NONE",
                                        "fuzzy_transpositions": true,
                                        "boost": 1.0,
                                        "prefix_length": 0,
                                        "operator": "OR",
                                        "lenient": false,
                                        "max_expansions": 50
                                    }
                                }
                            }
                        ],
                        "boost": 1.0
                    }
                }
            },
            "output_data": {
                "verbose_pipeline": true,
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "term": {
                                    "visibility": {
                                        "boost": 1.0,
                                        "value": "public"
                                    }
                                }
                            }
                        ],
                        "adjust_pure_negative": true,
                        "must": [
                            {
                                "bool": {
                                    "adjust_pure_negative": true,
                                    "must": [
                                        {
                                            "match": {
                                                "message": {
                                                    "auto_generate_synonyms_phrase_query": true,
                                                    "query": "this",
                                                    "zero_terms_query": "NONE",
                                                    "fuzzy_transpositions": true,
                                                    "boost": 1.0,
                                                    "prefix_length": 0,
                                                    "operator": "OR",
                                                    "lenient": false,
                                                    "max_expansions": 50
                                                }
                                            }
                                        }
                                    ],
                                    "boost": 1.0
                                }
                            }
                        ],
                        "boost": 1.0
                    }
                }
            }
        },
        {
            "processor_name": "rename_field",
            "duration_millis": 250042,
            "status": "success",
            "input_data": [
                {
                    "_index": "my_index",
                    "_id": "1",
                    "_score": 0.18232156,
                    "_source": {
                        "message": "This is a public message",
                        "visibility": "public"
                    }
                }
            ],
            "output_data": [
                {
                    "_index": "my_index",
                    "_id": "1",
                    "_score": 0.18232156,
                    "_source": {
                        "notification": "This is a public message",
                        "visibility": "public"
                    }
                }
            ]
        }
    ]
}
```
</details>