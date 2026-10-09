---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用預先篩選的混合搜尋"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 38
---

# 使用預先篩選的混合搜尋
**3.0 版新增**
{: .label .label-purple }

您可以在混合搜尋中提供頂層 `filter` 參數（置於 `hybrid` 查詢中），對混合搜尋結果執行預先篩選。

`filter` 會在查詢執行期間套用至每個子查詢，因此只有符合篩選條件的文件會被評分。預先篩選適用於將同一篩選條件套用至所有子查詢，而無須在每個子查詢中重複撰寫。

`filter` 必須是單一查詢物件。
{: .note}

若要在最終結果擷取後再進行篩選，而不是在執行期間篩選每個子查詢，請使用後置篩選 (post-filter)。如需更多資訊，請參閱[使用後置篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/post-filtering/)。

## 範例

下列範例請求結合 `match` 查詢與 `knn` 查詢，並套用一個共用的 `filter`，將兩個子查詢限制在 `shoes` 類別：

```json
POST /products/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "filter": {
        "term": { "category": "shoes" }
      },
      "queries": [
        {
          "match": { "description": "running shoes" }
        },
        {
          "knn": {
            "embedding": {
              "vector": [1.23, 0.45, 0.67, ...],
              "k": 10
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會將 `category: shoes` 篩選套用至 `match` 與 `knn` 兩個子查詢，這等同於下列將篩選分別套用至每個子查詢的查詢：

```json
POST /products/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "bool": {
            "must": {
              "match": { "description": "running shoes" }
            },
            "filter": {
              "term": { "category": "shoes" }
            }
          }
        },
        {
          "knn": {
            "embedding": {
              "vector": [1.23, 0.45, 0.67, ...],
              "k": 10,
              "filter": {
                "term": { "category": "shoes" }
              }
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 依多個條件篩選

由於 `filter` 必須是單一查詢物件，請使用[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)結合多個條件。下列範例將結果篩選為僅包含有現貨的鞋子：

```json
"filter": {
  "bool": {
    "must": [
      { "term": { "category": "shoes" }},
      { "term": { "in_stock": true }}
    ]
  }
}
```

## 結合共用篩選與子查詢篩選

子查詢除了共用篩選之外，也可以定義自己的篩選。在此情況下，OpenSearch 會使用邏輯 `AND` 結合兩者，進一步縮小該子查詢的結果範圍。

在下列範例中，共用篩選將所有子查詢限制在 `shoes` 類別，而 `match` 子查詢則另外縮小至 `nike` 品牌：

```json
POST /products/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "filter": {
        "term": { "category": "shoes" }
      },
      "queries": [
        {
          "bool": {
            "must": {
              "match": { "description": "running shoes" }
            },
            "filter": {
              "term": { "brand": "nike" }
            }
          }
        },
        {
          "knn": {
            "embedding": {
              "vector": [1.23, 0.45, 0.67, ...],
              "k": 10
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}
