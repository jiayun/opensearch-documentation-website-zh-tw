---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期範圍"
parent: Bucket aggregations
nav_order: 30
redirect_from:
  - /query-dsl/aggregations/bucket/date-range/
---

# 日期範圍彙總

使用 `date_range` 彙總，將文件分組到由日期邊界定義的桶中。`date_range` 彙總的行為類似數值的 `range` 彙總，但除了 [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) 日期與 epoch 毫秒之外，還接受日期數學運算式。

請注意以下細節：

- `from` 為包含，`to` 為不包含。
- 若要建立無界限的桶，請省略 `from` 或 `to`。
- 日期數學支援捨入：例如 `now-7d/d`（7 天前當天的起始時間）。

## 參數

下表列出 `date_range` 彙總接受的參數。

| 參數 | 必要 | 說明 |
| --- | --- | --- |
| `field` | 是 | 用於彙總的日期欄位。 |
| `ranges`| 是 | 非空的範圍物件陣列。既未指定 `from` 也未指定 `to` 的範圍會比對所有值。 |
| `ranges[].from` | 否 | 包含的下限。 |
| `ranges[].to` | 否 | 不包含的上限。 |
| `ranges[].key`| 否 | 桶的標籤。|
| `format`| 否 | 用於在 `from_as_string` 與 `to_as_string` 回應欄位中顯示桶邊界，以及在 `from` 與 `to` 中解析日期字串的日期格式，例如 `yyyy-MM-dd`。 |
| `time_zone` | 否 | 用於評估日期數學、捨入，以及 `from` 與 `to` 中未指定時區偏移之日期字串的 IANA 時區或 UTC 偏移，例如 `Europe/Dublin` 或 `+01:00`。使用 `Europe/Dublin` 時，`"from": "2025-10-01"` 會被評估為 `2025-10-01T00:00:00+01:00`。 |
| `keyed` | 否 | 若為 `true`，則以物件而非陣列的形式回傳桶。每個桶以其 `key` 值作為鍵，該值是您為範圍指定的自訂 `key`，或是產生的鍵，例如 `*-2025-09-20T00:00:00.000Z`。預設為 `false`。 |
| `missing` | 否 | 用來替代欄位缺失之文件的值。 |


### `from` 與 `to` 的可接受值

`from` 與 `to` 接受下列值：

- ISO 8601 字串：`"2025-10-01T00:00:00Z"`、`"2025-10-01"`
- 日期數學：`"now-7d/d"`、`"now+1M/M"`、`"2025-09-01||/M"`
- Epoch 毫秒：`1756684800000`

若日期字串中省略了某些組成部分，缺少的部分會以預設值填入。例如，`"2025-10"` 會被視為 2025 年 10 月的起始。
{: .note}

## 範例設定

本頁的範例使用 `my-index` 索引。請建立索引，並將 `event_time` 欄位對應為接受 epoch 毫秒：

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "event_time": { "type": "date", "format": "epoch_millis" }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引。文件 6 沒有 `@timestamp` 值：

```json
POST my-index/_bulk?refresh
{ "index": { "_id": "1" } }
{ "@timestamp": "2025-09-10T12:00:00Z", "event_time": 1697400000000 }
{ "index": { "_id": "2" } }
{ "@timestamp": "2025-09-18T09:00:00Z", "event_time": 1697500000000 }
{ "index": { "_id": "3" } }
{ "@timestamp": "2025-09-22T15:00:00Z", "event_time": 1698000000000 }
{ "index": { "_id": "4" } }
{ "@timestamp": "2025-09-26T08:00:00Z" }
{ "index": { "_id": "5" } }
{ "@timestamp": "2025-10-01T07:30:00Z" }
{ "index": { "_id": "6" } }
{ "note": "no timestamp" }
```
{% include copy-curl.html %}

為了讓本頁的回應不依賴於您執行範例的時間，範例中的日期數學是以固定日期 `2025-10-01` 並使用 `||` 分隔符計算。若要從目前時間計算範圍，請將 `2025-10-01||` 替換為 `now`。例如，使用 `now-7d/d` 而非 `2025-10-01||-7d/d`。

## 範例：三個滑動時間窗

