---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "合併欄位"
parent: Full-text queries
nav_order: 60
---

# 合併欄位查詢
**於 3.2 版引入**
{: .label .label-purple }

`combined_fields` 查詢將多個文字欄位視為統一欄位，使用 BM25F 演算法提供一致的相關性評分。與針對每個欄位執行個別查詢的 `multi_match` 的 [`cross_fields`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/#cross-fields) 類型不同，`combined_fields` 會一起處理所有欄位，提供更好的效能與更準確的評分。您可以套用不同的欄位權重，同時維持所有欄位的統一評分。

`combined_fields` 查詢中的所有欄位都必須是 `text` 欄位，且必須使用相同的文字分析器。
{: .note }

## 設定

若要跟著範例操作，請將一些範例文件編製索引：

```json
POST /books/_bulk
{"index":{"_id":"1"}}
{"title":"Database Systems","description":"A comprehensive guide to database design and implementation"}
{"index":{"_id":"2"}}
{"title":"Introduction to Systems","description":"This book covers database architectures and distributed systems"}
```
{% include copy-curl.html %}

## 範例

下列範例示範 `combined_fields` 查詢中的欄位權重。此查詢會在 `title` 和 `description` 欄位中搜尋「database systems」，其中 `title` 欄位的權重是 `description` 欄位的四倍：

```json
GET /books/_search
{
  "query": {
    "combined_fields": {
      "query": "database systems",
      "fields": ["title^4", "description"]
    }
  }
}
```
{% include copy-curl.html %}

回應顯示，「Database Systems」的分數明顯高於「Introduction to Systems」，因為兩個查詢詞彙都出現在權重較高的 `title` 欄位中：

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.2924412,
    "hits": [
      {
        "_index": "books",
        "_id": "1",
        "_score": 0.2924412,
        "_source": {
          "title": "Database Systems",
          "description": "A comprehensive guide to database design and implementation"
        }
      },
      {
        "_index": "books",
        "_id": "2",
        "_score": 0.2239699,
        "_source": {
          "title": "Introduction to Systems",
          "description": "This book covers database architectures and distributed systems"
        }
      }
    ]
  }
}
```

## 參數

下表列出 `combined_fields` 查詢的參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `query` | 字串 | 要搜尋的查詢字串。必要。 |
| `fields` | 字串陣列 | 要搜尋的欄位。支援欄位名稱模式，以及使用 `^` 語法指定欄位權重（例如 `title^2`）。必要。 |
| `operator` | 字串 | 用於解讀查詢字串的布林邏輯。有效值為 `OR`（預設）和 `AND`。選用。 |
| `minimum_should_match` | 字串 | 傳回文件所需符合的最少詞彙數。可以是絕對數值、百分比或兩者的組合。如需詳細資訊，請參閱[最少應符合數量]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。選用。 |
| `boost` | 浮點數 | 指定此欄位對相關性分數之權重的浮點數值。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設為 1.0。選用。 |
| `_name` | 字串 | 查詢的名稱，可用於在回應中識別此查詢。選用。 |

## 使用 AND 運算子

預設情況下，查詢使用 `OR` 運算子，這表示符合查詢中任一詞彙的文件都會傳回。您可以將其變更為 `AND`，要求所有詞彙都必須符合：

```json
GET /books/_search
{
  "query": {
    "combined_fields": {
      "query": "introduction systems",
      "fields": ["title", "description"],
      "operator": "AND"
    }
  }
}
```
{% include copy-curl.html %}

回應包含唯一一份在合併欄位中同時出現兩個詞彙（「introduction」和「systems」）的文件：

```json
{
  "took": 1,
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
    "max_score": 0.4214915,
    "hits": [
      {
        "_index": "books",
        "_id": "2",
        "_score": 0.4214915,
        "_source": {
          "title": "Introduction to Systems",
          "description": "This book covers database architectures and distributed systems"
        }
      }
    ]
  }
}
```

## 使用 minimum_should_match

`minimum_should_match` 參數可讓您指定傳回文件所需符合的最少詞彙數。例如，下列查詢要求至少 75% 的詞彙必須符合：

```json
GET /books/_search
{
  "query": {
    "combined_fields": {
      "query": "comprehensive database architectures book",
      "fields": ["title", "description"],
      "minimum_should_match": "75%"
    }
  }
}
```
{% include copy-curl.html %}

回應包含唯一一份符合 4 個查詢詞彙中至少 3 個（75%）的文件：

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
    "max_score": 0.6993829,
    "hits": [
      {
        "_index": "books",
        "_id": "2",
        "_score": 0.6993829,
        "_source": {
          "title": "Introduction to Systems",
          "description": "This book covers database architectures and distributed systems"
        }
      }
    ]
  }
}
```

