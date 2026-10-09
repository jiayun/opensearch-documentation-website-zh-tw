---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ID
parent: Metadata fields
nav_order: 20
redirect_from:
  - /field-types/metadata-fields/id/
---

# ID 中繼資料欄位

OpenSearch 中的每份文件都有一個唯一的 `_id` 欄位。此欄位會被編製索引，讓您能夠使用 GET API 或 [`ids` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/ids/)來擷取文件。

如果您未提供 `_id` 值，OpenSearch 會自動為該文件產生一個。
{: .note}

下列範例請求會建立一個名為 `test-index1` 的索引，並新增兩份具有不同 `_id` 值的文件。

第一個請求新增一份 `_id` 為 `1` 的文件：

```json
PUT test-index1/_doc/1
{
  "text": "Document with ID 1"
}
```
{% include copy-curl.html %}

第二個請求新增一份 `_id` 為 `2` 的文件，並重新整理索引，讓兩份文件都能立即被搜尋：

```json
PUT test-index1/_doc/2?refresh=true
{
  "text": "Document with ID 2"
}
```
{% include copy-curl.html %}

接著，您可以使用 `_id` 欄位查詢這些文件，如下列範例請求所示：

```json
GET test-index1/_search
{
  "query": {
    "terms": {
      "_id": ["1", "2"]
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回兩份 `_id` 值分別為 `1` 和 `2` 的文件：

```json
{
  "took": 10,
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
        "_index": "test-index1",
        "_id": "1",
        "_score": 1,
        "_source": {
          "text": "Document with ID 1"
        }
      },
      {
        "_index": "test-index1",
        "_id": "2",
        "_score": 1,
        "_source": {
          "text": "Document with ID 2"
        }
      }
    ]
  }
```
{% include copy-curl.html %}

## `_id` 欄位的限制

雖然 `_id` 欄位可用於各種查詢，但不得用於彙總、排序和指令碼。如果您需要依 `_id` 欄位進行排序或彙總，建議將 `_id` 內容複製到另一個啟用 `doc_values` 的欄位。範例請參閱 [IDs 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/ids/)。
