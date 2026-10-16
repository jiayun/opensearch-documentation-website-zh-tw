---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "忽略超過上限的值"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/ignore-above/
nav_order: 120
has_children: false
has_toc: false
---

# Ignore above 對應參數

`ignore_above` 對應參數可為字串值設定最大長度。當值超過限制時，OpenSearch 仍會為文件編製索引，但會略過該值：它不會加入索引或 [doc values]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)，因此不會符合查詢，也不會出現在彙總或排序結果中。原始值仍保留在 [`_source`]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/) 欄位中，並會隨文件一併回傳。

使用 `ignore_above` 可避免異常冗長的值（例如堆疊追蹤，或傳送到對應為 `keyword` 之欄位的自由格式文字）增加索引大小或導致索引編製失敗。

若未指定 `ignore_above`，預設值為 `2147483647`，因此所有字串值無論長度都會編製索引。當 OpenSearch 動態對應字串欄位時，會建立一個 `keyword` 子欄位，並將其 `ignore_above` 設為 `256`。

若欄位包含字串陣列，OpenSearch 會對每個陣列元素分別套用限制。在限制內的元素會編製索引，較長的元素則會被略過。OpenSearch 不會在 [`_ignored`]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/ignored/) 中繼資料欄位記錄被略過的值，且對該欄位執行的 [`exists`]({{site.url}}{{site.baseurl}}/query-dsl/term/exists/) 查詢不會符合唯一值已被略過的文件。

## 範例：未使用 ignore_above

建立一個含有 `keyword` 欄位的索引，但不指定 `ignore_above` 參數：

```json
PUT /test-no-ignore
{
  "mappings": {
    "properties": {
      "sentence": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將一份含有長字串值的文件編製索引：

```json
PUT /test-no-ignore/_doc/1
{
  "sentence": "text longer than 10 characters"
}
```
{% include copy-curl.html %}

針對完整字串執行 term 查詢：

```json
GET /test-no-ignore/_search
{
  "query": {
    "term": {
      "sentence": "text longer than 10 characters"
    }
  }
}
```
{% include copy-curl.html %}

由於 `sentence` 欄位已編製索引，因此會傳回該文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "test-no-ignore",
        "_id": "1",
        "_score": 1,
        "_source": {
          "sentence": "text longer than 10 characters"
        }
      }
    ]
  }
}
```

## 範例：使用 ignore_above

建立索引，並在同一欄位上將 `ignore_above` 參數設為 `10`：

```json
PUT /test-ignore
{
  "mappings": {
    "properties": {
      "sentence": {
        "type": "keyword",
        "ignore_above": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

將相同的文件（含長字串值）編製索引：

```json
PUT /test-ignore/_doc/1
{
  "sentence": "text longer than 10 characters"
}
```
{% include copy-curl.html %}

對完整字串執行 term 查詢：

```json
GET /test-ignore/_search
{
  "query": {
    "term": {
      "sentence": "text longer than 10 characters"
    }
  }
}
```
{% include copy-curl.html %}

不會傳回任何結果，因為 `sentence` 欄位中的字串超過 `ignore_above` 閾值，因此未被編製索引：

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
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

若要確認該文件仍在索引中，請在不帶查詢的情況下搜尋索引：

```json
GET /test-ignore/_search
```
{% include copy-curl.html %}

傳回的命中結果包含該文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "test-ignore",
        "_id": "1",
        "_score": 1,
        "_source": {
          "sentence": "text longer than 10 characters"
        }
      }
    ]
  }
}
```

## 範例：陣列與彙總

建立一個包含 `product_tags` 欄位的索引，該欄位會略過長度超過 12 個字元的標籤：

```json
PUT /test-ignore-array
{
  "mappings": {
    "properties": {
      "product_tags": {
        "type": "keyword",
        "ignore_above": 12
      }
    }
  }
}
```
{% include copy-curl.html %}

將一份所有標籤都在限制內的文件編製索引：

