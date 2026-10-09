---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Boost
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/boost/
nav_order: 10
has_children: false
has_toc: false
---

# Boost 對應參數

`boost` 對應參數用於在搜尋查詢期間提高或降低欄位的相關性分數。它可讓您在計算文件的整體相關性分數時，對特定欄位施加更多或更少的權重。

`boost` 參數會以乘數方式套用至欄位的分數。例如，如果某欄位的 `boost` 值為 `2`，則該欄位的分數貢獻會加倍。相反地，`boost` 值為 `0.5` 則會將該欄位的分數貢獻減半。

使用 `boost` 參數時，建議您從較小的值 (1.5 或 2) 開始，並測試其對搜尋結果的影響。過高的 boost 值可能會使相關性分數產生偏差，導致非預期或不理想的搜尋結果。

boost 參數僅適用於[詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/)。它不適用於 `prefix`、`range` 或 `fuzzy` 詞彙層級查詢。
{: .note}

## 索引時與查詢時加權

雖然您可以在欄位對應中設定 boost 值 (索引時加權)，但並不建議這麼做。建議改用查詢時加權，它具有以下幾項優點：

- **彈性**：查詢時加權可讓您調整 boost 值，而無需重新為文件編製索引。

- **精確度**：索引時加權會儲存為 [`norms`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/norms/) 的一部分，而該結構僅使用 1 個位元組。這可能會降低欄位長度正規化的解析度。

- **動態控制**：查詢時加權讓您能夠針對不同的使用情境實驗不同的 boost 值。

## 範例

使用 `boost` 參數可為特定欄位賦予更多權重。例如，若標題是相關性的較強指標，將 `title` 欄位的權重提高得比 `description` 欄位更多，可以改善搜尋結果。

在此範例中，`title` 欄位的 boost 為 `2`，因此它對相關性分數的貢獻是 `description` 欄位 (其預設 boost 為 `1`) 的兩倍。

### 索引時加權 (不建議)

建立一個包含加權欄位的索引 (僅供示範之用)：

```json
PUT /article_index
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "boost": 2
      },
      "description": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將一些範例文件加入索引：

```json
PUT /article_index/_doc/1
{
  "title": "Introduction to Machine Learning",
  "description": "This article covers basic algorithms and their applications in data science."
}
```
{% include copy-curl.html %}

```json
PUT /article_index/_doc/2
{
  "title": "Data Science Fundamentals",
  "description": "Learn about machine learning algorithms and statistical methods for analyzing data."
}
```
{% include copy-curl.html %}

使用索引時加權搜尋這兩個欄位：

```json
POST /article_index/_search
{
  "query": {
    "multi_match": {
      "query": "machine learning algorithms",
      "fields": ["title", "description"]
    }
  }
}
```
{% include copy-curl.html %}

文件 1 的分數較高，因為 "machine learning" 出現在已加權的 `title` 欄位中。文件 2 的分數較低，因為 "machine learning" 出現在未加權的 `description` 欄位中。兩份文件都包含 "algorithms"，這也對它們的分數有所貢獻：

<p id="index-time-response"></p>

```json
{
  "took": 415,
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
    "max_score": 1.1906823,
    "hits": [
      {
        "_index": "article_index",
        "_id": "1",
        "_score": 1.1906823,
        "_source": {
          "title": "Introduction to Machine Learning",
          "description": "This article covers basic algorithms and their applications in data science."
        }
      },
      {
        "_index": "article_index",
        "_id": "2",
        "_score": 0.7130072,
        "_source": {
          "title": "Data Science Fundamentals",
          "description": "Learn about machine learning algorithms and statistical methods for analyzing data."
        }
      }
    ]
  }
}
```

### 查詢時加權 (建議)

請改用查詢時加權取代索引時加權，以獲得更好的控制與彈性。查詢時加權不需要設定任何特殊的欄位對應。

將一些範例文件加入索引：

```json
PUT /article_index_2/_doc/1
{
  "title": "Introduction to Machine Learning",
  "description": "This article covers basic algorithms and their applications in data science."
}
```
{% include copy-curl.html %}

```json
PUT /article_index_2/_doc/2
{
  "title": "Data Science Fundamentals",
  "description": "Learn about machine learning algorithms and statistical methods for analyzing data."
}
```
{% include copy-curl.html %}

首先，不加權搜尋 `title` 欄位：

```json
POST /article_index_2/_search
{
  "query": {
    "match": {
      "title": {
        "query": "machine learning algorithms"
      }
    }
  }
}
```
{% include copy-curl.html %}

符合的文件分數為 0.59：

```json
{
  "took": 13,
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
    "max_score": 0.59534115,
    "hits": [
      {
        "_index": "article_index_2",
        "_id": "1",
        "_score": 0.59534115,
        "_source": {
          "title": "Introduction to Machine Learning",
          "description": "This article covers basic algorithms and their applications in data science."
        }
      }
    ]
  }
}
```

接著，以加權方式搜尋同一欄位：

```json
POST /article_index_2/_search
{
  "query": {
    "match": {
      "title": {
        "query": "machine learning algorithms",
        "boost": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

文件分數加倍：

```json
{
  "took": 16,
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
    "max_score": 1.1906823,
    "hits": [
      {
        "_index": "article_index_2",
        "_id": "1",
        "_score": 1.1906823,
        "_source": {
          "title": "Introduction to Machine Learning",
          "description": "This article covers basic algorithms and their applications in data science."
        }
      }
    ]
  }
}
```

若要取得搜尋 `title` 與 `description` 兩個欄位的基準，請先不加權搜尋：

```json
POST /article_index_2/_search
{
  "query": {
    "multi_match": {
      "query": "machine learning algorithms",
      "fields": ["title", "description"]
    }
  }
}
```
{% include copy-curl.html %}

文件 2 的分數高於文件 1：

```json
{
  "took": 10,
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
    "max_score": 0.7130072,
    "hits": [
      {
        "_index": "article_index_2",
        "_id": "2",
        "_score": 0.7130072,
        "_source": {
          "title": "Data Science Fundamentals",
          "description": "Learn about machine learning algorithms and statistical methods for analyzing data."
        }
      },
      {
        "_index": "article_index_2",
        "_id": "1",
        "_score": 0.59534115,
        "_source": {
          "title": "Introduction to Machine Learning",
          "description": "This article covers basic algorithms and their applications in data science."
        }
      }
    ]
  }
}
```

若要比較索引時加權與查詢時加權，請使用查詢時加權搜尋多個欄位：

```json
POST /article_index_2/_search
{
  "query": {
    "multi_match": {
      "query": "machine learning algorithms",
      "fields": ["title^2", "description"]
    }
  }
}
```
{% include copy-curl.html %}

此查詢產生的回應與[索引時加權查詢](#index-time-response)相同，且文件 1 的分數現在高於文件 2：

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.1906823,
    "hits": [
      {
        "_index": "article_index_2",
        "_id": "1",
        "_score": 1.1906823,
        "_source": {
          "title": "Introduction to Machine Learning",
          "description": "This article covers basic algorithms and their applications in data science."
        }
      },
      {
        "_index": "article_index_2",
        "_id": "2",
        "_score": 0.7130072,
        "_source": {
          "title": "Data Science Fundamentals",
          "description": "Learn about machine learning algorithms and statistical methods for analyzing data."
        }
      }
    ]
  }
}
```
