---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文件值"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/doc-values/
nav_order: 25
has_children: false
has_toc: false
---

# 文件值對應參數

預設情況下，大多數欄位會使用反向索引來編製索引並供搜尋。反向索引的運作方式是儲存一份經過排序的唯一詞彙清單，並將每個詞彙對應到包含它的文件。

然而，排序、彙總以及在指令碼中存取欄位，需要不同的方法。這些操作不是從詞彙找出文件，而是需要從特定文件擷取詞彙。

文件值讓這些操作得以實現。它們是在編製索引時建立的磁碟上、以欄為導向的資料結構。雖然它們儲存的值與 `_source` 欄位相同，但其格式經過最佳化，可快速執行排序與彙總。

幾乎所有欄位類型預設都會啟用文件值，`text` 欄位除外。如果您確定某個欄位不會用於排序、彙總或指令碼，可以停用文件值以減少磁碟用量。

## 範例

若要了解 `doc_values` 如何影響欄位，請建立一個範例索引。在此索引中，`status_code` 欄位預設啟用 `doc_values`，因此支援排序與彙總。`session_id` 欄位則停用 `doc_values`，因此不支援排序或彙總，但仍可查詢：

```json
PUT /web_analytics
{
  "mappings": {
    "properties": {
      "status_code": {
        "type": "keyword"
      },
      "session_id": {
        "type": "keyword",
        "doc_values": false
      }
    }
  }
}
```
{% include copy-curl.html %}

將一些範例資料加入索引：

```json
PUT /web_analytics/_doc/1
{
  "status_code": "200",
  "session_id": "abc123"
}
```
{% include copy-curl.html %}

```json
PUT /web_analytics/_doc/2
{
  "status_code": "404",
  "session_id": "def456"
}
```
{% include copy-curl.html %}

```json
PUT /web_analytics/_doc/3
{
  "status_code": "200",
  "session_id": "ghi789"
}
```
{% include copy-curl.html %}

對 `status_code` 欄位執行彙總：

```json
GET /web_analytics/_search
{
  "size": 0,
  "aggs": {
    "status_codes": {
      "terms": {
        "field": "status_code"
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會傳回正確的結果，因為 `status_code` 已啟用 `doc_values`：

```json
{
  "took": 37,
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
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "status_codes": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "200",
          "doc_count": 2
        },
        {
          "key": "404",
          "doc_count": 1
        }
      ]
    }
  }
}
```

嘗試對 `session_id` 欄位進行彙總：

```json
GET /web_analytics/_search
{
  "size": 0,
  "aggs": {
    "session_counts": {
      "terms": {
        "field": "session_id"
      }
    }
  }
}
```
{% include copy-curl.html %}

此彙總會失敗，因為 `session_id` 已停用 `doc_values`，導致彙總所需的文件對欄位查詢無法執行。