```json
PUT /test-ignore-array/_doc/1
{
  "product_tags": ["outdoor", "waterproof"]
}
```
{% include copy-curl.html %}

將一份包含超出限制之標籤的文件編製索引：

```json
PUT /test-ignore-array/_doc/2?refresh=true
{
  "product_tags": ["outdoor", "lightweight-breathable-fabric"]
}
```
{% include copy-curl.html %}

對 `product_tags` 欄位執行 `terms` 彙總：

```json
GET /test-ignore-array/_search
{
  "size": 0,
  "aggs": {
    "tags": {
      "terms": {
        "field": "product_tags"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示兩份文件都符合搜尋條件，但 `lightweight-breathable-fabric` 標籤未出現在彙總桶中。第二份文件中的 `outdoor` 標籤在限制內，因此仍會被計入：

```json
{
  "took": 9,
  "timed_out": false,
  "terminated_early": true,
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
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "tags": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "outdoor",
          "doc_count": 2
        },
        {
          "key": "waterproof",
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 變更現有欄位的限制

您可以使用 [Create or Update Index Mappings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) 來變更現有欄位的 `ignore_above` 值。新的限制只會套用至變更後編製索引的文件。較早編製索引的文件不會更新，因此在舊限制下被略過的值仍無法搜尋，直到您重新編製那些文件的索引為止。

建立一個包含 `sku` 欄位且限制為 8 個字元的索引，然後將 `sku` 值長度為 13 個字元的文件編製索引：

```json
PUT /test-ignore-update
{
  "mappings": {
    "properties": {
      "sku": {
        "type": "keyword",
        "ignore_above": 8
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /test-ignore-update/_doc/1?refresh=true
{
  "sku": "SHOE-RUN-0042"
}
```
{% include copy-curl.html %}

將限制增加為 `20`：

```json
PUT /test-ignore-update/_mapping
{
  "properties": {
    "sku": {
      "type": "keyword",
      "ignore_above": 20
    }
  }
}
```
{% include copy-curl.html %}

將包含相同 `sku` 值的第二份文件編製索引：

```json
PUT /test-ignore-update/_doc/2?refresh=true
{
  "sku": "SHOE-RUN-0042"
}
```
{% include copy-curl.html %}

搜尋 `sku` 值：

```json
GET /test-ignore-update/_search
{
  "query": {
    "term": {
      "sku": "SHOE-RUN-0042"
    }
  }
}
```
{% include copy-curl.html %}

只會傳回第二份文件，因為第一份文件是在限制為 `8` 時編製索引的：

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
    "max_score": 1,
    "hits": [
      {
        "_index": "test-ignore-update",
        "_id": "2",
        "_score": 1,
        "_source": {
          "sku": "SHOE-RUN-0042"
        }
      }
    ]
  }
}
```

## 選擇限制值

Lucene 無法儲存以 UTF-8 編碼時超過 32,766 位元組的單一 `keyword` 詞彙或單一 `wildcard` 文件值。如果值超過此大小，且 `ignore_above` 未略過該值，OpenSearch 就會拒絕整份文件。設定 `ignore_above` 可避免此失敗情況，因為 OpenSearch 會略過過大的值，並為文件的其餘部分編製索引。

`ignore_above` 限制與 Lucene 限制採用不同的計量單位。OpenSearch 以 UTF-16 編碼單元計量 `ignore_above`。對大多數文字而言，一個編碼單元就是一個字元，但表情符號等字元會占用兩個編碼單元，因此在計算限制時會計為兩個。Lucene 以 UTF-8 位元組計量詞彙大小。每個 UTF-16 編碼單元以 UTF-8 編碼時最多占用 3 位元組，因此將 `ignore_above` 設為 `10922`（32,766 除以 3），即可確保 OpenSearch 編製索引的任何值都符合 Lucene 限制，無論其中包含哪些字元。如果您的值只包含 ASCII 字元，每個字元占用 1 位元組，便可將限制設為最高 `32766`。