## 與 multi_match cross_fields 比較

`combined_fields` 查詢與使用 `type: cross_fields` 的 `multi_match` 在計算相關性分數的方式上有所不同。雖然這兩種查詢類型都會跨多個欄位搜尋，但 `combined_fields` 使用 BM25F 演算法，在評分時將所有欄位視為單一統一欄位。這表示反向文件頻率（IDF）會跨所有欄位整體計算，而非逐一欄位計算，且詞頻正規化會考量所有欄位的合併長度。當您的欄位長度差異很大時，例如較短的標題欄位與較長的本文欄位，這種方法特別有益，因為它可避免在計算相關性時給予較短欄位過高的權重。此外，`combined_fields` 使用以詞彙為中心的比對方式，查詢詞彙可以透過任意欄位組合來符合，而不必在個別欄位內符合所有詞彙。

下列範例使用相同的查詢比較這兩種方法。

**合併欄位查詢**：

```json
GET /books/_search
{
  "query": {
    "combined_fields": {
      "query": "database systems",
      "fields": ["title", "description"]
    }
  }
}
```
{% include copy-curl.html %}

`combined_fields` 查詢會一起計算所有欄位的詞頻，提供更準確的 BM25F 評分：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.20001775,
    "hits": [
      {
        "_index": "books",
        "_id": "1",
        "_score": 0.20001775,
        "_source": {
          "title": "Database Systems",
          "description": "A comprehensive guide to database design and implementation"
        }
      },
      {
        "_index": "books",
        "_id": "2",
        "_score": 0.19373488,
        "_source": {
          "title": "Introduction to Systems",
          "description": "This book covers database architectures and distributed systems"
        }
      }
    ]
  }
}
```

**Multi_match cross_fields 查詢**：

```json
GET /books/_search
{
  "query": {
    "multi_match": {
      "query": "database systems",
      "fields": ["title", "description"],
      "type": "cross_fields"
    }
  }
}
```
{% include copy-curl.html %}

`cross_fields` 方法會針對每個欄位執行個別查詢，然後合併結果，這可能導致評分較不精確：

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.18051638,
    "hits": [
      {
        "_index": "books",
        "_id": "1",
        "_score": 0.18051638,
        "_source": {
          "title": "Database Systems",
          "description": "A comprehensive guide to database design and implementation"
        }
      },
      {
        "_index": "books",
        "_id": "2",
        "_score": 0.16574687,
        "_source": {
          "title": "Introduction to Systems",
          "description": "This book covers database architectures and distributed systems"
        }
      }
    ]
  }
}
```

請注意，`combined_fields` 查詢會產生較高的相關性分數（排名第一的結果為 0.20001775，相較之下另一種查詢為 0.18051638）。

## 限制

請注意 `combined_fields` 查詢的下列限制：

- 所有欄位都必須使用相同的文字分析器。
- 此查詢僅適用於 `text` 欄位。
- 此查詢不支援以與 `multi_match` 相同的方式提升個別欄位的權重；請改用欄位權重。
