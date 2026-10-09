---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合查詢結果分頁"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 20
---

# 混合查詢結果分頁
**2.19 版新增**
{: .label .label-purple }

您可以在混合查詢子句中使用 `pagination_depth` 參數，搭配標準的 `from` 與 `size` 參數，對混合查詢結果進行分頁。`pagination_depth` 參數定義每個子查詢從每個分片可擷取的最大搜尋結果數量。例如，將 `pagination_depth` 設為 `50`，可讓每個子查詢從每個分片在記憶體中保留最多 50 筆結果。

若要瀏覽結果，請使用 `from` 與 `size` 參數：

- `from`：指定開始顯示結果的文件編號。預設為 `0`。
- `size`：指定每頁傳回的結果數量。預設為 `10`。

例如，若要從第 20 筆文件開始顯示 10 筆文件，請指定 `from: 20` 與 `size: 10`。如需分頁的更多資訊，請參閱 [分頁顯示結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。

### pagination_depth 對混合搜尋結果的影響

變更 `pagination_depth` 會影響在套用任何排名、篩選或分頁調整之前所擷取的底層搜尋結果集合。這是因為 `pagination_depth` 決定每個子查詢從每個分片擷取的結果數量，最終可能改變正規化後的結果順序。為確保分頁一致，請在翻頁時保持 `pagination_depth` 值不變。  

預設情況下，未分頁的混合搜尋會使用 `from + size` 公式擷取結果，其中 `from` 一律為 `0`。
{: .note}  

若要啟用更深的分頁，請提高 `pagination_depth` 值。接著即可使用 `from` 與 `size` 參數瀏覽結果。請注意，更深的分頁可能影響搜尋效能，因為擷取和處理更多結果需要額外的運算資源。

下列範例顯示以 `from: 0`、`size: 5` 與 `pagination_depth: 10` 設定的搜尋請求。這表示在套用分頁之前，`bool` 與 `term` 查詢各自會從每個分片擷取最多 10 筆搜尋結果：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "size": 5,      
  "query": {
    "hybrid": {
      "pagination_depth":10,  
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
  }
}
```
{% include copy-curl.html %}

回應包含前五筆結果：

```json
{
    "hits": {
        "total": {
            "value": 6,
            "relation": "eq"
        },
        "max_score": 0.5,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "d3eXlZQBJkWerFzHv4eV",
                "_score": 0.5,
                "_source": {
                    "category": "permission",
                    "doc_keyword": "workable",
                    "doc_index": 4976,
                    "doc_price": 100
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "eneXlZQBJkWerFzHv4eW",
                "_score": 0.5,
                "_source": {
                    "category": "editor",
                    "doc_index": 9871,
                    "doc_price": 30
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "e3eXlZQBJkWerFzHv4eW",
                "_score": 0.5,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "entire",
                    "doc_index": 8242,
                    "doc_price": 350
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "fHeXlZQBJkWerFzHv4eW",
                "_score": 0.24999997,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "idea",
                    "doc_index": 5212,
                    "doc_price": 200
                }
            },
            {
                "_index": "index-test",
                "_id": "fXeXlZQBJkWerFzHv4eW",
                "_score": 5.0E-4,
                "_source": {
                    "category": "editor",
                    "doc_keyword": "bubble",
                    "doc_index": 1298,
                    "doc_price": 130
                }
            }
        ]
    }
}
```

下列搜尋請求以 `from: 6`、`size: 5` 與 `pagination_depth: 10` 設定。`pagination_depth` 保持不變，以確保分頁是基於同一組搜尋結果：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "size":5,      
  "from":6,      
  "query": {
    "hybrid": {
      "pagination_depth":10,  
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
  }
}
```
{% include copy-curl.html %}

回應排除前五筆項目，並顯示其餘結果：

```json
{
    "hits": {
        "total": {
            "value": 6,
            "relation": "eq"
        },
        "max_score": 0.5,
        "hits": [
            {
                "_index": "index-test",
                "_id": "fneXlZQBJkWerFzHv4eW",
                "_score": 5.0E-4,
                "_source": {
                    "category": "editor",
                    "doc_keyword": "bubble",
                    "doc_index": 521,
                    "doc_price": 75
                }
            }
        ]
    }
}
```

