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

您可以將 `enabled` 參數設為 `false`，以停用 `_source` 欄位，如下列範例請求所示：

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

停用 `_source` 欄位可能會影響某些功能的可用性，例如 `update`、`update_by_query` 和 `reindex` API，以及使用原始已編製索引的文件對查詢或彙總進行偵錯的能力。若要在不明確儲存 `_source` 欄位的情況下支援這些功能，可以使用[衍生來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source)，同時符合儲存空間限制。
{: .warning}

## 納入或排除欄位

您可以使用 `includes` 和 `excludes` 參數，選擇性地控制 `_source` 欄位的內容。這讓您能在編製索引之後、儲存之前，刪減要儲存的 `_source` 欄位內容，如下列範例請求所示：

```json
PUT logs
{
  "mappings": {
    "_source": {
      "includes": [
        "*.count",
        "meta.*"
      ],
      "excludes": [
        "meta.description",
        "meta.other.*"
      ]
    }
  }
}
```
{% include copy-curl.html %}

這些欄位不會儲存在 `_source` 中，但您仍然可以搜尋這些欄位，因為資料仍保有索引。

## 衍生來源

OpenSearch 將每個匯入的文件儲存在 `_source` 欄位中，也會為個別欄位編製索引以供搜尋。`_source` 欄位可能會占用大量儲存空間。若要減少儲存空間用量，您可以設定 OpenSearch 略過儲存 `_source` 欄位，改為在需要時動態重建該欄位，例如在執行 `search`、`get`、`mget`、`reindex` 或 `update` 操作時。

若要啟用衍生來源，請設定索引層級的 `derived_source` 設定：


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

雖然略過 `_source` 欄位可以大幅降低儲存空間需求，但動態衍生來源通常比讀取已儲存的 `_source` 更慢。若要在搜尋查詢期間避免這項額外負擔，請在不需要 `_source` 欄位時，不要請求該欄位。您可以在搜尋查詢中將 `_source` 參數設為 `false`（如下列範例所示），或提供 `include` 和 `exclude` 欄位清單來達成此目的：

```json
GET sample-index1/_search
{
  "_source": false,
  "query": { "match_all": {} }
}
```
{% include copy-curl.html %}

使用 [Get Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/get-documents/) 或 [Multi-get Documents API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/) 進行即時讀取時，在發生[`refresh`]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/) 之前，讀取請求會由交易記錄檔提供資料，此時使用衍生來源的效能可能較慢。這是因為必須先暫時匯入文件，才能重建來源。您可以使用索引層級的 `derived_source.translog` 設定，在讀取交易記錄檔期間停用衍生來源的產生，以避免這項額外延遲：

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

如果使用此設定，您可能會發現文件的 `_source` 內容會因文件仍在交易記錄檔中或已寫入分段而有所不同。

### 支援的欄位與參數

衍生來源使用 [`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 和 [`stored_fields`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/) 在查詢時重建文件。由於 `doc_values` 的實作方式，動態產生的 `_source` 在格式或精確度上可能與原始匯入的文件不同。

衍生來源支援下列欄位類型，其中大多數不需要變更欄位對應（但有一些[限制](#limitations)）：

- [`boolean`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/boolean/)
- [`byte`, `double`, `float`, `half_float`, `integer`, `long`, `short`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)
- [`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)
- [`date-nanos`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date-nanos/)
- [`geo_point`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/)
- [`ip`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/ip/)
- [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)
- [`unsigned_long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/unsigned-long/)
- [`scaled_float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)
- [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/)
- [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/)

對於已啟用衍生來源的 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位，欄位值預設會以儲存欄位的形式儲存。您不需要將 `store` 對應參數設為 `true`。
{: .note}

若要搭配衍生來源使用 [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/) 欄位，必須將對應參數 [`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 設為 `true`。
{: .note}

### 限制

衍生來源不支援下列欄位：

- 包含 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 參數的欄位。
- 定義了 [`ignore_above`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-above/) 或 [`normalizer`]({{site.url}}{{site.baseurl}}/analyzers/normalizers/) 參數的 [`keyword`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/) 和 [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/) 欄位。
- 巢狀欄位。
