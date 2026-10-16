---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "來源"
parent: Metadata fields
nav_order: 70
redirect_from:
  - /field-types/metadata-fields/source/
---

# 來源中繼資料欄位

`_source` 欄位包含已編製索引的原始 JSON 文件本文。雖然此欄位無法搜尋，但系統會儲存此欄位，以便在執行 `get` 和 `search` 等擷取請求時傳回完整文件。

## 停用欄位

儲存 `_source` 會增加索引的大小。如果您永遠不需要擷取原始文件，可以將 `enabled` 參數設為 `false` 來停用 `_source` 欄位，如下列範例請求所示：

```json
PUT sample-index1
{
  "mappings": {
    "_source": {
      "enabled": false
    }
  }
}
```
{% include copy-curl.html %}

沒有 `_source` 時，搜尋和取得請求會傳回文件中繼資料，例如 `_id`，但不會傳回文件內容。欄位仍可搜尋，也可用於彙總。

停用 `_source` 會限制您日後能對索引執行的操作。沒有 `_source` 時，OpenSearch 無法提供下列功能：

- [Update Document]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)、[Update by Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) 和 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) API，這些 API 會從 `_source` 讀取文件。由於您無法重新編製索引，也無法將資料移至新索引以變更其對應或分析器。
- 針對未個別儲存之欄位的[醒目提示]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)。要求醒目提示的搜尋不會傳回這些欄位的醒目提示。若要醒目提示某個欄位，請將其 [`store`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/) 參數設為 `true`。
- 檢視原始文件，以排解查詢或彙總傳回非預期結果的原因。

您無法為現有索引啟用或停用 `_source`。若要在不明確儲存 `_source` 欄位的情況下支援這些功能，請使用[衍生的來源](#derived-source)。若要在不移除 `_source` 的情況下減少儲存空間，請使用更精簡的[索引轉碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/)。
{: .warning}

停用 `_source` 最適合包含許多僅由數字、日期和關鍵字組成之小型文件的索引，例如指標。這些文件通常永遠不會更新或重新編製索引，而對它們的搜尋會傳回彙總。在此情況下，停用 `_source` 可減少磁碟使用量和輸入/輸出。

## 包含或排除欄位

您可以使用 `includes` 和 `excludes` 參數選擇性控制 `_source` 欄位的內容。OpenSearch 會為完整文件編製索引，但在儲存前會從 `_source` 中移除指定的欄位。這兩個參數都接受萬用字元模式。下列請求會建立一個索引，在 `_source` 中只儲存請求計數與主機資訊，並移除主機備註與標籤：

```json
PUT app-metrics
{
  "mappings": {
    "_source": {
      "includes": [
        "*.count",
        "host.*"
      ],
      "excludes": [
        "host.notes",
        "host.tags.*"
      ]
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引至該索引：

```json
PUT app-metrics/_doc/1?refresh=true
{
  "requests": {
    "count": 42,
    "path": "/checkout"
  },
  "host": {
    "name": "web-01",
    "notes": "Rebooted after kernel update",
    "tags": {
      "rack": "r12",
      "zone": "us-east-1a"
    }
  }
}
```
{% include copy-curl.html %}

從 `_source` 移除的欄位仍會被編製索引，因此您可以搜尋它們。下列請求會搜尋被排除的 `host.tags.zone` 欄位：

```json
GET app-metrics/_search
{
  "query": {
    "match": {
      "host.tags.zone": "us-east-1a"
    }
  }
}
```
{% include copy-curl.html %}

回應包含該文件，但其 `_source` 只包含 `host.name` 和 `requests.count`。`requests.path` 欄位因不符合任何 `includes` 模式而被移除，`tags` 物件則因所有欄位都被排除而為空：

```json
{
  "took": 1,
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
    "max_score": 0.39229372,
    "hits": [
      {
        "_index": "app-metrics",
        "_id": "1",
        "_score": 0.39229372,
        "_source": {
          "host": {
            "name": "web-01",
            "tags": {}
          },
          "requests": {
            "count": 42
          }
        }
      }
    ]
  }
}
```

Update Document、Update by Query 與 Reindex API 會從已儲存的 `_source` 重建文件，因此會捨棄被移除的欄位。例如，在您更新前述文件中的任何欄位後，`host.tags.zone` 欄位將不再被編製索引，搜尋也不再符合該文件。如同 `enabled` 參數，您無法為現有索引變更 `includes` 或 `excludes`。若要在不從儲存空間移除欄位的情況下，從搜尋結果中省略欄位，請在搜尋請求中使用[來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)。
{: .warning}

## 衍生的來源

OpenSearch 會將每個匯入的文件儲存在 `_source` 欄位中，同時也會為個別欄位建立索引以供搜尋。`_source` 欄位可能佔用大量儲存空間。為了減少儲存空間用量，您可以設定 OpenSearch 略過儲存 `_source` 欄位，改為在需要時動態重建，例如在 `search`、`get`、`mget`、`reindex` 或 `update` 作業期間。

若要啟用衍生的來源，請設定 `derived_source` 索引層級設定：


```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  }
}
```
{% include copy-curl.html %}

雖然略過 `_source` 欄位可以大幅降低儲存空間需求，但動態衍生來源通常比讀取已儲存的 `_source` 更慢。為了避免搜尋查詢期間的這項額外負擔，請在不需要時不要請求 `_source` 欄位。您可以在搜尋查詢中將 `_source` 參數設為 `false`（如下列範例所示），或提供 `include` 與 `exclude` 欄位的清單：

```json
GET sample-index1/_search
{
  "_source": false,
  "query": { "match_all": {} }
}
```
{% include copy-curl.html %}

對於使用 [Get Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/get-documents/) 或 [Multi-get Documents API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/) 的即時讀取（在 [`refresh`]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/) 發生之前，這些讀取是由 translog 提供），使用衍生的來源時效能可能會較慢。這是因為必須先暫時匯入文件，才能重建來源。您可以使用索引層級的 `derived_source.translog` 設定來避免這項額外延遲，該設定會停用在 translog 讀取期間產生衍生的來源：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "translog": {
          "enabled": false
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如果使用此設定，`_source` 內容可能會有所不同，取決於它仍在 translog 中，還是已寫入分段。

### 支援的欄位與參數

衍生來源使用 [`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 和 [`stored_fields`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/) 在查詢時重建文件。由於 `doc_values` 的實作方式，動態產生的 `_source` 在格式或精確度上可能與原始匯入的文件不同。

衍生來源支援下列欄位類型，其中大多數不需要變更欄位對應（但有一些[限制](#limitations)）：

- [`boolean`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/boolean/)
- [`byte`, `double`, `float`, `half_float`, `integer`, `long`, `short`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)
- [`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)
- [`date_nanos`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date-nanos/)
- [`geo_point`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/)
- [`ip`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/ip/)
- [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)
- [`unsigned_long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/unsigned-long/)
- [`scaled_float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)
- [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/)
- [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/)

對於已啟用衍生來源的 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位，其欄位值預設會以儲存欄位的形式儲存。您不需要將 `store` 對應參數設為 `true`。
{: .note}

若要搭配衍生來源使用 [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/) 欄位，必須將對應參數 [`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 設為 `true`。
{: .note}

### 限制

衍生來源不支援下列欄位：

- 包含 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 參數的欄位。
- 定義了 [`ignore_above`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-above/) 或 [`normalizer`]({{site.url}}{{site.baseurl}}/analyzers/normalizers/) 參數的 [`keyword`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/) 和 [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/) 欄位。
- 巢狀欄位。
