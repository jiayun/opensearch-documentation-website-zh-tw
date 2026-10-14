---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢與篩選上下文"
nav_order: 5
redirect_from:
  - /opensearch/query-dsl/query-filter-context/
  - /query-dsl/query-dsl/query-filter-context/
---

# 查詢與篩選上下文

查詢由查詢子句組成，這些子句可以在[_篩選上下文_](#filter-context)或[_查詢上下文_](#query-context)中執行。篩選上下文中的查詢子句提出的問題是「文件_是否_符合該查詢子句？」，並傳回符合的文件。查詢上下文中的查詢子句提出的問題是「文件_有多符合_該查詢子句？」，除了傳回符合的文件之外，還會以[_相關性分數_](#relevance-score)的形式提供每份文件的相關性。

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

分數越高，表示文件的相關性越高。雖然不同的查詢類型計算相關性分數的方式不同，但所有查詢類型都會考量查詢子句是在篩選上下文還是查詢上下文中執行。

若要影響相關性分數，請將查詢子句放在查詢上下文中，其餘所有查詢子句則放在篩選上下文中。
{: .tip}

## 範例資料

本頁的範例使用一個部落格文章索引。若要試用這些範例，請先建立索引：

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

## 篩選上下文

篩選上下文中的查詢子句提出的問題是「文件_是否_符合該查詢子句？」，其答案只有是或否兩種。例如，您可以使用篩選上下文來回答關於部落格文章的下列問題：

- 文章的 `status` 是否設定為 `published`？
- 文章的 `publish_date` 是否在 2025 年？

使用篩選上下文時，OpenSearch 會傳回符合的文件，而不計算相關性分數。因此，對於具有精確值的欄位，您應該使用篩選上下文。

若要在篩選上下文中執行查詢子句，請將它傳遞給 `filter` 參數。例如，下列布林查詢會搜尋 2025 年發布的文章：

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

為了提升效能，OpenSearch 會快取經常使用的篩選條件。

## 查詢上下文

查詢上下文中的查詢子句提出的問題是「文件_有多符合_該查詢子句？」，其答案並非只有是或否。查詢上下文適合全文搜尋，在這種情況下，您不僅想取得符合的文件，還想判斷每份文件的相關性。例如，您可以使用查詢上下文來尋找關於向量搜尋的部落格文章。

使用查詢上下文時，每份符合的文件都會在 `_score` 欄位中包含相關性分數，您可以用它依相關性對文件進行[排序]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。

若要在查詢上下文中執行查詢子句，請將它傳遞給 `query` 參數。例如，下列查詢會搜尋內容符合 `vector search` 這些字詞的文章：

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

回應包含全部五篇文章，因為每篇文章至少包含其中一個字詞。文章會依相關性分數排序。文件 4 的分數最高，因為它包含 `search` 三次；文件 3 的分數最低，因為它只包含 `search`：

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

相關性分數是具有 24 位元有效位數精確度的單精確度浮點數。若分數計算超出有效位數的精確度，可能會發生精確度損失。
{: .note}

## 結合查詢與篩選上下文

單一布林查詢可以同時包含兩種上下文的子句。`must` 與 `should` 參數中的子句會在查詢上下文中執行，並影響 `_score`。`filter` 與 `must_not` 參數中的子句會在篩選上下文中執行，只會納入或排除文件。如需更多資訊，請參閱[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)。

下列查詢結合了前兩個範例。`must` 參數中的 `match` 子句會計算相關性分數，而 `filter` 參數中的 `term` 與 `range` 子句會將結果限制為 2025 年發布的文章：

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

回應包含與篩選上下文範例相同的三份文件，並依相關性排序。文件 4 因為是草稿而被排除，文件 5 則因為是在 2024 年發布而被排除。每份文件的 `_score` 都與查詢上下文範例中的相同，因為篩選子句不會影響分數：

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

## 相關文件

- [布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)
- [常數分數查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/constant-score/)
- [詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/)
- [全文查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/index/)
- [排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)
