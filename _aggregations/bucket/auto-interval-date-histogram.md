---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動間隔日期長條圖"
parent: Bucket aggregations
nav_order: 12
---

# 自動間隔日期長條圖彙總

[日期長條圖彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)必須指定間隔，而 `auto_date_histogram` 與其類似，是一種多桶 (multi-bucket) 彙總，會根據您提供的桶數量與資料的時間範圍，自動建立日期長條圖桶。實際傳回的桶數量一律小於或等於您指定的桶數量。當您處理時間序列資料，並想以不同的時間間隔將資料視覺化或進行分析，而不必手動指定間隔大小時，這種彙總特別實用。

## 間隔

系統會根據收集到的資料選擇桶間隔，以確保傳回的桶數量小於或等於請求的數量。

下表列出每個時間單位可能傳回的間隔。

| 單位   | 間隔                |
| :--- | :---|
| 秒| 1、5、10 和 30 的倍數                 |
| 分鐘| 1、5、10 和 30 的倍數                 |
| 小時  | 1、3 和 12 的倍數                     |
| 天   | 1 和 7 的倍數                         |
| 月 | 1 和 3 的倍數                         |
| 年  | 1、5、10、20、50 和 100 的倍數        |

如果彙總傳回的桶過多 (例如每日桶)，OpenSearch 會自動減少桶數量，以確保結果易於處理。OpenSearch 不會傳回與請求數量完全相同的每日桶，而是將桶數量減少約 1/7。例如，如果您請求 70 個桶，但資料包含過多的每日間隔，OpenSearch 可能只會傳回 10 個桶，並將資料分組到較大的間隔 (例如週) 中，以避免結果數量過多。當可用資料過多時，這有助於最佳化彙總並避免過度細節。

## 範例

在下列範例中，您將搜尋包含部落格文章的索引。

首先，為此索引建立對應，並將 `date_posted` 欄位指定為 `date` 類型：

```json
PUT blogs
{
  "mappings" : {
    "properties" :  {
      "date_posted" : {
        "type" : "date",
        "format" : "yyyy-MM-dd"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將下列文件編製索引至 `blogs` 索引：

```json
PUT blogs/_doc/1
{
  "name": "Semantic search in OpenSearch",
  "date_posted": "2022-04-17"
}
```
{% include copy-curl.html %}

```json
PUT blogs/_doc/2
{
  "name": "Sparse search in OpenSearch",
  "date_posted": "2022-05-02"
}
```
{% include copy-curl.html %}

```json
PUT blogs/_doc/3
{
  "name": "Distributed tracing with Data Prepper",
  "date_posted": "2022-04-25"
}
```
{% include copy-curl.html %}

```json
PUT blogs/_doc/4
{
  "name": "Observability in OpenSearch",
  "date_posted": "2023-03-23"
}

