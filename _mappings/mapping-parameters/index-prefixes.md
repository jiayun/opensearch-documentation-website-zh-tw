---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引前綴"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/index-prefixes/
nav_order: 170
has_children: false
has_toc: false
---

# 索引前綴對應參數

`index_prefixes` 對應參數會指示引擎為文字欄位中詞彙的開頭分段產生額外的索引項目。啟用後，它會根據可設定的最小與最大字元長度建立前綴索引。這可以大幅改善[前綴查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/)的效能，例如[自動完成]({{site.url}}{{site.baseurl}}/opensearch/search/autocomplete/)或[隨打即搜]({{site.url}}{{site.baseurl}}/opensearch/search/autocomplete/#search-as-you-type)，讓這些查詢能快速比對預先編製索引的詞彙前綴。

根據預設，不會執行前綴索引，以維持最小的索引大小與快速的索引作業。不過，如果您的應用程式受益於快速的前綴比對，啟用此參數可以明顯改善查詢效率。

## 索引前綴組態

您可以將下列組態參數傳遞給 `index_prefixes` 對應參數：

- `min_chars`：需要編製索引的前綴的最小長度。最小值為 `0`。預設為 `2`。
- `max_chars`：需要編製索引的前綴的最大長度。最大值為 `20`。預設為 `5`。

## 在欄位上啟用索引前綴

下列請求會建立名為 `products` 的索引，並將 `name` 欄位設定為建立長度介於 `2` 與 `10` 個字元之間的前綴索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "index_prefixes": {
          "min_chars": 2,
          "max_chars": 10
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求將文件編製索引：

```json
PUT /products/_doc/1
{
  "name": "Ultra HD Television"
}
```
{% include copy-curl.html %}

下列搜尋請求顯示一個前綴查詢，用於搜尋 `name` 欄位開頭為 `ul` 的文件：

```json
POST /products/_search
{
  "query": {
    "prefix": {
      "name": "ul"
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
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Ultra HD Television"
        }
      }
    ]
  }
}
```

## 搭配索引前綴使用預設參數

下列請求會使用 `index_prefixes` 搭配預設參數建立名為 `products_default` 的索引：

```json
PUT /products_default
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "index_prefixes": {}
      }
    }
  }
}
```
{% include copy-curl.html %}
