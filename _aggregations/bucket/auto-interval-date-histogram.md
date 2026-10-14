---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動間隔日期直方圖"
parent: Bucket aggregations
nav_order: 12
---

# 自動間隔日期直方圖彙總

與[日期直方圖彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)類似，您必須在其中指定間隔，`auto_date_histogram` 是一種多桶彙總，會根據您提供的桶數與資料的時間範圍，自動建立日期直方圖桶。實際傳回的桶數一律小於或等於您指定的桶數。當您處理時間序列資料，並希望在不同時間間隔上視覺化或分析資料，而不想手動指定間隔大小時，此彙總特別有用。

## 間隔

桶間隔會根據收集到的資料選擇，以確保傳回的桶數小於或等於要求的數量。

下表列出每個時間單位可能的傳回間隔。

| 單位   | 間隔                |
| :--- | :---|
| 秒 | 1、5、10 與 30 的倍數                 |
| 分鐘 | 1、5、10 與 30 的倍數                 |
| 小時  | 1、3 與 12 的倍數                     |
| 天   | 1 與 7 的倍數                         |
| 月 | 1 與 3 的倍數                         |
| 年  | 1、5、10、20、50 與 100 的倍數        |

如果彙總傳回太多桶（例如每日桶），OpenSearch 會自動減少桶數，以確保結果易於管理。它不會傳回要求的每日桶數，而是將桶數減至約原來的七分之一。例如，如果您要求 70 個桶，但資料包含太多每日間隔，OpenSearch 可能只會傳回 10 個桶，將資料分組為較大的間隔（例如週），以避免結果過多。這有助於最佳化彙總，並在資料過多時防止過度細節。

## 參數

自動間隔日期直方圖彙總接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :--- 
`field` | 字串 | 要彙總的欄位。該欄位必須包含日期或時間戳記值。`field` 與 `script` 至少須指定其中一個。
`buckets` | 整數 | 想要的桶數。傳回的桶數會小於或等於想要的數量。選用。預設為 `10`。
`minimum_interval` | 字串 | 要使用的最小間隔。指定最小間隔可使彙總過程更有效率。有效值為 `year`、`month`、`day`、`hour`、`minute` 與 `second`。選用。
`time_zone` | 字串 | 指定在分桶與捨入時使用預設 (UTC) 以外的時區。您可以將 `time_zone` 參數指定為 [UTC 偏移](https://en.wikipedia.org/wiki/UTC_offset)，例如 `-04:00`，或 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)，例如 `America/New_York`。選用。預設為 `UTC`。如需更多資訊，請參閱[時區](#time-zone)。
`format` | 字串 | 傳回代表桶鍵之日期的格式。選用。預設為欄位對應中指定的格式。如需更多資訊，請參閱[日期格式](#date-format)。
`script` | 字串 | 用於將值彙總到桶中的文件層級或值層級指令碼。`field` 與 `script` 至少須指定其中一個。
`missing` | 字串 | 指定如何處理欄位值遺漏的文件。預設情況下，這類文件會被忽略。如果您在 `missing` 參數中指定日期值，所有欄位值遺漏的文件都會收集到具有指定日期的桶中。

## 範例

在下列範例中，您將搜尋包含網誌文章的索引。

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

接下來，將下列文件編製索引到 `blogs` 索引中：

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

若要使用 `auto_date_histogram` 彙總，請指定包含日期或時間戳記值的欄位。例如，若要依 `date_posted` 將網誌文章彙總為兩個桶，請傳送下列請求：

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

回應顯示網誌文章被彙總為兩個桶。間隔自動設定為 1 年，2022 年的三篇文章收集在同一個桶中，2023 年的文章則在另一個桶中：

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

在 OpenSearch 中，日期內部以 64 位元整數儲存，代表自 epoch 起以毫秒為單位的時間戳記。在彙總回應中，每個桶的 `key` 都會以此類時間戳記傳回。`key_as_string` 值顯示相同的時間戳記，但根據 [`format`](#date-format) 參數格式化為日期字串。`doc_count` 欄位包含桶中的文件數。

## 日期格式

如果您未指定 `format` 參數，則會使用欄位對應中定義的格式（如前述回應所示）。若要修改格式，請指定 `format` 參數：

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

`key_as_string` 欄位現在會以指定格式傳回：

```json
{
  "key_as_string": "2023-01-01 00:00:00",
  "key": 1672531200000,
  "doc_count": 1
}
```

或者，您可以指定其中一種內建日期[格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)：

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

`key_as_string` 欄位現在會以指定格式傳回：

```json
{
  "key_as_string": "20230101T000000Z",
  "key": 1672531200000,
  "doc_count": 1
}
```

## 時區

預設情況下，日期以 UTC 儲存與處理。`time_zone` 參數可讓您為分桶指定不同的時區。您可以將 `time_zone` 參數指定為 [UTC 偏移](https://en.wikipedia.org/wiki/UTC_offset)，例如 `-04:00`，或 [IANA 時區 ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)，例如 `America/New_York`。

舉例來說，將下列文件編製索引到索引中：

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

回應包含兩個 3 小時的桶，從 2022 年 4 月 17 日的 UTC 午夜開始：

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

回應包含兩個桶，其開始時間偏移 2 小時，並從 2022 年 4 月 16 日的 23:00 開始：

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

使用有日光節約時間 (DST) 變更的時區時，接近轉換時間的桶大小可能與相鄰桶的大小略有不同。
{: .note}
