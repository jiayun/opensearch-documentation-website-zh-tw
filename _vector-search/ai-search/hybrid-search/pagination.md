---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "混合查詢結果分頁"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 20
---

# 混合查詢結果的分頁
**於 2.19 版推出**
{: .label .label-purple }

您可以在混合查詢子句中搭配標準的 `from` 與 `size` 參數，使用 `pagination_depth` 參數來為混合查詢結果分頁。`pagination_depth` 參數定義每個子查詢可從每個分片擷取的最大搜尋結果數。例如，將 `pagination_depth` 設為 `50`，即可讓每個分片在記憶體中為每個子查詢保留最多 50 筆結果。

`from` 值大於 `0` 的混合查詢必須指定 `pagination_depth`。`pagination_depth` 值不得超過 `index.max_result_window` 索引設定。

若要瀏覽結果，請使用 `from` 與 `size` 參數：

- `from`：指定要從哪一筆文件編號開始顯示結果。預設值為 `0`。
- `size`：指定每頁要傳回的結果數。預設值為 `10`。

例如，若要略過前 20 筆文件並顯示接下來 10 筆，請指定 `from: 20` 與 `size: 10`。如需分頁的詳細資訊，請參閱[為結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。

## 必要條件

本頁的範例使用 `my-nlp-index` 索引與 `nlp-search-pipeline` 搜尋管線。若要建立索引並將文件匯入，請依照[結合混合搜尋與彙總]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/aggregations/)中的步驟操作。若要建立搜尋管線，請參閱[步驟 3：設定搜尋管線]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/#step-3-configure-a-search-pipeline)。

## pagination_depth 對混合搜尋結果的影響

變更 `pagination_depth` 會影響在套用任何排名、篩選或分頁調整之前所擷取的基礎搜尋結果集。這是因為 `pagination_depth` 決定從每個分片針對每個子查詢擷取的結果數量，而這最終可能改變正規化後的結果順序。為確保分頁一致，在頁面之間瀏覽時請保持 `pagination_depth` 值不變。  

依預設，未分頁的混合搜尋會使用 `from + size` 公式擷取結果，其中 `from` 一律為 `0`。
{: .note}  

若要啟用更深層的分頁，請增加 `pagination_depth` 值。接著您可以使用 `from` 和 `size` 參數瀏覽結果。請注意，更深層的分頁可能影響搜尋效能，因為擷取和處理更多結果需要額外的運算資源。

下列範例顯示設定了 `from: 0`、`size: 2` 和 `pagination_depth: 10` 的搜尋請求。這表示在套用分頁之前，`bool` 和 `term` 查詢都會從每個分片擷取最多 10 筆搜尋結果：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "size": 2,
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

回應包含四份相符文件中的前兩份：

```json
{
    "hits": {
        "total": {
            "value": 4,
            "relation": "eq"
        },
        "max_score": 0.7,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "eneXlZQBJkWerFzHv4eW",
                "_score": 0.7,
                "_source": {
                    "category": "editor",
                    "doc_index": 9871,
                    "doc_price": 30
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "e3eXlZQBJkWerFzHv4eW",
                "_score": 0.7,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "entire",
                    "doc_index": 8242,
                    "doc_price": 350
                }
            }
        ]
    }
}
```

下列搜尋請求設定了 `from: 2`、`size: 2` 和 `pagination_depth: 10`。`pagination_depth` 保持不變，以確保分頁是根據同一組搜尋結果：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "size": 2,
  "from": 2,
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

回應會略過前兩份文件，並包含接下來兩份：

```json
{
    "hits": {
        "total": {
            "value": 4,
            "relation": "eq"
        },
        "max_score": 0.7,
        "hits": [
            {
                "_index": "my-nlp-index",
                "_id": "fHeXlZQBJkWerFzHv4eW",
                "_score": 0.7,
                "_source": {
                    "category": "statement",
                    "doc_keyword": "idea",
                    "doc_index": 5212,
                    "doc_price": 200
                }
            },
            {
                "_index": "my-nlp-index",
                "_id": "d3eXlZQBJkWerFzHv4eV",
                "_score": 0.3,
                "_source": {
                    "category": "permission",
                    "doc_keyword": "workable",
                    "doc_index": 4976,
                    "doc_price": 100
                }
            }
        ]
    }
}
```

