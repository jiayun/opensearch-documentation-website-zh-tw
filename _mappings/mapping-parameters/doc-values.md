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

# Doc values 對應參數

`doc_values` 對應參數控制 OpenSearch 是否將欄位的值儲存在 doc values 中，這是一種以文件為單位組織的磁碟結構。OpenSearch 在編製索引時建立 doc values，並將其用於需要取得每個相符文件欄位值的作業：排序、彙總，以及在指令碼中存取欄位值。

搜尋使用的是另一種結構。反向索引將每個詞彙對應到包含它的文件，因此可以快速找出查詢的文件，但在特定文件中查閱欄位值則較慢。Doc values 儲存與 `_source` 欄位相同的值，但以欄的方式組織，每個欄位一欄，因此 OpenSearch 無需剖析 `_source` 即可讀取任何文件的值。

所有支援 doc values 的欄位類型預設都會啟用 doc values。`text` 欄位類型不支援 doc values，OpenSearch 會忽略 `text` 欄位對應中的 `doc_values`。若要對文字進行排序或彙總，請新增 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 子欄位，或較少見地啟用 [field data]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/field-data/)。

如果您不會對某個欄位進行排序、彙總或執行指令碼，可以停用 doc values 以減少磁碟用量。停用 doc values 的欄位仍然可以被搜尋。停用 doc values 之前，請注意以下事項：

- 您無法變更現有欄位的 `doc_values`。若要稍後啟用或停用 doc values，必須將資料重新編製索引到新的索引。
- [Derived source]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source) 會從 doc values 與儲存欄位重建 `_source`。若某欄位的對應同時停用 `doc_values` 與 [`store`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/)，OpenSearch 會拒絕該 derived source 對應。

對數值欄位而言，反向的取捨也有可能。如果您將數值欄位的 [`index`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/) 設為 `false` 但保留 doc values，OpenSearch 仍可透過掃描其 doc values 來搜尋該欄位。這類查詢比對已編製索引欄位的查詢慢，因此此組態適合主要以彙總為主、僅偶爾搜尋的欄位。

## 範例：在查詢用欄位上停用 doc values

下列請求會建立一個索引，其中 `response_code` 欄位使用預設的 doc values，因此您可以對它進行排序與彙總。`request_id` 欄位則停用了 doc values，因為每個值都是唯一的，且僅用於查詢個別請求：

```json
PUT /web_analytics
{
  "mappings": {
    "properties": {
      "response_code": {
        "type": "keyword"
      },
      "request_id": {
        "type": "keyword",
        "doc_values": false
      }
    }
  }
}
```
{% include copy-curl.html %}

在索引中加入一些範例資料：

```json
PUT /web_analytics/_doc/1
{
  "response_code": "200",
  "request_id": "req-7f3a"
}
```
{% include copy-curl.html %}

```json
PUT /web_analytics/_doc/2
{
  "response_code": "404",
  "request_id": "req-91c2"
}
```
{% include copy-curl.html %}

```json
PUT /web_analytics/_doc/3?refresh=true
{
  "response_code": "200",
  "request_id": "req-b04e"
}
```
{% include copy-curl.html %}

對 `response_code` 欄位執行彙總：

```json
GET /web_analytics/_search
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response_code"
      }
    }
  }
}
```
{% include copy-curl.html %}

彙總會為每個回應碼傳回一個桶 (bucket)：

```json
{
  "took": 4,
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
    "response_codes": {
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

嘗試對 `request_id` 欄位進行彙總：

```json
GET /web_analytics/_search
{
  "size": 0,
  "aggs": {
    "request_counts": {
      "terms": {
        "field": "request_id"
      }
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會拒絕該請求，因為 `request_id` 沒有 doc values 可用來讀取每份文件的值。對 `request_id` 進行排序也因同樣原因而失敗。不過，您仍然可以搜尋該欄位。例如，對 `req-91c2` 執行 `term` 查詢會傳回文件 2。
