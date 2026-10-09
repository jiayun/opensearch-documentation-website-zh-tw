---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.

layout: default
title: Wrapper
parent: Specialized queries
nav_order: 80
---

# Wrapper 查詢

`wrapper` 查詢可讓您以 Base64 編碼的 JSON 格式提交完整查詢。當查詢必須嵌入僅支援字串值的情境時，此查詢非常實用。

只有在需要處理系統限制時才使用此查詢。為了可讀性與可維護性，建議盡可能使用標準的 JSON 查詢。

## 範例

使用下列對應建立名為 `products` 的索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件編製索引：

```json
POST /products/_bulk
{ "index": { "_id": 1 } }
{ "title": "Wireless headphones with noise cancellation" }
{ "index": { "_id": 2 } }
{ "title": "Bluetooth speaker" }
{ "index": { "_id": 3 } }
{ "title": "Over-ear headphones with rich bass" }
```
{% include copy-curl.html %}

以 Base64 格式編碼下列查詢：

```bash
echo -n '{ "match": { "title": "headphones" } }' | base64
```
{% include copy.html %}

執行編碼後的查詢：

```json
POST /products/_search
{
  "query": {
    "wrapper": {
      "query": "eyAibWF0Y2giOiB7ICJ0aXRsZSI6ICJoZWFkcGhvbmVzIiB9IH0="
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩筆符合的文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.20098841,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.20098841,
        "_source": {
          "title": "Wireless headphones with noise cancellation"
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.18459359,
        "_source": {
          "title": "Over-ear headphones with rich bass"
        }
      }
    ]
  }
}
```
