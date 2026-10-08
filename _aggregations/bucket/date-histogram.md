---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期長條圖"
parent: Bucket aggregations
nav_order: 20
redirect_from:
  - /query-dsl/aggregations/bucket/date-histogram/
---

# 日期長條圖彙總

`date_histogram` 彙總會使用[日期運算]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#date-math)將文件分組到以時間為基礎的桶 (bucket) 中。您可以用它來彙整每小時、每日或每月的指標、繪製流量趨勢圖表，或填入時間序列儀表板。

## 選擇合適的間隔

`date_histogram` 支援兩種間隔樣式：

- **`calendar_interval`**：將桶對齊日曆邊界，例如日、月或年。當您關注實際的日曆期間時，請使用此樣式。範例值：`"day"`、`"1M"`、`"year"`。
- **`fixed_interval`**：使用以 [SI 單位](https://en.wikipedia.org/wiki/International_System_of_Units)測量的精確持續時間。桶的長度一律相同，不受日光節約時間或月份長度影響。範例值：`"5m"`、`"12h"`、`"30d"`。

舊版 `interval` 欄位為了相容性而保留，但已被棄用。請改用 `calendar_interval` 或 `fixed_interval`。
{: .note}


## 範例：每月桶（日曆間隔）

計算每個日曆月的文件數量：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
  "size": 0,
  "aggs": {
    "logs_per_month": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "1M"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：均勻的每小時桶（固定間隔）

擷取固定間隔恰好為 1 小時的桶，不受日光節約時間變更影響：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_hour": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用時區

預設情況下，分桶會以 UTC 進行。設定 `time_zone` 可將桶的邊界對齊特定時區。

使用 `Europe/Dublin` 擷取每日桶：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_day_ie": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day",
        "time_zone": "Europe/Dublin"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用 `offset` 位移桶的起始時間

使用 `offset` 參數將桶的邊界往前或往後移動，例如，定義從 06:00 到 06:00（而非從午夜到午夜）的「報告日」：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_day_shifted": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day",
        "offset": "+6h"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：包含空的桶

將 `min_doc_count` 設為 `0`，並在 `extended_bounds` 中提供範圍，即可在整個時間範圍內傳回空的桶。

擷取過去 24 小時內固定間隔為 1 小時的桶，包括沒有資料的小時：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "last_24h": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "min_doc_count": 0,
        "extended_bounds": {"min": "now-24h", "max": "now"}
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：嚴格限制範圍

`hard_bounds` 會將長條圖嚴格限制在指定的最小與最大時間範圍內。即使資料超出這些界限，也不會在界限外建立任何桶。

擷取 `2025-09-01T00:00:00Z` 至 `2025-09-01T06:00:00Z` 期間內固定間隔為 30 分鐘的桶：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "strict_range": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "30m",
        "hard_bounds": {"min": "2025-09-01T00:00:00Z", "max": "2025-09-01T06:00:00Z"}
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用 `keyed` 傳回桶的對應表

設定 `keyed: true` 可將桶以物件形式傳回，並以格式化的日期字串作為索引鍵：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "per_month": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1M",
        "format": "yyyy-MM-dd",
        "keyed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

回應範例：

```json
{
  "aggregations": {
    "per_month": {
      "buckets": {
        "2025-01-01": {"key_as_string": "2025-01-01", "key": 1735689600000, "doc_count": 3},
        "2025-02-01": {"key_as_string": "2025-02-01", "key": 1738368000000, "doc_count": 2}
      }
    }
  }
}
```

## 範例：將缺少的日期視為固定值

使用 `missing` 參數，將沒有值的文件指派到位於所提供日期的合成桶：

```json
GET articles/_search
{
  "size": 0,
  "aggs": {
    "published_per_year": {
      "date_histogram": {
        "field": "publish_date",
        "calendar_interval": "year",
        "missing": "2000-01-01"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：排序桶

預設情況下，傳回的桶會依 `_key` 遞增排序。如有需要，請使用 `order` 參數改為遞減排序。

擷取桶並將最近的月份排在最前面：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "recent_months": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1M",
        "order": {"_key": "desc"}
      }
    }
  }
}
```
{% include copy-curl.html %}

依桶的計數排序（最高者優先）：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "busiest_hours": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "order": {"_count": "desc"}
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：以指令碼產生值來源

您可以使用 Painless 指令碼，動態產生或修改 `date_histogram` 中用於分桶的日期值。這可讓您在查詢時彈性處理複雜的日期邏輯。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。`date_histogram` 彙總無法直接處理日期物件或字串。它需要單一數值來代表每份文件的時間戳記。此值必須是代表 epoch 毫秒的長整數，也就是自 1970 年 1 月 1 日 00:00:00 UTC 起經過的毫秒數。您提供的任何指令碼都必須傳回此類型的值。下列使用 `script` 的範例，其行為與先前使用 `"field": "timestamp"` 的範例相同，但會為日期欄位產生正確的傳回類型：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_hour_script": {
      "date_histogram": {
        "script": {
          "lang": "painless",
          "source": "return doc['timestamp'].value.toInstant().toEpochMilli();"
        },
        "fixed_interval": "1h"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

`date_histogram` 彙總支援下列參數。

| 參數 | 必要 | 類型 | 說明 |
|:--|:--|:--|:--|
| `field` | 下列其中之一為必要：`field` 或 `script`。 | 字串 | 要進行分桶的日期/日期時間欄位。 |
| `calendar_interval` | 下列其中之一為必要：`calendar_interval`、`fixed_interval` 或舊版 `interval`。 | 字串 | 可感知日曆的間隔（例如 `"day"`、`"1M"`、`"year"`）。僅支援單數的日曆單位。 |
| `fixed_interval` | 下列其中之一為必要：`calendar_interval`、`fixed_interval` 或舊版 `interval`。 | 字串 | 固定間隔，例如 `"5m"`、`"12h"`、`"30d"`。不適用於月或季等日曆單位。 |
| `time_zone` | 選用 | 字串 | 用於分桶與格式化的時區。可接受時區（例如 `"Europe/Dublin"`）或 UTC 偏移量（例如 `"-07:00"`）。 |
| `format` | 選用 | 字串 | 用於 `key_as_string` 的輸出日期格式，例如 `"yyyy-MM-dd"`。若省略，則套用對應的預設值。 |
| `offset` | 選用 | 字串 | 以正或負的間隔位移桶的邊界，例如 `"+6h"`、`"-30m"`。在套用 `time_zone` 之後計算。 |
| `min_doc_count` | 選用 | 整數 | 傳回桶所需的最少文件數。預設為 `1`。設為 `0` 可包含空的桶。 |
| `extended_bounds` | 選用 | 物件 | 將桶的範圍延伸至資料範圍之外：`{"min": "<date>", "max": "<date>"}`。通常與 `min_doc_count: 0` 搭配使用。 |
| `hard_bounds` | 選用 | 物件 | 將桶嚴格限制在某個範圍內：`{"min": "<date>", "max": "<date>"}`。範圍外的桶永遠不會建立。 |
| `missing` | 選用 | 日期字串 | 將缺少該欄位的文件視為具有此日期值。 |
| `keyed` | 選用 | 布林值 | 若為 `true`，則將桶以物件形式傳回，並以格式化的日期字串作為索引鍵。 |
| `order` | 選用 | 物件 | 依 `_key` 或 `_count` 以遞增或遞減方式排序桶。 |
| `script` | 下列其中之一為必要：`field` 或 `script`。 | 物件 | 選用的指令碼，用於計算要進行分桶的值。由於指令碼會針對每個值進行修改，因此會增加額外負擔，應謹慎使用。 |

