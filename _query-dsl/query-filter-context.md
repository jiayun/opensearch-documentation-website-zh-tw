---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢與篩選情境"
nav_order: 5
redirect_from:
  - /opensearch/query-dsl/query-filter-context/
  - /query-dsl/query-dsl/query-filter-context/
---

# 查詢與篩選情境

查詢由查詢子句組成，這些子句可以在[_篩選情境_](#filter-context)或[_查詢情境_](#query-context)中執行。篩選情境中的查詢子句會問「文件_是否_符合該查詢子句？」並回傳符合的文件。查詢情境中的查詢子句會問「文件符合該查詢子句的程度_如何_？」，回傳符合的文件，並以[_相關性分數_](#relevance-score)的形式提供每份文件的相關性。

## 相關性分數

_相關性分數_衡量文件與查詢的符合程度。它是一個正浮點數，OpenSearch 會將它記錄在每份文件的 `_score` 中繼資料欄位中：

```json
"hits": [
  {
    "_index": "blog-posts",
    "_id": "1",
    "_score": 0.16890505,
    "_source": {
      "title": "Getting started with vector search",
      "content": "Vector search finds documents with similar meaning by comparing embeddings.",
      "status": "published",
      "publish_date": "2025-03-10"
    }
  },
  ...
]
```

分數越高表示文件越相關。雖然不同的查詢類型計算相關性分數的方式不同，但所有查詢類型都會考量查詢子句是在篩選情境還是查詢情境中執行。

請將會影響相關性分數的查詢子句放在查詢情境中，並將所有其他查詢子句放在篩選情境中。
{: .tip}

## 範例資料

本頁的範例使用一個部落格文章索引。若要試用這些範例，請建立索引：

```json
PUT blog-posts
{
  "mappings": {
    "properties": {
      "title":        { "type": "text" },
      "content":      { "type": "text" },
      "status":       { "type": "keyword" },
      "publish_date": { "type": "date" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件加入索引：

```json
POST blog-posts/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "title": "Getting started with vector search", "content": "Vector search finds documents with similar meaning by comparing embeddings.", "status": "published", "publish_date": "2025-03-10" }
{ "index": { "_id": "2" } }
{ "title": "Tuning vector search performance", "content": "Learn how to tune vector search using quantization and caching.", "status": "published", "publish_date": "2025-06-02" }
{ "index": { "_id": "3" } }
{ "title": "Keyword search basics", "content": "Keyword search matches the exact terms in your query.", "status": "published", "publish_date": "2025-01-20" }
{ "index": { "_id": "4" } }
{ "title": "Hybrid search explained", "content": "Hybrid search combines keyword search and vector search results.", "status": "draft", "publish_date": "2025-08-15" }
{ "index": { "_id": "5" } }
{ "title": "A year of vector search", "content": "A look back at the vector search features released in 2024.", "status": "published", "publish_date": "2024-11-05" }
```
{% include copy-curl.html %}

## 篩選情境

篩選情境中的查詢子句會問「文件_是否_符合該查詢子句？」，這是一個二元答案。例如，您可以使用篩選情境來回答關於部落格文章的下列問題：

- 文章的 `status` 是否設定為 `published`？
- 文章的 `publish_date` 是否在 2025 年？

使用篩選情境時，OpenSearch 會回傳符合的文件，而不計算相關性分數。因此，對於具有精確值的欄位，您應該使用篩選情境。

若要在篩選情境中執行查詢子句，請將它傳遞給 `filter` 參數。例如，下列布林查詢會搜尋 2025 年發布的文章：

```json
GET blog-posts/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "status": "published" }},
        { "range": { "publish_date": { "gte": "2025-01-01", "lte": "2025-12-31" }}}
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含 2025 年發布的三篇文章。每份文件的 `_score` 都是 `0.0`，因為篩選子句不會計算相關性：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 5,
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
    "max_score": 0.0,
    "hits": [
      {
        "_index": "blog-posts",
        "_id": "1",
        "_score": 0.0,
        "_source": {
          "title": "Getting started with vector search",
          "content": "Vector search finds documents with similar meaning by comparing embeddings.",
          "status": "published",
          "publish_date": "2025-03-10"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "2",
        "_score": 0.0,
        "_source": {
          "title": "Tuning vector search performance",
          "content": "Learn how to tune vector search using quantization and caching.",
          "status": "published",
          "publish_date": "2025-06-02"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "3",
        "_score": 0.0,
        "_source": {
          "title": "Keyword search basics",
          "content": "Keyword search matches the exact terms in your query.",
          "status": "published",
          "publish_date": "2025-01-20"
        }
      }
    ]
  }
}
```
</details>

為了提升效能，OpenSearch 會快取經常使用的篩選器。

## 查詢情境

查詢情境中的查詢子句會問「文件符合該查詢子句的程度_如何_？」，這沒有二元答案。查詢情境適合全文搜尋，此時您不僅想取得符合的文件，還想判斷每份文件的相關性。例如，您可以使用查詢情境來尋找關於向量搜尋的部落格文章。

使用查詢情境時，每份符合的文件都會在 `_score` 欄位中包含相關性分數，您可以用它依相關性對文件[排序]({{site.url}}{{site.baseurl}}/opensearch/search/sort/)。

若要在查詢情境中執行查詢子句，請將它傳遞給 `query` 參數。例如，下列查詢會搜尋內容符合 `vector search` 這些字詞的文章：

```json
GET blog-posts/_search
{
  "query": {
    "match": {
      "content": "vector search"
    }
  }
}
```
{% include copy-curl.html %}

回應包含全部五篇文章，因為每篇至少包含其中一個字詞。文章依相關性分數排序。文件 4 的分數最高，因為它包含 `search` 三次；文件 3 的分數最低，因為它只包含 `search`：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 0.1985399,
    "hits": [
      {
        "_index": "blog-posts",
        "_id": "4",
        "_score": 0.1985399,
        "_source": {
          "title": "Hybrid search explained",
          "content": "Hybrid search combines keyword search and vector search results.",
          "status": "draft",
          "publish_date": "2025-08-15"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "1",
        "_score": 0.16890505,
        "_source": {
          "title": "Getting started with vector search",
          "content": "Vector search finds documents with similar meaning by comparing embeddings.",
          "status": "published",
          "publish_date": "2025-03-10"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "2",
        "_score": 0.16890505,
        "_source": {
          "title": "Tuning vector search performance",
          "content": "Learn how to tune vector search using quantization and caching.",
          "status": "published",
          "publish_date": "2025-06-02"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "5",
        "_score": 0.16219063,
        "_source": {
          "title": "A year of vector search",
          "content": "A look back at the vector search features released in 2024.",
          "status": "published",
          "publish_date": "2024-11-05"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "3",
        "_score": 0.040917058,
        "_source": {
          "title": "Keyword search basics",
          "content": "Keyword search matches the exact terms in your query.",
          "status": "published",
          "publish_date": "2025-01-20"
        }
      }
    ]
  }
}
```
</details>

