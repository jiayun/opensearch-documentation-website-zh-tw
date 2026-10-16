---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Null 值"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/null-value/
nav_order: 210
has_children: false
has_toc: false
---

# Null 值對應參數

`null_value` 對應參數可讓您在編製索引期間，以預先定義的替代值取代明確的 `null` 值。根據預設，若欄位設為 `null`，就不會編製索引，也無法搜尋。定義 `null_value` 後，會改為將指定的替代值編製索引。這可讓您查詢或彙總欄位原本為 `null` 的文件，而不需修改文件的 `_source`。

當 `null` 帶有您想搜尋的意義時（例如尚未有出貨狀態的訂單，或尚未指派分類的產品），請使用 `null_value`。由於替代值會編製索引，包含 `null` 的文件也會符合對該欄位的 [`exists`]({{site.url}}{{site.baseurl}}/query-dsl/term/exists/) 查詢。

OpenSearch 只會取代明確的 `null` 值，包括陣列中的 `null` 元素。例如，若 `null_value` 為 `"unknown"`，則陣列 `["camping", null]` 會編製索引為 `camping` 和 `unknown`。下列值不會被取代：

- 空陣列（`[]`）
- 文件中缺少的欄位

您無法變更現有欄位的 `null_value`。若要使用不同的替代值，請建立包含新對應的索引，並將您的文件[重新編製索引]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)至該索引。

## 選擇替代值

`null_value` 必須是該欄位類型的有效值。例如，`long` 欄位需要數字，而 `boolean` 欄位需要 `true` 或 `false`。若數值、`boolean` 或 `geo_point` 欄位的 `null_value` 無效，OpenSearch 會拒絕該對應。

`date` 與 `ip` 欄位類型是例外。如果它們的 `null_value` 無法解析，例如 `date` 欄位的 `"never"`，OpenSearch 會接受該對應、在淘汰記錄檔中寫入警告，並忽略 `null_value`。包含 `null` 的文件隨後在編製索引時，該欄位不會有值。請透過為包含 `null` 的文件編製索引，並確認替代值可被搜尋，來測試該對應。
{: .important}

請選擇一個在真實資料中不會出現的替代值，以便區分被替換的值與實際值。對數值欄位而言，若實際值永遠不為負數，則 `-1` 這類值即可使用。

替代值會被編製索引，但不會改變 `_source` 欄位，該欄位仍包含 `null`。如果索引使用[衍生來源（derived source）]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source)，OpenSearch 會從已編製索引的值重建 `_source`，因此傳回的文件會包含替代值。

## 在欄位上設定 null_value

下列請求會建立名為 `products` 的索引。`category` 欄位的類型為 `keyword`，並在編製索引期間以 `"unknown"` 取代 `null` 值：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "category": {
        "type": "keyword",
        "null_value": "unknown"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 為包含 null 值的文件編製索引

為 `category` 欄位設為 `null` 的文件編製索引：

```json
PUT /products/_doc/1
{
  "category": null
}
```
{% include copy-curl.html %}

為 `category` 欄位為空陣列的文件編製索引：

```json
PUT /products/_doc/2
{
  "category": []
}
```
{% include copy-curl.html %}

為 `category` 欄位是包含 `null` 元素之陣列的文件編製索引：

```json
PUT /products/_doc/3?refresh=true
{
  "category": ["camping", null]
}
```
{% include copy-curl.html %}

## 查詢 null 替代值

搜尋 `category` 欄位包含 `null` 的文件：

```json
GET /products/_search
{
  "query": {
    "term": {
      "category": "unknown"
    }
  }
}
```
{% include copy-curl.html %}

回應包含文件 1 和 3。文件 2 不會被傳回，因為空陣列不會被取代。每份文件的 `_source` 仍包含 `null`：

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
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category": null
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 1,
        "_source": {
          "category": [
            "camping",
            null
          ]
        }
      }
    ]
  }
}
```

## 以 null 替代值進行彙總

由於 null 替代值會被編製索引，因此也會出現在彙總結果中。對 `category` 欄位執行 `terms` 彙總：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "category_count": {
      "terms": {
        "field": "category"
      }
    }
  }
}
```
{% include copy-curl.html %}

`unknown` 桶會計算包含 `null` 的兩份文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "category_count": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "unknown",
          "doc_count": 2
        },
        {
          "key": "camping",
          "doc_count": 1
        }
      ]
    }
  }
}
```
