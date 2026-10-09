---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "正規化器"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/normalizer/
nav_order: 190
has_children: false
has_toc: false
---

# 正規化器對應參數

`normalizer` 對應參數會為 keyword 欄位定義自訂的正規化流程。與文字欄位的[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)不同（分析器會產生多個詞元），[正規化器]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)會使用一組詞元篩選器，將整個欄位值轉換成單一詞元。當您定義正規化器時，keyword 欄位會在儲存前先由指定的篩選器處理，同時保持文件的 `_source` 不變。


## 定義正規化器

下列請求會建立名為 `products` 的索引，並使用名為 `my_normalizer` 的自訂正規化器。此正規化器會套用至 `code` 欄位，該欄位使用 `trim` 和 `lowercase` 篩選器：

```json
PUT /products
{
  "settings": {
    "analysis": {
      "normalizer": {
        "my_normalizer": {
          "type": "custom",
          "filter": ["trim", "lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "code": {
        "type": "keyword",
        "normalizer": "my_normalizer"
      }
    }
  }
}
```
{% include copy-curl.html %}

當您將文件匯入索引時，`code` 欄位會經過正規化，移除多餘的空格並將文字轉換為小寫：

```json
PUT /products/_doc/1
{
  "code": "  ABC-123 EXTRA  "
}
```
{% include copy-curl.html %}

在查詢中使用小寫且去除空白的文字，搜尋已編製索引的文件：

```json
POST /products/_search
{
  "query": {
    "term": {
      "code": "abc-123 extra"
    }
  }
}
```
{% include copy-curl.html %}

由於 `code` 欄位已正規化，`term` 查詢能成功比對到已儲存的文件：

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
          "code": "  ABC-123 EXTRA  "
        }
      }
    ]
  }
}
```