相關性分數是具有 24 位元有效位數精確度的單精度浮點數。如果分數計算超出有效位數精確度，可能會發生精確度損失。
{: .note}

## 結合查詢與篩選情境

單一布林查詢可以同時包含兩種情境中的子句。`must` 和 `should` 參數中的子句在查詢情境中執行，並計入 `_score`。`filter` 和 `must_not` 參數中的子句在篩選情境中執行，僅用於納入或排除文件。如需更多資訊，請參閱 [布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)。

下列查詢結合了前面兩個範例。`must` 參數中的 `match` 子句計算相關性分數，而 `filter` 參數中的 `term` 和 `range` 子句將結果限制為 2025 年發布的文章：

```json
GET blog-posts/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "content": "vector search" }}
      ],
      "filter": [
        { "term": { "status": "published" }},
        { "range": { "publish_date": { "gte": "2025-01-01", "lte": "2025-12-31" }}}
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含與篩選情境範例相同的三份文件，並依相關性排序。文件 4 被排除，因為它是草稿；文件 5 被排除，因為它發布於 2024 年。每份文件的 `_score` 與查詢情境範例中相同，因為篩選子句不會影響分數：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 5,
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
    "max_score": 0.16890505,
    "hits": [
      {
        "_index": "blog-posts",
        "_id": "1",
        "_score": 0.16890505,
        "_source": {
          "title": "Getting started with vector search",
          "content": "Vector search finds documents with similar meaning by comparing embeddings.",
          "status": "published",
          "publish_date": "2025-03-10"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "2",
        "_score": 0.16890505,
        "_source": {
          "title": "Tuning vector search performance",
          "content": "Learn how to tune vector search using quantization and caching.",
          "status": "published",
          "publish_date": "2025-06-02"
        }
      },
      {
        "_index": "blog-posts",
        "_id": "3",
        "_score": 0.040917058,
        "_source": {
          "title": "Keyword search basics",
          "content": "Keyword search matches the exact terms in your query.",
          "status": "published",
          "publish_date": "2025-01-20"
        }
      }
    ]
  }
}
```
</details>