```
{% include copy-curl.html %}

若要使用 `auto_date_histogram` 彙總，請指定包含日期或時間戳記值的欄位。例如，若要依 `date_posted` 將部落格文章彙總至兩個桶，請傳送下列請求：

```json
GET /blogs/_search
{
  "size": 0,
  "aggs": {
    "histogram": {
      "auto_date_histogram": {
        "field": "date_posted",
        "buckets": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

回應顯示部落格文章已彙總至兩個桶。間隔已自動設為 1 年，所有三篇 2022 年的部落格文章收集在一個桶中，而 2023 年的部落格文章則在另一個桶中：

```json
{
  "took": 20,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "histogram": {
      "buckets": [
        {
          "key_as_string": "2022-01-01",
          "key": 1640995200000,
          "doc_count": 3
        },
        {
          "key_as_string": "2023-01-01",
          "key": 1672531200000,
          "doc_count": 1
        }
      ],
      "interval": "1y"
    }
  }
}
```

## 傳回的桶

每個桶包含下列資訊：

```json
{
  "key_as_string": "2023-01-01",
  "key": 1672531200000,
  "doc_count": 1
}
```

在 OpenSearch 中，日期在內部以 64 位元整數儲存，代表自 epoch 起算的毫秒時間戳記。在彙總回應中，每個桶的 `key` 都會以這種時間戳記傳回。`key_as_string` 值顯示相同的時間戳記，但會根據 [`format`](#date-format) 參數格式化為日期字串。`doc_count` 欄位包含桶中的文件數量。

## 參數

自動間隔日期長條圖彙總接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`field` | 字串 | 要進行彙總的欄位。此欄位必須包含日期或時間戳記值。`field` 或 `script` 兩者必須擇一提供。
`buckets` | 整數 | 想要的桶數量。傳回的桶數量會小於或等於想要的數量。選用。預設為 `10`。
`minimum_interval` | 字串 | 要使用的最小間隔。指定最小間隔可讓彙總程序更有效率。有效值為 `year`、`month`、`day`、`hour`、`minute` 和 `second`。選用。
`time_zone` | 字串 | 指定在分桶與捨入時使用預設 (UTC) 以外的時區。您可以將 `time_zone` 參數指定為 [UTC 時差](https://en.wikipedia.org/wiki/UTC_offset)，例如 `-04:00`，或指定為 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)，例如 `America/New_York`。選用。預設為 `UTC`。如需詳細資訊，請參閱[時區](#time-zone)。
`format` | 字串 | 傳回代表桶鍵之日期時所用的格式。選用。預設為欄位對應中指定的格式。如需詳細資訊，請參閱[日期格式](#date-format)。
`script` | 字串 | 用於將值彙總至桶中的文件層級或值層級指令碼。`field` 或 `script` 兩者必須擇一提供。
`missing` | 字串 | 指定如何處理缺少欄位值的文件。根據預設，系統會忽略這類文件。如果您在 `missing` 參數中指定日期值，所有缺少欄位值的文件都會收集到具有指定日期的桶中。

## 日期格式

如果您未指定 `format` 參數，系統會使用欄位對應中定義的格式 (如前述回應所示)。若要修改格式，請指定 `format` 參數：

```json
GET /blogs/_search
{
  "size": 0,
  "aggs": {
    "histogram": {
      "auto_date_histogram": {
        "field": "date_posted",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```
{% include copy-curl.html %}

現在 `key_as_string` 欄位會以指定的格式傳回：

```json
{
  "key_as_string": "2023-01-01 00:00:00",
  "key": 1672531200000,
  "doc_count": 1
}
```

或者，您也可以指定其中一種內建日期[格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)：

```json
GET /blogs/_search
{
  "size": 0,
  "aggs": {
    "histogram": {
      "auto_date_histogram": {
        "field": "date_posted",
        "format": "basic_date_time_no_millis"
      }
    }
  }
}
```
{% include copy-curl.html %}

現在 `key_as_string` 欄位會以指定的格式傳回：

```json
{
  "key_as_string": "20230101T000000Z",
  "key": 1672531200000,
  "doc_count": 1
}
```

## 時區

根據預設，日期會以 UTC 儲存與處理。`time_zone` 參數可讓您為分桶指定不同的時區。您可以將 `time_zone` 參數指定為 [UTC 時差](https://en.wikipedia.org/wiki/UTC_offset)，例如 `-04:00`，或指定為 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)，例如 `America/New_York`。

舉例來說，將下列文件編製索引至某個索引：

```json
PUT blogs1/_doc/1
{
  "name": "Semantic search in OpenSearch",
  "date_posted": "2022-04-17T01:00:00.000Z"
}
```
{% include copy-curl.html %}

```json
PUT blogs1/_doc/2
{
  "name": "Sparse search in OpenSearch",
  "date_posted": "2022-04-17T04:00:00.000Z"
}
```
{% include copy-curl.html %}

首先，在不指定時區的情況下執行彙總：

```json
GET /blogs1/_search
{
  "size": 0,
  "aggs": {
    "histogram": {
      "auto_date_histogram": {
        "field": "date_posted",
        "buckets": 2,
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩個 3 小時的桶，從 2022 年 4 月 17 日 UTC 午夜開始：

```json
{
  "took": 6,
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
    "hits": []
  },
  "aggregations": {
    "histogram": {
      "buckets": [
        {
          "key_as_string": "2022-04-17 01:00:00",
          "key": 1650157200000,
          "doc_count": 1
        },
        {
          "key_as_string": "2022-04-17 04:00:00",
          "key": 1650168000000,
          "doc_count": 1
        }
      ],
      "interval": "3h"
    }
  }
}
```

現在，將 `time_zone` 指定為 `-02:00`：

```json
GET /blogs1/_search
{
  "size": 0,
  "aggs": {
    "histogram": {
      "auto_date_histogram": {
        "field": "date_posted",
        "buckets": 2,
        "format": "yyyy-MM-dd HH:mm:ss",
        "time_zone": "-02:00"
      }
    }
  }
}
```

回應包含兩個桶，其開始時間偏移了 2 小時，從 2022 年 4 月 16 日 23:00 開始：

```json
{
  "took": 17,
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
    "hits": []
  },
  "aggregations": {
    "histogram": {
      "buckets": [
        {
          "key_as_string": "2022-04-16 23:00:00",
          "key": 1650157200000,
          "doc_count": 1
        },
        {
          "key_as_string": "2022-04-17 02:00:00",
          "key": 1650168000000,
          "doc_count": 1
        }
      ],
      "interval": "3h"
    }
  }
}
```

使用有日光節約時間 (DST) 變更的時區時，接近轉換時間點的桶大小可能與相鄰桶的大小略有不同。
{: .note}
