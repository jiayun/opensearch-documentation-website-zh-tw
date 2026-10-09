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

`null_value` 對應參數可讓您在編製索引期間，以預先定義的替代值取代明確的 `null` 值。根據預設，若欄位設為 `null`，就不會編製索引，也無法搜尋。若定義了 `null_value`，則會改為將指定的替代值編製索引。這可讓您查詢或彙總欄位原本為 `null` 的文件，而不需修改文件 `_source`。

`null_value` 的類型必須與其所套用的欄位相同。例如，`date` 欄位不能使用 `true` 這類 `boolean` 作為其 `null_value`；`null_value` 必須是有效的日期字串。
{: .important}

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

## 為含有 null 值的文件編製索引

使用下列命令為 `category` 欄位設為 `null` 的文件編製索引：

```json
PUT /products/_doc/1
{
  "category": null
}
```
{% include copy-curl.html %}

## 查詢 null 替代值

使用下列命令搜尋 `category` 欄位先前為 `null` 的文件：

```json
POST /products/_search
{
  "query": {
    "term": {
      "category": "unknown"
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.2876821,
        "_source": {
          "category": null
        }
      }
    ]
  }
}
```

## 彙總 null 替代值

由於 null 替代值已編製索引，因此也會出現在彙總中。使用下列命令對 `category` 欄位執行 `terms` 彙總：

```json
POST /products/_search
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

回應包含彙總結果：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
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
          "doc_count": 1
        }
      ]
    }
  }
}
```