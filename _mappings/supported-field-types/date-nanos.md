---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "奈秒日期"
redirect_from:
  - /field-types/supported-field-types/date-nanos/
parent: Date field types
grand_parent: Supported field types
nav_order: 40
---

# 奈秒日期欄位類型
**於 1.0 版導入**
{: .label .label-purple }

`date_nanos` 欄位類型與 [`date`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/) 欄位類型類似，都是用來儲存日期。然而，`date` 以毫秒解析度儲存日期，而 `date_nanos` 則以奈秒解析度儲存日期。日期以 `long` 值儲存，對應自 epoch 起算的奈秒數。因此，支援的日期範圍大約是 1970 至 2262 年。

對 `date_nanos` 欄位的查詢會轉換為以該欄位值 `long` 表示法的範圍查詢。接著，儲存的欄位與彙總結果會使用欄位上設定的格式轉換為字串。

`date_nanos` 欄位支援 `date` 所支援的所有[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date#formats)與[參數]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date#parameters)。您可以使用以 `||` 分隔的多種格式。
{: .note}

對於 `date_nanos` 欄位，您可以使用 `strict_date_optional_time_nanos` 格式來保留奈秒解析度。如果在將欄位對應為 `date_nanos` 時未指定格式，預設格式為 `strict_date_optional_time||epoch_millis`，可讓您以 `strict_date_optional_time` 或 `epoch_millis` 格式傳入值。`strict_date_optional_time` 格式支援奈秒解析度的日期，但 `epoch_millis` 格式僅支援毫秒解析度的日期。

## 範例

建立一個包含 `date` 欄位的對應，該欄位類型為 `date_nanos` 並使用 `strict_date_optional_time_nanos` 格式：

```json
PUT testindex/_mapping
{
  "properties": {
      "date": {
        "type": "date_nanos",
        "format" : "strict_date_optional_time_nanos"
      }
    }
}
```
{% include copy-curl.html %}

將兩份文件編製索引至該索引：

```json
PUT testindex/_doc/1
{ "date": "2022-06-15T10:12:52.382719622Z" }
```
{% include copy-curl.html %}

```json
PUT testindex/_doc/2
{ "date": "2022-06-15T10:12:52.382719624Z" }
```
{% include copy-curl.html %}

您可以使用範圍查詢來搜尋日期範圍：

```json
GET testindex/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "2022-06-15T10:12:52.382719621Z",
        "lte": "2022-06-15T10:12:52.382719623Z"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含日期在指定範圍內的文件：

```json
{
  "took": 43,
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
        "_id": "1",
        "_score": 1,
        "_source": {
          "date": "2022-06-15T10:12:52.382719622Z"
        }
      }
    ]
  }
}
```

查詢含有 `date_nanos` 欄位的文件時，您可以使用 `fields` 或 `docvalue_fields`：

```json
GET testindex/_search
{
  "fields": ["date"]
}
```
{% include copy-curl.html %}

```json
GET testindex/_search
{
  "docvalue_fields" : [
    {
      "field" : "date"
    }
  ]
}
```
{% include copy-curl.html %}

上述任一查詢的回應都包含兩份已編製索引的文件：

```json
{
  "took": 4,
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
        "_index": "testindex",
        "_id": "1",
        "_score": 1,
        "_source": {
          "date": "2022-06-15T10:12:52.382719622Z"
        },
        "fields": {
          "date": [
            "2022-06-15T10:12:52.382719622Z"
          ]
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 1,
        "_source": {
          "date": "2022-06-15T10:12:52.382719624Z"
        },
        "fields": {
          "date": [
            "2022-06-15T10:12:52.382719624Z"
          ]
        }
      }
    ]
  }
}
```

您可以如下所示依 `date_nanos` 欄位排序：

```json
GET testindex/_search
{
  "sort": { 
    "date": "asc"
  } 
}
```
{% include copy-curl.html %}

回應包含排序後的文件：

```json
{
  "took": 5,
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
    "max_score": null,
    "hits": [
      {
        "_index": "testindex",
        "_id": "1",
        "_score": null,
        "_source": {
          "date": "2022-06-15T10:12:52.382719622Z"
        },
        "sort": [
          1655287972382719700
        ]
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": null,
        "_source": {
          "date": "2022-06-15T10:12:52.382719624Z"
        },
        "sort": [
          1655287972382719700
        ]
      }
    ]
  }
}
```

您也可以使用 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼來存取欄位的奈秒部分：

```json
GET testindex/_search
{
  "script_fields" : {
    "my_field" : {
      "script" : {
        "lang" : "painless",
        "source" : "doc['date'].value.nano" 
      }
    }
  }
}
```
{% include copy-curl.html %}

回應僅包含欄位的奈秒部分：

```json
{
  "took": 4,
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
        "_index": "testindex",
        "_id": "1",
        "_score": 1,
        "fields": {
          "my_field": [
            382719622
          ]
        }
      },
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 1,
        "fields": {
          "my_field": [
            382719624
          ]
        }
      }
    ]
  }
}
```

## 衍生來源

當索引使用 [衍生來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source) 時，OpenSearch 在重建來源時可能會排序多值日期欄位中的值。衍生來源會以 `print_format` 中指定的格式傳回日期。如果未指定 `print_format`，且 `format` 包含以 `||` 分隔的多種日期格式，衍生來源會以第一種格式傳回日期。

建立一個啟用衍生來源並設定含多種格式之 `date_nanos` 欄位的索引：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "date_nanos": {
        "type": "date_nanos",
        "format": "strict_date_optional_time_nanos||strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```

將含有混合日期格式的文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "date_nanos": [1758504860, "2025-09-22T00:34", "2025-09-22T01:34:20Z"]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 如下：

```json
{
  "date_nanos": ["2025-09-22T00:34:00.000000000Z", "2025-09-22T01:34:00.000000000Z", "2025-09-22T01:34:00.000000000Z"]
}
```
