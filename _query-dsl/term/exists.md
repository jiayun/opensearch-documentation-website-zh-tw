---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Exists
parent: Term-level queries
nav_order: 70
---

# Exists 查詢

使用 `exists` 查詢來搜尋包含特定欄位的文件。

在下列任一情況下，文件欄位不會有已編製索引的值：

- 欄位在對應中指定了 `"index" : false`。
- 來源 JSON 中的欄位為 `null` 或 `[]`。
- 欄位值的長度超過對應中的 `ignore_above` 設定。
- 欄位值的格式錯誤，且對應中已定義 `ignore_malformed`。

在下列任一情況下，文件欄位會有已編製索引的值：

- 值為陣列，包含一個或多個 null 元素，以及一個或多個非 null 元素（例如，`["one", null]`）。
- 值為空字串（`""` 或 `"-"`）。
- 值為欄位對應中定義的自訂 `null_value`。


## 範例

例如，假設某個索引包含下列兩份文件：

```json
PUT testindex/_doc/1
{
  "title": "The wind rises"
}
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{
  "title": "Gone with the wind",
  "description": "A 1939 American epic historical film"
}
```
{% include copy-curl.html %}

下列查詢會搜尋包含 `description` 欄位的文件：

```json
GET testindex/_search
{
  "query": {
    "exists": {
      "field": "description"
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合條件的文件：

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Gone with the wind",
          "description": "A 1939 American epic historical film"
        }
      }
    ]
  }
}
```

## 尋找缺少已編製索引值的文件

若要尋找缺少已編製索引值的文件，您可以使用 `must_not` [布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)，並在其中使用 `exists` 查詢。例如，下列請求會搜尋缺少 `description` 欄位的文件：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "description"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合條件的文件：

```json
{
  "took": 19,
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
    "max_score": 0,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0,
        "_source": {
          "title": "The wind rises"
        }
      }
    ]
  }
}
```

## 參數

此查詢接受欄位名稱（`<field>`）作為頂層參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`boost` | 浮點數 | 指定此欄位對相關性分數所占權重的浮點數值。大於 1.0 的值會提高欄位的相關性。介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設值為 1.0。
