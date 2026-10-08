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

使用 `date_range` 彙總，依日期邊界所定義的桶 (bucket) 將文件分組。`date_range` 彙總的行為與數值型 `range` 彙總類似，但除了 [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) 日期和 epoch 毫秒之外，還接受日期運算 (date math)。

請注意下列細節：

- `from` 包含邊界值，`to` 不包含邊界值。
- 若要建立開放式的桶，請省略 `from` 或 `to`。
- 日期運算支援捨入，例如 `now-7d/d`（7 天前當天的開始時間）。

## 參數

下表列出 `date_range` 彙總接受的參數。

| 參數 | 必要 | 說明 |
| --- | --- | --- |
| `field` | 是 | 要進行彙總的日期欄位。 |
| `ranges`| 是 | 由範圍物件組成的非空陣列。每個物件必須至少指定一個邊界，即 `from` 和/或 `to`。 |
| `ranges[].from` | `from` 或 `to` 必須擇一提供。 | 包含邊界值的下限。 |
| `ranges[].to` | `from` 或 `to` 必須擇一提供。 | 不包含邊界值的上限。 |
| `ranges[].key`| 否 | 桶的標籤。|
| `format`| 否 | 控制回應中的 `*_as_string` 欄位，例如 `yyyy-MM-dd`。 |
| `time_zone` | 否 | 評估日期運算或捨入時所使用的 IANA 時區或 UTC 偏移量，例如 `Europe/Dublin`、`+01:00`。 |
| `keyed` | 否 | 若為 `true`，則傳回以 `key` 為鍵的物件，而非陣列。 |
| `missing` | 否 | 用來替代缺少該欄位之文件的值。 |


### `from` 和 `to` 可接受的值

`from` 和 `to` 可接受下列值：

- ISO 8601 字串：`"2025-10-01T00:00:00Z"`、`"2025-10-01"`
- 日期運算：`"now-7d/d"`、`"now+1M/M"`、`"2025-09-01||/M"`
- Epoch 毫秒：`1756684800000`

若日期字串中省略了部分組成元素，缺少的部分會以預設值填入。例如，`"2025-10"` 會被視為 2025 年 10 月的開始時間。
{: .note}

## 範例：三個滑動時間窗

下列範例使用日期運算和 `yyyy-MM-dd` 輸出 `format`，產生三個桶（最近 7 天、前 7 天，以及更早的資料）：

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
          { "from": "now-7d/d",  "to": "now+1d/d", "key": "last_7d" },
          { "from": "now-14d/d", "to": "now-7d/d", "key": "prev_7d" },
          { "to": "now-14d/d",                      "key": "older"  }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應範例：

```json
"aggregations": {
    "by_range": {
      "buckets": [
        {
          "key": "older",
          "to": 1758067200000,
          "to_as_string": "2025-09-17",
          "doc_count": 1
        },
        {
          "key": "prev_7d",
          "from": 1758067200000,
          "from_as_string": "2025-09-17",
          "to": 1758672000000,
          "to_as_string": "2025-09-24",
          "doc_count": 2
        },
        {
          "key": "last_7d",
          "from": 1758672000000,
          "from_as_string": "2025-09-24",
          "to": 1759363200000,
          "to_as_string": "2025-10-02",
          "doc_count": 2
        }
      ]
    }
  }
```

## 範例：使用自訂字串格式建立最近 10 天的桶

下列請求會建立單一桶，涵蓋最近 10 個日曆天。其起點為 10 天前當天的開始時間（`now-10d/d`），終點為明天的開始時間（`now+1d/d`，不包含）。`format` 只會影響回應中的 `*_as_string` 欄位，而不會影響文件比對：

```json
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "last_10_days": {
      "date_range": {
        "field": "@timestamp",
        "format": "yyyy-MM",
        "ranges": [ { "from": "now-10d/d", "to": "now+1d/d" } ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：具鍵值的回應與自訂鍵

下列請求會傳回依您的標籤組織的物件，以便後續處理：

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
          { "from": "now-1d/d", "to": "now+1d/d", "key": "today" },
          { "to": "now-1d/d", "key": "before_today" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應範例：

```json
"aggregations": {
    "keyed_ranges": {
      "buckets": {
        "before_today": {
          "to": 1759190400000,
          "to_as_string": "2025-09-30T00:00:00.000Z",
          "doc_count": 4
        },
        "today": {
          "from": 1759190400000,
          "from_as_string": "2025-09-30T00:00:00.000Z",
          "to": 1759363200000,
          "to_as_string": "2025-10-02T00:00:00.000Z",
          "doc_count": 1
        }
      }
    }
  }
```

## 範例：搭配時區使用 epoch 毫秒

當欄位值以 epoch 毫秒提供時，您仍可將 `from` 和 `to` 參數以數字形式提供。例如，在下列請求中，`time_zone` 會影響日期運算和邊界評估：

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
          { "from": "1697328000000", "to": "1697932800000", "key": "week_sample" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：處理缺少的日期

使用 `missing` 代入預設值，將沒有值的文件歸入某個桶：

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
          { "to": "2000-01-01", "key": "undated_or_old" },
          { "from": "2000-01-01", "key": "dated_recent" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}
