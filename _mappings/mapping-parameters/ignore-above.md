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

# ignore_above 對應參數

`ignore_above` 對應參數可限制已編製索引字串的最大字元數。若字串長度超過指定的門檻值，該值會隨文件一併儲存，但不會被編製索引。這有助於防止索引因異常長的值而膨脹，並可確保查詢效率。

預設情況下，若未指定 `ignore_above`，所有字串值都會完整編製索引。

## 範例：不使用 ignore_above

建立一個含有 `keyword` 欄位但未指定 `ignore_above` 參數的索引：

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

將含有長字串值的文件編製索引：

```json
PUT /test-no-ignore/_doc/1
{
  "sentence": "text longer than 10 characters"
}
```
{% include copy-curl.html %}

對完整字串執行 term 查詢：

```json
POST /test-no-ignore/_search
{
  "query": {
    "term": {
      "sentence": "text longer than 10 characters"
    }
  }
}
```
{% include copy-curl.html %}

文件會被傳回，因為 `sentence` 欄位已被編製索引：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13353139,
    "hits": [
      {
        "_index": "test-no-ignore",
        "_id": "1",
        "_score": 0.13353139,
        "_source": {
          "sentence": "text longer than 10 characters"
        }
      }
    ]
  }
}
```

## 範例：使用 ignore_above

在同一欄位上建立索引，並將 `ignore_above` 參數設為 `10`：

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

將同一份含有長字串值的文件編製索引：

```json
PUT /test-ignore/_doc/1
{
  "sentence": "text longer than 10 characters"
}
```
{% include copy-curl.html %}

對完整字串執行 term 查詢：

```json
POST /test-ignore/_search
{
  "query": {
    "term": {
      "sentence": "text longer than 10 characters"
    }
  }
}
```
{% include copy-curl.html %}

沒有傳回任何結果，因為 `sentence` 欄位中的字串超過了 `ignore_above` 門檻值，因此未被編製索引：

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

不過，文件仍然存在，可使用下列請求確認：

```json
GET test-ignore/_search
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
