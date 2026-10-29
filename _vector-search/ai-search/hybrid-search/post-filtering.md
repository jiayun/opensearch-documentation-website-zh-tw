---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用後置篩選的混合搜尋"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 40
---

# 使用後置篩選的混合搜尋
**於 2.13 版推出**
{: .label .label-purple }

您可以在查詢中提供 `post_filter` 參數，對混合搜尋結果執行後置篩選。

`post_filter` 子句會在擷取搜尋結果之後套用。後置篩選適合用來對搜尋結果套用額外的篩選條件。由於正規化處理器會在篩選後的結果上執行，因此這些結果的分數會再次正規化。如需更多資訊，請參閱[後置篩選如何影響搜尋結果與評分](#how-post-filtering-affects-search-results-and-scoring)。

後置篩選不會影響彙總結果。
{: .note}

若要在查詢執行期間篩選所有子查詢，而非篩選最終結果，請使用通用篩選條件。如需更多資訊，請參閱[使用前置篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pre-filtering/)。

## 範例：使用後置篩選的多面向搜尋

後置篩選常用於多面向搜尋，此類搜尋的介面會在搜尋結果旁顯示彙總計數（例如品牌、顏色與尺寸篩選條件）。使用 `post_filter` 可讓彙總計數以未篩選的完整查詢為基礎，同時只篩選顯示的命中結果。

首先，將產品文件匯入索引：

```json
POST /_bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "Nike Air Max", "brand": "Nike", "color": "Red", "size": 10, "price": 120, "category": "Running Shoes", "description": "Cushioned running shoes for daily training" }
{ "index": { "_index": "products", "_id": "2" } }
{ "name": "Nike Pegasus", "brand": "Nike", "color": "Black", "size": 9, "price": 130, "category": "Running Shoes", "description": "Responsive shoes for road running" }
{ "index": { "_index": "products", "_id": "3" } }
{ "name": "Adidas Adizero", "brand": "Adidas", "color": "White", "size": 10, "price": 160, "category": "Running Shoes", "description": "Lightweight racing shoes" }
{ "index": { "_index": "products", "_id": "4" } }
{ "name": "Puma Velocity", "brand": "Puma", "color": "Black", "size": 8, "price": 110, "category": "Running Shoes", "description": "Cushioned shoes for long runs" }
{ "index": { "_index": "products", "_id": "5" } }
{ "name": "Adidas Ultraboost", "brand": "Adidas", "color": "Black", "size": 9, "price": 180, "category": "Running Shoes", "description": "Running shoes with responsive cushioning" }
{ "index": { "_index": "products", "_id": "6" } }
{ "name": "Nike Pegasus Trail", "brand": "Nike", "color": "White", "size": 10, "price": 140, "category": "Trail Running Shoes", "description": "Trail running shoes with a grippy outsole" }
{ "index": { "_index": "products", "_id": "7" } }
{ "name": "Merrell Moab", "brand": "Merrell", "color": "Brown", "size": 10, "price": 130, "category": "Hiking Boots", "description": "Waterproof boots for mountain trails" }
```
{% include copy-curl.html %}

下列搜尋使用名為 `nlp-search-pipeline` 的搜尋管線，其中包含採用 `min_max` 正規化技術與 `arithmetic_mean` 合併技術的 `normalization-processor`。如需詳細資訊，請參閱[設定搜尋管線]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/#step-3-configure-a-search-pipeline)。

使用者搜尋「running shoes」，應用程式會建構混合查詢，比對 `category` 與 `description` 欄位中的文字。此查詢包含品牌、顏色與尺寸的彙總：

```json
GET /products/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "category": "running shoes"
          }
        },
        {
          "match": {
            "description": "running shoes"
          }
        }
      ]
    }
  },
  "aggs": {
    "brands": {
      "terms": { "field": "brand.keyword" }
    },
    "colors": {
      "terms": { "field": "color.keyword" }
    },
    "sizes": {
      "terms": { "field": "size" }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回符合查詢之所有品牌的命中結果。彙總包含符合文件內每個品牌、顏色與尺寸的計數：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  ...
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1.0,
        "_source": {
          "name": "Nike Pegasus",
          "brand": "Nike",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "5",
        "_score": 1.0,
        "_source": {
          "name": "Adidas Ultraboost",
          "brand": "Adidas",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.9290604,
        "_source": {
          "name": "Nike Air Max",
          "brand": "Nike",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 0.56825376,
        "_source": {
          "name": "Nike Pegasus Trail",
          "brand": "Nike",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.34844735,
        "_source": {
          "name": "Adidas Adizero",
          "brand": "Adidas",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 0.3007,
        "_source": {
          "name": "Puma Velocity",
          "brand": "Puma",
          ...
        }
      }
    ]
  },
  "aggregations": {
    "brands": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        { "key": "Nike", "doc_count": 3 },
        { "key": "Adidas", "doc_count": 2 },
        { "key": "Puma", "doc_count": 1 }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        { "key": "Black", "doc_count": 3 },
        { "key": "White", "doc_count": 2 },
        { "key": "Red", "doc_count": 1 }
      ]
    },
    "sizes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        { "key": 10, "doc_count": 3 },
        { "key": 9, "doc_count": 2 },
        { "key": 8, "doc_count": 1 }
      ]
    }
  }
}
```
</details>

彙總通常會以多面向篩選條件的形式顯示在介面中。當使用者選取特定品牌（例如 `Nike`）來篩選結果時，使用前置篩選會在計算彙總之前排除非 Nike 的文件，導致其他品牌從多面向計數中消失。

使用 `post_filter` 時，查詢與彙總會在完整結果集上執行。篩選條件只會套用至顯示的命中結果：

```json
GET /products/_search?search_pipeline=nlp-search-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "category": "running shoes"
          }
        },
        {
          "match": {
            "description": "running shoes"
          }
        }
      ]
    }
  },
  "aggs": {
    "brands": {
      "terms": { "field": "brand.keyword" }
    },
    "colors": {
      "terms": { "field": "color.keyword" }
    }
  },
  "post_filter": {
    "term": { "brand.keyword": "Nike" }
  }
}
```
{% include copy-curl.html %}

命中結果只包含 Nike 產品，但彙總仍反映未篩選的完整查詢。如[後置篩選如何影響搜尋結果與評分](#how-post-filtering-affects-search-results-and-scoring)所述，命中分數會再次以篩選後的命中結果進行正規化：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "products",
        "_id": "2",
        "_score": 1.0,
        "_source": {
          "name": "Nike Pegasus",
          "brand": "Nike",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.62393653,
        "_source": {
          "name": "Nike Air Max",
          "brand": "Nike",
          ...
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 0.001,
        "_source": {
          "name": "Nike Pegasus Trail",
          "brand": "Nike",
          ...
        }
      }
    ]
  },
  "aggregations": {
    "brands": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        { "key": "Nike", "doc_count": 3 },
        { "key": "Adidas", "doc_count": 2 },
        { "key": "Puma", "doc_count": 1 }
      ]
    },
    "colors": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        { "key": "Black", "doc_count": 3 },
        { "key": "White", "doc_count": 2 },
        { "key": "Red", "doc_count": 1 }
      ]
    }
  }
}
```
</details>

所有品牌選項仍會顯示在多面向篩選條件中，讓使用者可以切換品牌或比較計數，而不必移除篩選條件。

## 後置篩選對搜尋結果和評分的影響

後置篩選可能會大幅改變最終搜尋結果和文件分數。請考慮下列情境。

### 單一查詢情境

假設有一個查詢會傳回下列結果：
- 正規化前的查詢結果：`[d2: 5.0, d4: 3.0, d1: 2.0]`
- 正規化分數：`[d2: 1.0, d4: 0.33, d1: 0.0]`

對初始查詢結果套用後置篩選後，結果如下：
- 後置篩選相符項目 `[d2, d4]`
- 產生的分數：`[d2: 1.0, d4: 0.0]`

請注意，套用後置篩選後，文件 `d4` 的分數如何從 `0.33` 變成 `0.0`。

### 多重查詢情境

假設有一個包含兩個子查詢的查詢：
- 查詢 1 結果：`[d2: 5.0, d4: 3.0, d1: 2.0]`
- 查詢 2 結果：`[d1: 1.0, d5: 0.5, d4: 0.25]`
- 正規化分數：
  - 查詢 1：`[d2: 1.0, d4: 0.33, d1: 0.0]`
  - 查詢 2：`[d1: 1.0, d5: 0.33, d4: 0.0]`
- 合併的初始分數：`[d2: 1.0, d1: 0.5, d5: 0.33, d4: 0.165]`

對初始查詢結果套用後置篩選後，結果如下：
- 後置篩選相符項目 `[d2, d4]`
- 產生的分數：
  - 查詢 1：`[d2: 5.0, d4: 3.0]`
  - 查詢 2：`[d4: 0.25]`
- 正規化分數：
  - 查詢 1：`[d2: 1.0, d4: 0.0]`
  - 查詢 2：`[d4: 1.0]`
- 合併的最終分數：`[d2: 1.0, d4: 0.5]`

請注意：
- 文件 `d2` 的分數維持不變。
- 文件 `d4` 的分數已變更。
