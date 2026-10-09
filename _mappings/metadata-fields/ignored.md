---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "已忽略"
parent: Metadata fields
nav_order: 30
redirect_from:
  - /field-types/metadata-fields/ignored/
---

# 已忽略的中繼資料欄位

`_ignored` 欄位可協助您管理文件中格式錯誤資料的相關問題。當 [索引對應]({{site.url}}{{site.baseurl}}/mappings/) 中啟用了 `ignore_malformed` 設定時，此欄位會用來編製索引並儲存索引過程中遭忽略的欄位名稱。

`_ignored` 欄位可讓您搜尋並找出含有遭忽略欄位的文件，以及找出遭忽略的特定欄位名稱。這對於疑難排解很有幫助。

您可以使用 `term`、`terms` 和 `exists` 查詢來查詢 `_ignored` 欄位，結果會包含在搜尋命中項目中。

只有在您的索引對應中啟用了 `ignore_malformed` 設定時，才會填入 `_ignored` 欄位。如果 `ignore_malformed` 設為 `false`（預設值），格式錯誤的欄位會導致整份文件遭到拒絕，且不會填入 `_ignored` 欄位。
{: .note}

下列範例請求示範如何使用 `_ignored` 欄位：

```json
GET _search
{
  "query": {
    "exists": {
      "field": "_ignored"
    }
  }
}
```
{% include copy-curl.html %}

--- 

#### 使用 `_ignored` 欄位的範例索引請求

下列範例請求會將含有格式錯誤值的文件新增至 `test-ignored` 索引，然後搜尋含有遭忽略欄位的文件。

首先，建立索引並在 `length` 欄位上將 `ignore_malformed` 設為 `true`，以便在編製索引期間不會擲回錯誤：

```json
PUT test-ignored
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "length": {
        "type": "long",
        "ignore_malformed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將 `length` 值不是數字的文件編製索引。`refresh` 參數可讓文件立即可供搜尋：

```json
POST test-ignored/_doc?refresh=true
{
  "title": "correct text",
  "length": "not a number"
}
```
{% include copy-curl.html %}

最後，搜尋至少有一個遭忽略欄位的文件：

```json
GET test-ignored/_search
{
  "query": {
    "exists": {
      "field": "_ignored"
    }
  }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 42,
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
        "_index": "test-ignored",
        "_id": "qcf0wZABpEYH7Rw9OT7F",
        "_score": 1,
        "_ignored": [
          "length"
        ],
        "_source": {
          "title": "correct text",
          "length": "not a number"
        }
      }
    ]
  }
}
```

---

## 忽略指定的欄位

您可以使用 `term` 查詢來尋找特定欄位遭忽略的文件，如下列範例請求所示：

```json
GET _search
{
  "query": {
    "term": {
      "_ignored": "created_at"
    }
  }
}
```
{% include copy-curl.html %}

#### 回應 

```json
{
  "took": 51,
  "timed_out": false,
  "_shards": {
    "total": 45,
    "successful": 45,
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
