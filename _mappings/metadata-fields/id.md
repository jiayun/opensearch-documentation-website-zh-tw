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

OpenSearch 中的每份文件都有一個唯一的 `_id` 欄位。此欄位會編製索引，讓您可以使用 [Get Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/get-documents/) 或 [`ids` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/ids/) 擷取文件。

當您[將文件編製索引]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)時，會在請求路徑中設定 `_id`，例如 `PUT test-index1/_doc/1`。如果您未提供 `_id` 值，OpenSearch 會產生一個。

`_id` 在 UTF-8 編碼下最長可達 512 位元組。OpenSearch 會拒絕指定較長 ID 的請求。ASCII 範圍以外的字元會佔用超過 1 個位元組，因此含有這類字元的 ID 會在少於 512 個字元時就達到上限。

## 查詢文件 ID

您可以使用 `term`、`terms`、`match`、`query_string` 和 `simple_query_string` 查詢來搜尋 `_id` 欄位。此欄位必須符合完整的 ID，因此不支援 `prefix`、`wildcard` 和 `range` 查詢。

下列範例請求會建立名為 `test-index1` 的索引，並新增兩份具有不同 `_id` 值的文件。

第一個請求會新增一份 `_id` 為 `1` 的文件：

```json
PUT test-index1/_doc/1
{
  "text": "Document with ID 1"
}
```
{% include copy-curl.html %}

第二個請求會新增一份 `_id` 為 `2` 的文件，並重新整理索引，讓兩份文件都能立即被搜尋到：

```json
PUT test-index1/_doc/2?refresh=true
{
  "text": "Document with ID 2"
}
```
{% include copy-curl.html %}

接著，您可以使用 `_id` 欄位查詢文件，如下列範例請求所示：

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

回應會傳回這兩份文件，其 `_id` 值分別為 `1` 和 `2`：

```json
{
  "took": 7,
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
}
```

## 依文件 ID 排序與彙總

`_id` 欄位不會儲存 doc values。若要在指令碼中排序、彙總或存取 `_id`，OpenSearch 會將分片中的所有 ID 載入記憶體，這在包含大量文件的索引上可能耗用大量堆積記憶體。此存取方式已棄用，發生時 OpenSearch 會將警告寫入棄用記錄檔。`indices.id_field_data.enabled` 叢集設定可控制是否允許此行為。若將其設為 `false`，OpenSearch 會拒絕依 `_id` 排序或彙總的請求。如需更多資訊，請參閱[叢集設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-gateway-and-indexes-settings)。

若要依文件 ID 排序或彙總，請同時將 ID 儲存在文件本文中另一個 `keyword` 欄位。類型為 `keyword` 的欄位預設會儲存 doc values。