下列範例使用日期數學與 `yyyy-MM-dd` 輸出 `format`，產生三個桶（最近 7 天、前一個 7 天，以及更早）：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "by_range": {
      "date_range": {
        "field": "@timestamp",
        "format": "yyyy-MM-dd",
        "ranges": [
          {
            "from": "2025-10-01||-7d/d",
            "to": "2025-10-01||+1d/d",
            "key": "last_7d"
          },
          {
            "from": "2025-10-01||-14d/d",
            "to": "2025-10-01||-7d/d",
            "key": "prev_7d"
          },
          {
            "to": "2025-10-01||-14d/d",
            "key": "older"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含這三個桶：

```json
{
  "aggregations": {
    "by_range": {
      "buckets": [
        {
          "key": "older",
          "to": 1758067200000.0,
          "to_as_string": "2025-09-17",
          "doc_count": 1
        },
        {
          "key": "prev_7d",
          "from": 1758067200000.0,
          "from_as_string": "2025-09-17",
          "to": 1758672000000.0,
          "to_as_string": "2025-09-24",
          "doc_count": 2
        },
        {
          "key": "last_7d",
          "from": 1758672000000.0,
          "from_as_string": "2025-09-24",
          "to": 1759363200000.0,
          "to_as_string": "2025-10-02",
          "doc_count": 2
        }
      ]
    }
  }
}
```

## 範例：最近 10 天的桶與自訂字串格式

下列請求建立一個涵蓋 2025 年 10 月 1 日之前 10 天以及 10 月 1 日全天的桶。桶從 10 天前當天的起始時間（`-10d/d`）開始，並在隔天的起始時間（`+1d/d`，不包含）結束。

`format` 決定桶邊界在 `from_as_string` 與 `to_as_string` 回應欄位中的顯示方式。它也用於解析 `from` 與 `to` 中的日期字串，因此每個邊界中的日期必須使用相同格式。在此範例中，格式為 `yyyy-MM`，因此邊界以 `2025-10` 開頭，該字串會被解析為 2025 年 10 月 1 日：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "last_10_days": {
      "date_range": {
        "field": "@timestamp",
        "format": "yyyy-MM",
        "ranges": [
          {
            "from": "2025-10||-10d/d",
            "to": "2025-10||+1d/d"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含文件 3、4 與 5。`from_as_string` 與 `to_as_string` 欄位使用 `yyyy-MM` 格式：

```json
{
  "aggregations": {
    "last_10_days": {
      "buckets": [
        {
          "key": "2025-09-2025-10",
          "from": 1758412800000.0,
          "from_as_string": "2025-09",
          "to": 1759363200000.0,
          "to_as_string": "2025-10",
          "doc_count": 3
        }
      ]
    }
  }
}
```

## 範例：鍵值式回應與自訂鍵

下列請求回傳一個依您的標籤組織的物件，方便後續處理：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "keyed_ranges": {
      "date_range": {
        "field": "@timestamp",
        "keyed": true,
        "ranges": [
          {
            "from": "2025-10-01||/d",
            "to": "2025-10-01||+1d/d",
            "key": "today"
          },
          {
            "to": "2025-10-01||/d",
            "key": "before_today"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含一個 `today` 桶與一個 `before_today` 桶：

```json
{
  "aggregations": {
    "keyed_ranges": {
      "buckets": {
        "before_today": {
          "to": 1759276800000.0,
          "to_as_string": "2025-10-01T00:00:00.000Z",
          "doc_count": 4
        },
        "today": {
          "from": 1759276800000.0,
          "from_as_string": "2025-10-01T00:00:00.000Z",
          "to": 1759363200000.0,
          "to_as_string": "2025-10-02T00:00:00.000Z",
          "doc_count": 1
        }
      }
    }
  }
}
```

## 範例：帶時區的 epoch 毫秒

當欄位值以 epoch 毫秒提供時，您仍可以將 `from` 與 `to` 參數以數字提供。在下列請求中，`time_zone` 會影響日期數學與邊界評估：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "local_ranges": {
      "date_range": {
        "field": "event_time",
        "time_zone": "Europe/Dublin",
        "format": "epoch_millis",
        "ranges": [
          {
            "from": "1697328000000",
            "to": "1697932800000",
            "key": "week_sample"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

即使邊界是 epoch 毫秒，`time_zone` 仍會套用到邊界。在 2023 年 10 月，都柏林比 UTC 快一小時，因此回應中的兩個邊界都比請求中的值早一小時（`3600000` 毫秒）：

```json
{
  "aggregations": {
    "local_ranges": {
      "buckets": [
        {
          "key": "week_sample",
          "from": 1697324400000.0,
          "from_as_string": "1697324400000",
          "to": 1697929200000.0,
          "to_as_string": "1697929200000",
          "doc_count": 2
        }
      ]
    }
  }
}
```

## 範例：處理缺失的日期

使用 `missing`，以預設值替代的方式，將沒有值的文件歸入某個桶：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "dated_or_undated": {
      "date_range": {
        "field": "@timestamp",
        "missing": "1970-01-01",
        "ranges": [
          {
            "to": "2000-01-01",
            "key": "undated_or_old"
          },
          {
            "from": "2000-01-01",
            "key": "dated_recent"
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

沒有 `@timestamp` 值的文件 6 會被計入 `undated_or_old` 桶：

```json
{
  "aggregations": {
    "dated_or_undated": {
      "buckets": [
        {
          "key": "undated_or_old",
          "to": 946684800000.0,
          "to_as_string": "2000-01-01T00:00:00.000Z",
          "doc_count": 1
        },
        {
          "key": "dated_recent",
          "from": 946684800000.0,
          "from_as_string": "2000-01-01T00:00:00.000Z",
          "doc_count": 5
        }
      ]
    }
  }
}
```
